from PySide6.QtGui import QAction
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import (QMainWindow, QStatusBar, QVBoxLayout,
                               QMessageBox, QWidget, QMenu, QTabBar,
                               QApplication)

from pyqtgraph import PlotItem

from pynetix import __project__
from pynetix.resources.resources import Resource
from pynetix.maintab import MainTab
from pynetix.preferencestab import PreferencesTab
from pynetix.widgets.tabwidget import TabWidget
from pynetix.plottab import PlotTab


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(__project__)

        self.statusbar = None
        self.tabwidget = None
        self.mainTab = None
        self.layout = None
        self.preferences = None
        self.plotTabs = []
        self.actions = {}

        self._initLayout()
        self._initCentralWidget()
        self._initStatusbar()
        self._initTabwidget()
        self._initMenu()

        self.readSettings()

    def readSettings(self) -> None:
        settings = QSettings()
        self.move(settings.value('mainwindow/position'))
        self.resize(settings.value('mainwindow/size'))

    def removeTab(self, i: int) -> None:
        tab = self.tabwidget.widget(i)
        if isinstance(tab, PreferencesTab):
            self.preferences = None

        elif isinstance(tab, PlotTab):
            self.plotTabs.remove(tab)

        self.tabwidget.removeTab(i)

    def openAbout(self) -> None:
        text = Resource.getText('about')
        QMessageBox().about(None, 'Pynetix', text)

    def openPreferences(self) -> None:
        if self.preferences is None:
            self.preferences = PreferencesTab()
            self.tabwidget.addTab(self.preferences, 'Preferences')

        self.tabwidget.setCurrentWidget(self.preferences)
        self.preferences.settingChanged.connect(self.mainTab.settingChanged)

    def openPlot(self, plotItem: PlotItem) -> None:
        plotAlreadyOpen = False
        for plotTab in self.plotTabs:
            if plotTab.origPlotItem == plotItem:
                plotAlreadyOpen = True
                break

        if not plotAlreadyOpen:
            plotTab = PlotTab(plotItem)
            pos = self.mainTab.plotarea.getCoordinates(plotItem)
            title = f'Row: {pos[0] + 1:d}, Col: {pos[1] + 1:d}'
            self.tabwidget.addTab(plotTab, title)
            self.plotTabs.append(plotTab)

        self.tabwidget.setCurrentWidget(plotTab)

    def _initLayout(self) -> None:
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

    def _initStatusbar(self) -> None:
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

    def _initTabwidget(self) -> None:
        self.tabwidget = TabWidget()
        self.mainTab = MainTab()
        self.tabwidget.setTabsClosable(True)
        self.tabwidget.tabBar().tabCloseRequested.connect(self.removeTab)
        self.tabwidget.addTab(self.mainTab, 'Main Tab')

        self.mainTab.plotClicked.connect(self.openPlot)

        # hide the close button on first tab to make uncloseable
        bar = self.tabwidget.tabBar()
        left = bar.tabButton(0, QTabBar.ButtonPosition.LeftSide)
        right = bar.tabButton(0, QTabBar.ButtonPosition.RightSide)
        if (button := left) is not None:
            button.hide()
        elif (button := right) is not None:
            button.hide()

        self.layout.addWidget(self.tabwidget)

    def _initCentralWidget(self) -> None:
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(self.layout)

    def _initMenu(self) -> None:
        appMenu = QMenu('Pynetix')
        fileMenu = QMenu('File')
        helpMenu = QMenu('Help')

        updateAction = QAction('Check for Updates...')
        updateAction.setMenuRole(QAction.MenuRole.ApplicationSpecificRole)
        updateAction.triggered.connect(QApplication.instance().checkForUpdates)
        appMenu.addAction(updateAction)
        self.actions.update({'update': updateAction})

        aboutAction = QAction('About Pynetix')
        aboutAction.setMenuRole(QAction.MenuRole.AboutQtRole)
        aboutAction.triggered.connect(self.openAbout)
        appMenu.addAction(aboutAction)
        self.actions.update({'about': aboutAction})

        preferencesAction = QAction('About Pynetix')
        preferencesAction.setMenuRole(QAction.MenuRole.PreferencesRole)
        preferencesAction.triggered.connect(self.openPreferences)
        appMenu.addAction(preferencesAction)
        self.actions.update({'preferences': preferencesAction})

        self.menuBar().addMenu(appMenu)
        self.menuBar().addMenu(fileMenu)
        self.menuBar().addMenu(helpMenu)

    def closeEvent(self, event) -> None:
        settings = QSettings()
        settings.setValue('mainwindow/position', self.pos())
        settings.setValue('mainwindow/size', self.size())

        self.tabwidget.closeEvent(event)

        super().closeEvent(event)
