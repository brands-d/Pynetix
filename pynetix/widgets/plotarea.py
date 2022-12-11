from PySide6.QtWidgets import QWidget, QGridLayout
from pyqtgraph import GraphicsLayoutWidget, setConfigOption

from pynetix.resources.resources import Resource

class PlotArea(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.plots = []
        self.view = None
        self.plate = None

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

    def getPlot(self, row: int, col: int):
        return self.view.getItem(row, col)

    def _updatePlot(self, row: int, col: int) -> None:
        reaction = self.plate.reactions[row][col]
        plotItem = self.getPlot(row, col)
        plotItem.clear()
        plotItem.plot(reaction.times, reaction.values, pen={'color': Resource.getColour('BLUE')})

    def _addPlot(self, row: int, col: int, last_row: bool, first_col: bool) -> None:
        item = self.view.addPlot(row, col, enableMenu=False)
        item.showAxes((True, False, False, True), showValues=False)

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
