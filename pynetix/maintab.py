from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtWidgets import QHBoxLayout, QSizePolicy, QWidget

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
        self.meta_data = None

        self._init_layout()
        self._init_splitter()
        self._init_sidebar()
        self._init_filetree()
        self._init_tools()
        self._init_metadata()
        self._init_plotarea()

        self.read_settings()
        self.sidebar.read_settings()

    def read_settings(self) -> None:
        if 'maintab/splitter_sizes' in QSettings().allKeys():
            self.splitter.setSizes(QSettings().value('maintab/splitter_sizes'))

    def _init_layout(self) -> None:
        layout = QHBoxLayout()
        self.setLayout(layout)

    def _init_splitter(self) -> None:
        self.splitter = Splitter()
        self.splitter.setHandleWidth(0)
        self.layout().addWidget(self.splitter)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setChildrenCollapsible(True)

    def _init_plotarea(self) -> None:
        self.plotarea = QWidget()
        self.plotarea.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.splitter.addWidget(self.plotarea)

    def _init_sidebar(self) -> None:
        self.sidebar = SideBar()
        self.splitter.addWidget(self.sidebar)

    def _init_filetree(self) -> None:
        self.filetree = FoldWidget(QWidget(), 'File Explorer')
        self.sidebar.addWidget(self.filetree)

    def _init_tools(self) -> None:
        self.tools = FoldWidget(QWidget(), 'Tools')
        self.sidebar.addWidget(self.tools)

    def _init_metadata(self) -> None:
        self.meta_data = FoldWidget(QWidget(), 'Meta Data')
        self.sidebar.addWidget(self.meta_data)

    def closeEvent(self, event):
        QSettings().setValue('maintab/splitter_sizes', self.splitter.sizes())

        self.sidebar.closeEvent(event)

        return super().closeEvent(event)
