from datetime import datetime
from typing import Optional, List

import numpy as np
from PySide6.QtCore import QMimeData, Signal, QMargins
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QScrollArea
from SciQLopPlots import QCustomPlot, QCPMarginGroup, QCPAxisRect, QCP

from SciQLop.backend.pipelines_model.auto_register import auto_register
from SciQLop.backend.pipelines_model.base import PipelineModelItem
from SciQLop.backend.pipelines_model.base import model as pipelines_model
from .abstract_plot_panel import MetaPlotPanel, PlotPanel, PanelContainer
from .time_series_plot import TimeSeriesPlot
from ..drag_and_drop import DropHandler, DropHelper, PlaceHolderManager
from ...backend import Product
from ...backend import TimeRange
from ...backend import listify
from ...backend import logging
from ...mime import decode_mime
from ...mime.types import PRODUCT_LIST_MIME_TYPE

log = logging.getLogger(__name__)


class TSPanelContainer(PanelContainer):
    def __init__(self, parent=None):
        PanelContainer.__init__(self, TimeSeriesPlot, parent=parent)
        # self._margin_group = QCPMarginGroup(None)

    def add_widget(self, widget: QWidget, index: int):
        # if isinstance(widget, TimeSeriesPlot):
        #    widget.set_margin_group(self._margin_group)

        PanelContainer.add_widget(self, widget, index)

    def update_margins(self):
        axis_rects: List[QCPAxisRect] = [w.plot_instance.axisRect() for w in self.plots]
        if len(axis_rects):
            max_left_margin = 0
            min_right_pos = 1e9
            for ar in axis_rects:
                left_margin = ar.calculateAutoMargin(QCP.MarginSide.msLeft)
                max_left_margin = max(max_left_margin, left_margin)
                w = ar.width()
                min_right_pos = min(min_right_pos, ar.margins().left() + w)

            for ar in axis_rects:
                margins = ar.margins()
                total_w = ar.width() + margins.left() + margins.right()
                new_right_margin = total_w - min_right_pos
                ar.setMinimumMargins(QMargins(max_left_margin, ar.calculateAutoMargin(QCP.MarginSide.msTop),
                                              new_right_margin,
                                              ar.calculateAutoMargin(QCP.MarginSide.msTop)))


pipelines_model.register_icon("QCP", QIcon("://icons/QCP.png"))


@auto_register
class TimeSyncPanel(QScrollArea, PlotPanel, metaclass=MetaPlotPanel):
    time_range_changed = Signal(TimeRange)
    _time_range: TimeRange = TimeRange(0., 0.)
    delete_me = Signal(object)
    plot_list_changed = Signal()

    def __init__(self, name: str, parent=None, time_range: Optional[TimeRange] = None):
        QScrollArea.__init__(self, parent)
        self.setObjectName(name)
        self.setContentsMargins(0, 0, 0, 0)
        self._name = name
        self._plot_container = TSPanelContainer(parent=self)
        self.setWidget(self._plot_container)
        self.setWidgetResizable(True)
        self.time_range = time_range or TimeRange(datetime.utcnow().timestamp(), datetime.utcnow().timestamp())
        self._drop_helper = DropHelper(widget=self,
                                       handlers=[
                                           DropHandler(mime_type=PRODUCT_LIST_MIME_TYPE,
                                                       callback=self._plot_mime)])
        self._place_holder_manager = PlaceHolderManager(self,
                                                        handlers=[DropHandler(mime_type=PRODUCT_LIST_MIME_TYPE,
                                                                              callback=self._insert_plots)])

        self._plot_container.plot_list_changed.connect(self.plot_list_changed)
        self._parent_node = None

    @property
    def time_range(self) -> TimeRange:
        return self._time_range

    @time_range.setter
    def time_range(self, time_range: TimeRange):
        if self._time_range != time_range:
            self._time_range = time_range
            for p in self.plots:
                p.time_range = time_range
            self.time_range_changed.emit(time_range)
            self._plot_container.update_margins()

    @property
    def name(self):
        return self.objectName()

    @name.setter
    def name(self, new_name):
        with pipelines_model.model_update_ctx():
            self.setObjectName(new_name)

    def __repr__(self):
        return f"TimeSyncPanel: {self._name}"

    @property
    def place_holder_manager(self):
        return self._place_holder_manager

    def indexOf(self, widget: QWidget):
        return self._plot_container.indexOf(widget)

    def index_of(self, child):
        return self._plot_container.indexOf(child)

    def child_at(self, row: int):
        if 0 <= row < len(self._plot_container.plots):
            return self._plot_container.plots[row]
        return None

    @property
    def plots(self) -> List[TimeSeriesPlot]:
        return self._plot_container.plots

    def _insert_plots(self, mime_data: QMimeData, placeholder: QWidget) -> bool:
        assert mime_data.hasFormat(PRODUCT_LIST_MIME_TYPE)
        products = decode_mime(mime_data, preferred_formats=[PRODUCT_LIST_MIME_TYPE])
        self.plot(products, self.indexOf(placeholder))
        return True

    def _plot_mime(self, mime_data: QMimeData, index=None) -> bool:
        assert mime_data.hasFormat(PRODUCT_LIST_MIME_TYPE)
        products = decode_mime(mime_data, preferred_formats=[PRODUCT_LIST_MIME_TYPE])
        self.plot(products, -1)
        return True

    def _plot(self, product: Product or str, index: int) -> bool:
        if product is not None:
            p = TimeSeriesPlot(parent=self)
            p.time_range_changed.connect(lambda time_range: TimeSyncPanel.time_range.fset(self, time_range))
            p.time_range = self.time_range
            self._plot_container.add_widget(p, index)
            p.parent_node = self
            p.plot(product)
            p.parent_place_holder_manager = self._place_holder_manager
            return True
        return False

    def plot(self, products: List[Product or str] or Product or str, index: Optional[int] = None):
        products = listify(products)
        indexes = [-1] * len(products) if index is None else range(index, index + len(products))
        list(map(lambda p_i: self._plot(*p_i), zip(products, indexes)))

    def update_margins(self):
        self._plot_container.update_margins()

    def replot(self, refresh_priority=QCustomPlot.rpQueuedReplot):
        for p in self.plots:
            p.replot(refresh_priority)

    def insertWidget(self, index: int, widget: QWidget or TimeSeriesPlot):
        self._plot_container.add_widget(widget, index)

    def count(self) -> int:
        return self._plot_container.count()

    def __getitem__(self, index: int) -> TimeSeriesPlot:
        plots = filter(lambda w: isinstance(w, TimeSeriesPlot), self._plot_container.plots)
        return list(plots)[index]

    def select(self):
        self.setStyleSheet("border: 3px dashed blue")

    def unselect(self):
        self.setStyleSheet("")

    def __del__(self):
        log.debug("deleting TimeSyncPanel")

    def __eq__(self, other: 'PipelineModelItem') -> bool:
        return self is other

    @property
    def icon(self) -> str:
        return "QCP"

    @property
    def parent_node(self) -> 'PipelineModelItem':
        return self._parent_node

    @parent_node.setter
    def parent_node(self, parent: 'PipelineModelItem'):
        with pipelines_model.model_update_ctx():
            if self._parent_node is not None:
                self._parent_node.remove_children_node(self)
            self._parent_node = parent
            if parent is not None:
                parent.add_children_node(self)

    @property
    def children_nodes(self) -> List['PipelineModelItem']:
        return self._plot_container.plots

    def remove_children_node(self, node: 'PipelineModelItem'):
        self._plot_container.remove_plot(node)

    def add_children_node(self, node: 'PipelineModelItem'):
        pass

    def delete_node(self):
        self._plot_container.close()
        self.delete_me.emit(self)
