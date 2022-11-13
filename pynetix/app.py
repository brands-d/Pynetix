from logging import getLogger, DEBUG

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings
from pynetix.mainwindow import MainWindow

from pynetix.other.colours import Colour
from pynetix.other.stylesheet import Style
#from pynetix.other.worker import BasicWorker
from pynetix import (__project__, __resources__, __remote__, __version__)
from pynetix.other.logging import StatusBarHandler, ColoredStatusBarFormatter


class App(QApplication):

    def __init__(self, argv=[]) -> None:
        super().__init__(argv)

        # settings
        self.setApplicationName(__project__)
        # self.setOrganizationName(__organization__)
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
        getLogger('pynetix').info('Initialization finished.')

        self.check_for_updates()

    def _init_mainwindow(self) -> None:
        self.mainwindow = MainWindow()

    def _init_logging(self) -> None:
        log = getLogger('pynetix')
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

    def check_for_updates(self) -> None:
        # def f():
        #   print('x')
        if QSettings().value('remote/check_update') == 'true':
            getLogger('pynetix').info('Checking for updates...')
            try:
                from urllib import request
                from re import search
                url = 'https://raw.githubusercontent.com/brands-d/Pynetix/main/pynetix/__init__.py'
                for line in request.urlopen(url):
                    line = line.decode('utf-8')
                    if '__version__' in line:
                        newest_version = search("= *'(.*)' *$", line).group(1)
                        if newest_version != __version__:
                            getLogger('pynetix').warning(
                                'Newer version available.')
                        else:
                            getLogger('pynetix').info("You\'re up to date.")
            except Exception:
                getLogger('pynetix').warning('Checking for updates failed.')
        #worker = BasicWorker(f, caller=self)
        # worker.start()
