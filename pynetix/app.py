from logging import DEBUG, getLogger

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from pynetix import __project__, __resources__, __version__
from pynetix.mainwindow import MainWindow
from pynetix.other.colours import Colour
from pynetix.other.icons import Icon
from pynetix.other.lib import QBoolToBool
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
        self.verifySettings()
        self.updateColours()
        self.updateStyle()
        self._initIcons()

        # declaration of direct children
        self.mainwindow = None

        # init of children
        self._initMainwindow()

        # finalizations
        self._initLogging()
        self.mainwindow.show()
        getLogger(__project__).info('Initialization finished.')

        self.checkForUpdates()

    def verifySettings(self) -> None:
        settings = QSettings()
        defaults = QSettings(str(__resources__ / 'default_settings.ini'),
                             QSettings.Format.IniFormat)
        defaults.setFallbacksEnabled(False)

        # this way new settings can be introduced easily
        for key in defaults.allKeys():
            if not settings.contains(key):
                settings.setValue(key, defaults.value(key))

    def updateColours(self) -> None:
        theme = QSettings().value('colour/theme')
        try:
            Colour.updateColourScheme(theme)
        except ValueError:
            print(
                f'Chosen theme "{theme}" does not exist. Fallback to "default".')
            Colour.updateColourScheme('default')
            QSettings().setValue('colour/theme', 'default')

    def updateStyle(self) -> None:
        self.setStyleSheet(Style.getStyle('Application'))

    def checkForUpdates(self) -> None:
        if QBoolToBool(QSettings().value('remote/checkUpdate')):
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
                            newestVersion = search(
                                "= *'(.*)' *$", line).group(1)
                            if newestVersion != __version__:
                                return 1
                            else:
                                return 0
                except Exception:
                    return -1

            task = Task(f)
            task.finished.connect(self._handleUpdateResults)
            task.start()

    def addTask(self, task):
        self.tasks.append(task)

    def removeTask(self, task):
        self.tasks.remove(task)

    def _initIcons(self) -> None:
        Icon.updateColours()

    def _initMainwindow(self) -> None:
        self.mainwindow = MainWindow()

    def _initLogging(self) -> None:
        log = getLogger(__project__)
        log.setLevel(DEBUG)
        handler = StatusBarHandler(self.mainwindow.statusBar())
        handler.setFormatter(ColoredStatusBarFormatter())
        log.addHandler(handler)

    def _handleUpdateResults(self):
        task = self.sender()
        result = task.result
        task.quit()

        if result == 0:
            getLogger(__project__).info("You\'re up to date.")
        elif result == 1:
            getLogger(__project__).warning('Newer version available.')
        else:
            getLogger(__project__).warning('Checking for updates failed.')
