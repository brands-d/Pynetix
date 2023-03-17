from PySide6.QtWidgets import QWidget, QGridLayout
from pyqtgraph import (ScatterPlotItem, PlotWidget,
                       setConfigOption, PlotItem, mkBrush,
                       InfiniteLine, TextItem)
from numpy import arctan2, rad2deg, zeros

from pynetix.resources.resources import Resource
from pynetix.other.lib import closestValue


class PlotTab(QWidget):
    def __init__(self, plotItem: PlotItem) -> None:

        super().__init__()

        self.origPlotItem = plotItem
        self.plotItem = None
        self.data = self.origPlotItem.listDataItems()[0].getData()
        self.dynamicSlope = None
        self.staticSlope = None
        self.plot = None
        self.dynamicHoverLine = None
        self.staticHoverLine = None
        self.angles = None
        self.slopes = None

        self._initPlot(plotItem)
        self._initStaticSlopeDisplay()
        self._initDynamicSlopeDisplay()
        self._initLayout()
        self.calcAngles()

    def hoverEvent(self, item, points, event):
        try:
            xMouse = event.pos().x()
        except AttributeError:
            return

        index = closestValue(xMouse, self.data[0])

        if self.dynamicHoverLine is None:
            self._initDynamicHoverLine()

        self.dynamicHoverLine.setValue(
            (self.data[0][index], self.data[1][index]))
        self.dynamicHoverLine.setAngle(self.angles[index])
        self.dynamicSlope.setText(
            f'Dynamic Slope: {self.slopes[index]:.3e}')

    def clickEvent(self, event):
        view = self.plotItem.getViewBox()
        xMouse = view.mapSceneToView(event.scenePos()).x()
        index = closestValue(xMouse, self.data[0])

        if self.staticHoverLine is None:
            self._initStaticHoverLine()

        self.staticHoverLine.setValue(
            (self.data[0][index], self.data[1][index]))
        self.staticHoverLine.setAngle(self.angles[index])
        self.staticSlope.setText(
            f'Static Slope: {self.slopes[index]:.3e}')

    def calcAngles(self, width=3):
        x, y = self.data
        delta_x = x[width*2]-x[0]  # equidistant
        delta_y = y[width*2:]-y[:-width*2]

        self.slopes = zeros(x.shape)
        self.slopes[width:-width] = delta_y/delta_x

        angles = rad2deg(arctan2(delta_y, delta_x))
        self.angles = zeros(x.shape)
        self.angles[width:-width] = angles

    def _initPlot(self, plotItem: PlotItem):
        setConfigOption('background', Resource.getColour('BLACK'))
        setConfigOption('foreground', Resource.getColour('WHITE'))

        self.plot = PlotWidget()
        pen = {'color': Resource.getColour('BLUE')}
        brush = mkBrush(Resource.getColour('BLUE'))
        self.plotItem = ScatterPlotItem(*self.data,
                                        pen=pen,
                                        brush=brush,
                                        hoverable=True,
                                        symbol='x',
                                        size=8)
        self.plot.addItem(self.plotItem)
        self.plotItem.sigHovered.connect(self.hoverEvent)
        self.plotItem.scene().sigMouseClicked.connect(self.clickEvent)

    def _initDynamicHoverLine(self):
        pen = {'color': Resource.getColour('ORANGE')+'b3', 'width': 3}
        self.dynamicHoverLine = InfiniteLine(movable=False,
                                             pen=pen)
        self.plot.addItem(self.dynamicHoverLine)

    def _initStaticHoverLine(self):
        pen = {'color': Resource.getColour('RED'), 'width': 3}
        self.staticHoverLine = InfiniteLine(movable=False,
                                            pen=pen)
        self.plot.addItem(self.staticHoverLine)

    def _initDynamicSlopeDisplay(self):
        self.dynamicSlope = TextItem('Dynamic Slope: ',
                                     color=Resource.getColour('ORANGE'))
        self.dynamicSlope.setPos(0.8*max(self.data[0]), 0.9*max(self.data[1]))
        self.plot.addItem(self.dynamicSlope)

    def _initStaticSlopeDisplay(self):
        self.staticSlope = TextItem(' Static Slope: ',
                                    color=Resource.getColour('RED'))
        self.staticSlope.setPos(0.8*max(self.data[0]), 0.85*max(self.data[1]))
        self.plot.addItem(self.staticSlope)

    def _initLayout(self):
        layout = QGridLayout()
        layout.addWidget(self.plot)
        self.setLayout(layout)

    def closeEvent(self, event):
        return super().closeEvent(event)
