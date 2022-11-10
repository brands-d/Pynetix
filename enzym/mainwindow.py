from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QMainWindow, QStatusBar


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.statusbar = None

        self._init_statusbar()

        self.read_settings()

    def _init_statusbar(self) -> None:
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

    def read_settings(self) -> None:
        settings = QSettings()
        self.move(settings.value('mainwindow/position'))
        self.resize(settings.value('mainwindow/size'))

    def write_settings(self) -> None:
        settings = QSettings()
        settings.setValue('mainwindow/position', self.pos())
        settings.setValue('mainwindow/size', self.size())

    def closeEvent(self, event) -> None:
        self.write_settings()
        event.accept()
