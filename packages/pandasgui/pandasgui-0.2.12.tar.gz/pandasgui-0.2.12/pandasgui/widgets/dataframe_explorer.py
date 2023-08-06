import sys
from typing import List
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from pandasgui.widgets.dataframe_viewer import DataFrameViewer
from pandasgui.widgets.grapher import Grapher
from pandasgui.widgets.reshaper import Reshaper
from pandasgui.widgets.filter_viewer import FilterViewer
from pandasgui.widgets.stats_viewer import StatisticsViewer
from pandasgui.widgets.dock_widget import DockWidget
from pandasgui.store import PandasGuiDataFrameStore

import logging

logger = logging.getLogger(__name__)


class DataFrameExplorer(QtWidgets.QMainWindow):
    def __init__(self, pgdf: PandasGuiDataFrameStore):
        super().__init__()

        pgdf = PandasGuiDataFrameStore.cast(pgdf)
        pgdf.dataframe_explorer = self
        self.pgdf = pgdf

        # Dock setup
        self.docks: List[DockWidget] = []
        self.setDockOptions(self.GroupedDragging | self.AllowTabbedDocks | self.AllowNestedDocks)
        self.setTabPosition(Qt.AllDockWidgetAreas, QtWidgets.QTabWidget.North)

        #
        self.filter_viewer = FilterViewer(pgdf)
        self.dataframe_viewer = DataFrameViewer(pgdf)
        self.statistics_viewer = StatisticsViewer(pgdf)
        self.grapher = Grapher(pgdf)
        self.reshaper = Reshaper(pgdf)

        self.filters_dock = self.add_view(self.filter_viewer, "Filters")
        self.dataframe_dock = self.add_view(self.dataframe_viewer, "DataFrame")
        self.statistics_dock = self.add_view(self.statistics_viewer, "Statistics")
        self.grapher_dock = self.add_view(self.grapher, "Grapher")
        self.reshaper_dock = self.add_view(self.reshaper, "Reshaper")

        def set_active_tab(name):
            self.active_tab = name

        self.dataframe_dock.activated.connect(lambda: set_active_tab("DataFrame"))
        self.filters_dock.activated.connect(lambda: set_active_tab("Filters"))
        self.statistics_dock.activated.connect(lambda: set_active_tab("Statistics"))
        self.grapher_dock.activated.connect(lambda: set_active_tab("Grapher"))
        self.reshaper_dock.activated.connect(lambda: set_active_tab("Reshaper"))

        # Layout
        self.dataframe_viewer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.addDockWidget(Qt.RightDockWidgetArea, self.filters_dock)

        # Filter dock sizing
        # self.filters_dock.setFixedWidth(self.filter_viewer.sizeHint().width())
        self.filters_dock.setFixedWidth(self.filter_viewer.sizeHint().width() + 50)
        self.filters_dock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)

    def add_view(self, widget: QtWidgets.QWidget, title: str):
        dock = DockWidget(title, self.pgdf.name)
        dock.setAllowedAreas(Qt.AllDockWidgetAreas)

        frame = QtWidgets.QFrame()
        frame.setFrameStyle(frame.Box | frame.Raised)
        frame.setLineWidth(2)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(widget)
        frame.setLayout(layout)
        dock.setWidget(frame)

        if len(self.docks) > 0:
            self.tabifyDockWidget(self.docks[0], dock)
            # Keep the first tab active by default
            self.docks[0].raise_()
        else:
            self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        self.docks.append(dock)
        return dock


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    from pandasgui.datasets import pokemon

    # Create and show widget
    dfe = DataFrameExplorer(pokemon)
    dfe.show()

    sys.exit(app.exec_())
