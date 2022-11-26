from logging import DEBUG, getLogger

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from pynetix import __project__, __resources__, __version__
from pynetix.mainwindow import MainWindow
from pynetix.other.colours import Colour
from pynetix.other.icons import Icon
from pynetix.other.lib import str_to_bool
from pynetix.other.logging import ColoredStatusBarFormatter, StatusBarHandler
from pynetix.other.stylesheet import Style
from pynetix.other.worker import Task


class App(QApplication):

    def __init__(self, argv=[]) -> None:
        super().__init__(argv)

        self.tasks = []

        # settings
        self.setApplicationName(__project__)
        self.setOrganizationName(__project__)
        self.verify_settings()
        self.update_colours()
        self.update_style()
        self._init_icons()

        # declaration of direct children
        self.mainwindow = None

        # init of children
        self._init_mainwindow()

        # finalizations
        self._init_logging()
        self.mainwindow.show()
        getLogger(__project__).info('Initialization finished.')

        self.check_for_updates()

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
        self.setStyleSheet(Style.get_style('Application'))

    def check_for_updates(self) -> None:
        if str_to_bool(QSettings().value('remote/check_update')):
            getLogger(__project__).info('Checking for updates...')
            from re import search
            from urllib import request

            def f():
                try:
                    url = 'https://raw.githubusercontent.com/brands-d/' + \
                        __project__+'/main/'+__project__.lower()+'/__init__.py'
                    for line in request.urlopen(url):
                        line = line.decode('utf-8')
                        if '__version__' in line:
                            newest_version = search(
                                "= *'(.*)' *$", line).group(1)
                            if newest_version != __version__:
                                return 1
                            else:
                                return 0
                except Exception:
                    return -1

            task = Task(f)
            task.finished.connect(self._handle_update_results)
            task.start()

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def _init_icons(self) -> None:
        Icon.update_colours()

    def _init_mainwindow(self) -> None:
        self.mainwindow = MainWindow()

    def _init_logging(self) -> None:
        log = getLogger(__project__)
        log.setLevel(DEBUG)
        handler = StatusBarHandler(self.mainwindow.statusBar())
        handler.setFormatter(ColoredStatusBarFormatter())
        log.addHandler(handler)

    def _handle_update_results(self):
        task = self.sender()
        result = task.result
        task.quit()

        if result == 0:
            getLogger(__project__).info("You\'re up to date.")
        elif result == 1:
            getLogger(__project__).warning('Newer version available.')
        else:
            getLogger(__project__).warning('Checking for updates failed.')
