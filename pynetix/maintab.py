from logging import getLogger

from PySide6.QtCore import QSettings, Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QSizePolicy, QWidget

from pynetix import __project__
from pynetix.models.plate import Plate
from pynetix.widgets.filetreewidget import FileTreeWidget
from pynetix.widgets.foldwidget import FoldWidget
from pynetix.widgets.plotarea import PlotArea
from pynetix.widgets.metadatawidget import MetaDataWidget
from pynetix.widgets.sidebar import SideBar
from pynetix.widgets.splitter import Splitter

from pyqtgraph import PlotItem


class MainTab(QWidget):
    plotClicked = Signal(PlotItem)

    def __init__(self) -> None:
        super().__init__()

        self.plotarea = None
        self.sidebar = None
        self.splitter = None
        self.filetree = None
        self.tools = None
        self.metaData = None
        self.plate = None

        self._initLayout()
        self._initSplitter()
        self._initSidebar()
        self._initFiletree()
        self._initTools()
        self._initMetadata()
        self._initPlotarea()

        self.readSettings()
        self.sidebar.readSettings()

        if QSettings().value('maintab/openFile') is not None:
            self.openFile(QSettings().value('maintab/openFile'))

    def readSettings(self) -> None:
        if 'maintab/splitterSizes' in QSettings().allKeys():
            sizes = QSettings().value('maintab/splitterSizes')
            # size is saved as str in some OS
            sizes = [int(size) for size in sizes]
            self.splitter.setSizes(sizes)

    def settingChanged(self, setting: str, value: str) -> None:
        if setting == 'path/projectDir':
            self.filetree.changePath(value)

    def openFile(self, path):
        try:
            getLogger(__project__).info(f'Opening plate {path}')
            self.plate = Plate(path)
        except:
            getLogger(__project__).error(f'{path} not a valid file.', 20)
        else:
            self.metaData.setPlate(self.plate)
            self.plotarea.setPlate(self.plate)
            getLogger(__project__).info(f'Plate {path} opened successfully.')

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
        self.plotarea = PlotArea()
        self.plotarea.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.splitter.addWidget(self.plotarea)

        self.plotarea.plotClicked.connect(self.plotClicked.emit)

    def _initSidebar(self) -> None:
        self.sidebar = SideBar()
        self.splitter.addWidget(self.sidebar)

    def _initFiletree(self) -> None:
        self.filetree = FileTreeWidget()
        self.filetree.fileRequested.connect(self.openFile)
        self.sidebar.addWidget(self.filetree)

    def _initTools(self) -> None:
        self.tools = FoldWidget(QWidget(), 'Tools')
        self.sidebar.addWidget(self.tools)

    def _initMetadata(self) -> None:
        self.metaData = MetaDataWidget()
        self.sidebar.addWidget(self.metaData)

    def closeEvent(self, event):
        QSettings().setValue('maintab/splitterSizes', self.splitter.sizes())
        if self.plate is not None:
            QSettings().setValue('maintab/openFile', self.plate.filePath)
        else:
            QSettings().setValue('maintab/openFile', None)

        self.sidebar.closeEvent(event)
        self.filetree.closeEvent(event)

        return super().closeEvent(event)
