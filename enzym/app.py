
from importlib import import_module
from logging import getLogger, DEBUG

from PyQt6.QtWidgets import QApplication, QMainWindow, QStatusBar

from enzym.other.logging import StatusBarHandler, ColoredStatusBarFormatter


class App(QApplication):

    def __init__(self, argv=[]) -> None:

        super().__init__(argv)

        colour = 'test'  # should be read from config
        try:
            self.colour = import_module(f'colorschemes.{colour}').Colour
        except:
            raise ValueError(
                f'Colour scheme {colour} not found. Check config files for spelling.')

        self._init_mainwindow()
        self._init_logging()

        self.mainwindow.show()

        getLogger('enzym').info('Initialization finished.')

    def _init_mainwindow(self) -> None:
        self.mainwindow = QMainWindow()
        self.statusBar = QStatusBar()
        self.mainwindow.setStatusBar(self.statusBar)

    def run(self) -> int:
        return super().exec()

    def _init_logging(self) -> None:
        log = getLogger('enzym')
        log.setLevel(DEBUG)
        handler = StatusBarHandler(self.mainwindow.statusBar())
        handler.setFormatter(ColoredStatusBarFormatter(self.colour))
        log.addHandler(handler)
