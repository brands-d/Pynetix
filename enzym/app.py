from logging import getLogger, DEBUG

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings
from enzym.mainwindow import MainWindow

from enzym.other.colours import Colour
from enzym.other.stylesheet import Style
from enzym import __project__, __organization__, __resources__
from enzym.other.logging import StatusBarHandler, ColoredStatusBarFormatter


class App(QApplication):

    def __init__(self, argv=[]) -> None:
        super().__init__(argv)

        # settings
        self.setApplicationName(__project__)
        self.setOrganizationName(__organization__)
        self.verify_settings()
        self.update_colours()
        self.update_style()

        # declaration of direct children
        self.mainwindow = None

        # init of children
        self._init_mainwindow()
        self._init_logging()

        # finalizations
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

    def verify_settings(self) -> None:
        settings = QSettings()
        defaults = QSettings(str(__resources__ / 'default_settings.ini'),
                             QSettings.Format.IniFormat)
        defaults.setFallbacksEnabled(False)

        # this way new settings can be introduced easily
        for key in defaults.allKeys():
            if not settings.contains(key):
                settings.setValue(key, defaults.value(key))

    def update_colours(self) -> None:
        Colour.update_colour_scheme(QSettings().value('colours/theme'))

    def update_style(self) -> None:
        self.setStyleSheet(Style.get_style('application'))
