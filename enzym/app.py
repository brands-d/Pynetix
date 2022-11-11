from logging import getLogger, DEBUG

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings
from enzym.mainwindow import MainWindow

from enzym import __project__, __organization__, __directory__
from enzym.other.logging import StatusBarHandler, ColoredStatusBarFormatter
from enzym.other.colours import Colour

class App(QApplication):

    def __init__(self, argv=[]) -> None:
        super().__init__(argv)

        self.setApplicationName(__project__)
        self.setOrganizationName(__organization__)

        self.mainwindow = None

        self.verify_settings()

        Colour.update_colour_scheme(QSettings().value('colours/theme'))
        self._init_mainwindow()
        self._init_logging()

        self.mainwindow.show()

        getLogger('enzym').info('Initialization finished.')

    def _init_mainwindow(self) -> None:
        self.mainwindow = MainWindow()

    def _init_logging(self) -> None:
        log = getLogger('enzym')
        log.setLevel(DEBUG)
        handler = StatusBarHandler(self.mainwindow.statusBar())
        handler.setFormatter(ColoredStatusBarFormatter())
        log.addHandler(handler)

    def update_colours(self) -> None:
        pass

    def verify_settings(self) -> None:
        settings = QSettings()
        defaults = QSettings(str(__directory__ / '..' / 'default_settings.ini'),
                             QSettings.Format.IniFormat)
        defaults.setFallbacksEnabled(False)

        # this way new settings can be introduced easily
        for key in defaults.allKeys():
            if not settings.contains(key):
                settings.setValue(key, defaults.value(key))
