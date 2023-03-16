from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QGridLayout
from pyqtgraph import GraphicsLayoutWidget, setConfigOption, PlotItem

from pynetix.resources.resources import Resource


class PlotArea(QWidget):
    plotClicked = Signal(PlotItem)

    def __init__(self) -> None:
        super().__init__()

        self.view = None
        self.plate = None
        self.plots = []

        self._initView()
        self._initLayout()

    def setPlate(self, plate):
        first = self.plate is None
        self.plate = plate
        for row in range(self.plate.dimensions[0]):
            for col in range(self.plate.dimensions[1]):
                if first:
                    self._addPlot(row, col,
                                  last_row=row == self.plate.dimensions[0]-1,
                                  first_col=col == 0)
                self._updatePlot(row, col)

        self.getPlot(0, 0).scene().sigMouseClicked.connect(self._emitPlotEvent)

    def getPlot(self, row: int, col: int):
        return self.view.getItem(row, col)

    def getCoordinates(self, item: PlotItem) -> (int, int):
        i = self.plots.index(item)
        row = i // self.plate.dimensions[1]
        col = i % self.plate.dimensions[1]

        return (row, col)

    def _emitPlotEvent(self, event) -> None:
        if not event.double():
            return

        event.accept()
        scene = self.getPlot(0, 0).scene()
        scene.setClickRadius(0)
        for item in scene.itemsNearEvent(event):
            if isinstance(item, PlotItem):
                self.plotClicked.emit(item)

    def _updatePlot(self, row: int, col: int) -> None:
        reaction = self.plate.reactions[row][col]
        plotItem = self.getPlot(row, col)
        plotItem.clear()
        plotItem.plot(reaction.times, reaction.values, pen={
                      'color': Resource.getColour('BLUE')})

    def _addPlot(self, row: int, col: int, last_row: bool, first_col: bool) -> None:
        item = self.view.addPlot(row, col, enableMenu=False)
        item.showAxes((True, False, False, True), showValues=False)
        self.plots.append(item)

        if last_row:
            item.getAxis('bottom').setStyle(showValues=True)
        if first_col:
            item.getAxis('left').setStyle(showValues=True)

    def _initView(self):
        setConfigOption('background', Resource.getColour('BLACK'))
        setConfigOption('foreground', Resource.getColour('WHITE'))

        self.view = GraphicsLayoutWidget()

    def _initLayout(self):
        layout = QGridLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)
