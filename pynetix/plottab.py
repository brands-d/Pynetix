from PySide6.QtWidgets import QWidget, QGridLayout
from pyqtgraph import PlotWidget, setConfigOption, PlotItem

from pynetix import __project__
from pynetix.resources.resources import Resource


class PlotTab(QWidget):
    def __init__(self, plotItem: PlotItem) -> None:

        super().__init__()

        self.plotItem = plotItem
        self.view = None

        self._initView()
        self._initLayout()
        self.plotData(plotItem.listDataItems()[0].getData())

    def plotData(self, data) -> None:
        self.view.plot(*data,
                       pen={'color': Resource.getColour('BLUE'),
                            'width': 3},
                       enableMenu=False)

    def _initView(self):
        setConfigOption('background', Resource.getColour('BLACK'))
        setConfigOption('foreground', Resource.getColour('WHITE'))

        self.view = PlotWidget()

    def _initLayout(self):
        layout = QGridLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def closeEvent(self, event):
        return super().closeEvent(event)
