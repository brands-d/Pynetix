from logging import getLogger

from PySide6.QtGui import QAction
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QMainWindow, QStatusBar, QVBoxLayout, QWidget, QMenu, QTabBar

from pynetix import __project__
from pynetix.maintab import MainTab
from pynetix.preferencestab import PreferencesTab
from pynetix.widgets.tabwidget import TabWidget


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(__project__)

        self.statusbar = None
        self.tabwidget = None
        self.mainTab = None
        self.layout = None
        self.preferences = None
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
        if isinstance(self.tabwidget.widget(i), PreferencesTab):
            self.preferences = None

        self.tabwidget.removeTab(i)

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

        # hide the close button on first tab to make uncloseable
        if (button := self.tabwidget.tabBar().tabButton(0, QTabBar.ButtonPosition.LeftSide)) is not None:
            button.hide()
        elif (button := self.tabwidget.tabBar().tabButton(0, QTabBar.ButtonPosition.RightSide)) is not None:
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
        updateAction.triggered.connect(self.notImplemented)
        appMenu.addAction(updateAction)
        self.actions.update({'update': updateAction})

        aboutAction = QAction('About Pynetix')
        aboutAction.setMenuRole(QAction.MenuRole.AboutQtRole)
        aboutAction.triggered.connect(self.notImplemented)
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

    def notImplemented(self) -> None:
        getLogger(__project__).warning('Feature not implemented yet. ごめん', 5)

    def openPreferences(self) -> None:
        if self.preferences is None:
            self.preferences = PreferencesTab()
            self.tabwidget.addTab(self.preferences, 'Preferences')

        self.tabwidget.setCurrentWidget(self.preferences)
        self.preferences.settingChanged.connect(self.mainTab.settingChanged)

    def closeEvent(self, event) -> None:
        settings = QSettings()
        settings.setValue('mainwindow/position', self.pos())
        settings.setValue('mainwindow/size', self.size())

        self.tabwidget.closeEvent(event)

        super().closeEvent(event)
