from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import QHBoxLayout, QSizePolicy, QWidget

from pynetix.widgets.filetreewidget import FileTreeWidget
from pynetix.widgets.foldwidget import FoldWidget
from pynetix.widgets.sidebar import SideBar
from pynetix.widgets.splitter import Splitter


class MainTab(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.plotarea = None
        self.sidebar = None
        self.splitter = None
        self.filetree = None
        self.tools = None
        self.metaData = None

        self._initLayout()
        self._initSplitter()
        self._initSidebar()
        self._initFiletree()
        self._initTools()
        self._initMetadata()
        self._initPlotarea()

        self.readSettings()
        self.sidebar.readSettings()

    def readSettings(self) -> None:
        if 'maintab/splitterSizes' in QSettings().allKeys():
            sizes = QSettings().value('maintab/splitterSizes')
            # size is saved as str in some OS
            sizes = [int(size) for size in sizes]
            self.splitter.setSizes(sizes)

    def _initLayout(self) -> None:
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def _initSplitter(self) -> None:
        self.splitter = Splitter()
        self.splitter.setHandleWidth(0)
        self.layout().addWidget(self.splitter)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setChildrenCollapsible(True)

    def _initPlotarea(self) -> None:
        self.plotarea = QWidget()
        self.plotarea.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.splitter.addWidget(self.plotarea)

    def _initSidebar(self) -> None:
        self.sidebar = SideBar()
        self.splitter.addWidget(self.sidebar)

    def _initFiletree(self) -> None:
        self.filetree = FileTreeWidget()
        self.sidebar.addWidget(self.filetree)

    def _initTools(self) -> None:
        self.tools = FoldWidget(QWidget(), 'Tools')
        self.sidebar.addWidget(self.tools)

    def _initMetadata(self) -> None:
        self.metaData = FoldWidget(QWidget(), 'Meta Data')
        self.sidebar.addWidget(self.metaData)

    def closeEvent(self, event):
        QSettings().setValue('maintab/splitterSizes', self.splitter.sizes())

        self.sidebar.closeEvent(event)
        self.filetree.closeEvent(event)
        
        return super().closeEvent(event)
