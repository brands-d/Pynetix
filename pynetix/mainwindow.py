from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QMainWindow, QStatusBar, QVBoxLayout, QWidget

from pynetix import __project__
from pynetix.maintab import MainTab
from pynetix.widgets.tabwidget import TabWidget


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(__project__)

        self.statusbar = None
        self.tabwidget = None
        self.layout = None

        self._init_layout()
        self._init_central_widget()
        self._init_statusbar()
        self._init_tabwidget()

        self.read_settings()

    def read_settings(self) -> None:
        settings = QSettings()
        self.move(settings.value('mainwindow/position'))
        self.resize(settings.value('mainwindow/size'))

    def _init_layout(self) -> None:
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

    def _init_statusbar(self) -> None:
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

    def _init_tabwidget(self) -> None:
        self.tabwidget = TabWidget()
        self.tabwidget.addTab(MainTab(), 'Main Tab')

        self.layout.addWidget(self.tabwidget)

    def _init_central_widget(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(self.layout)

    def closeEvent(self, event) -> None:
        settings = QSettings()
        settings.setValue('mainwindow/position', self.pos())
        settings.setValue('mainwindow/size', self.size())

        self.tabwidget.closeEvent(event)

        super().closeEvent(event)
