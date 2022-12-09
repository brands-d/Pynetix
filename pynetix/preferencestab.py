from logging import getLogger
from os import path
from pathlib import Path

from PySide6.QtCore import QSettings, Qt, Signal
from PySide6.QtWidgets import (QCheckBox, QComboBox, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QSizePolicy,
                               QSpacerItem, QVBoxLayout, QWidget, QFileDialog)

from pynetix import __project__
from pynetix.resources.resources import Resource
from pynetix.other.lib import QBoolToBool
from pynetix.widgets.splitter import Splitter


class PreferencesTab(QWidget):
    settingChanged = Signal(str, str)

    settings = {'update': {'name': 'checkUpdate',
                           'group': 'remote',
                           'type': 'checkbox',
                           'short': 'Check for Updates',
                           'long': 'If internet connection is available, Pynetix tries to check online if a newer version is available. Result is displayed in the Statusbar.'},
                'project': {'name': 'projectDir',
                            'group': 'path',
                            'type': 'path',
                            'short': 'Project Path',
                            'long': 'Root Path of your current Project folder. Base directory of the File Tree.'},
                'theme': {'name': 'theme',
                          'group': 'colour',
                          'type': 'combobox',
                          'options': None,
                          'short': 'Colour Theme',
                          'long': 'Colour Theme of the Application.'}}

    def __init__(self) -> None:
        super().__init__()

        self.sidebar = None
        self.splitter = None

        self._initLayout()
        self._initSplitter()
        self._initSidebar()
        self._initSettings()

    def _initLayout(self) -> None:
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def _initSplitter(self) -> None:
        self.splitter = Splitter()
        self.splitter.setHandleWidth(0)
        self.layout().addWidget(self.splitter)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setChildrenCollapsible(False)

    def _initSidebar(self) -> None:
        pass

    def _initSettings(self) -> None:
        self.settings = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.settings.setLayout(layout)

        setting = CheckBoxSetting(PreferencesTab.settings['update'])
        setting.changed.connect(self.settingChanged.emit)
        layout.addWidget(setting)
        setting = ThemeSetting(PreferencesTab.settings['theme'])
        setting.changed.connect(self.settingChanged.emit)
        layout.addWidget(setting)
        setting = PathSetting(PreferencesTab.settings['project'])
        setting.changed.connect(self.settingChanged.emit)
        layout.addWidget(setting)

        layout.addSpacerItem(QSpacerItem(0, 0,
                                         QSizePolicy.Policy.Minimum,
                                         QSizePolicy.Policy.Expanding))
        self.splitter.addWidget(self.settings)

    def closeEvent(self, event):
        return super().closeEvent(event)


class Setting(QWidget):
    changed = Signal(str, str)

    def __init__(self, info) -> None:
        self.info = info
        self.title = None

        super().__init__()

    def readSetting(self):
        return QSettings().value(self.info['group'] + '/' + self.info['name'])

    def writeSetting(self, value):
        setting = self.info['group'] + '/' + self.info['name']
        getLogger(__project__).info(
            f'Saved preference for "{setting}" as "{value}".')
        QSettings().setValue(setting, value)
        self.changed.emit(setting, value)

    def _initLayout(self, layout) -> None:
        self.setLayout(layout)
        layout.setSpacing(0)
        layout.setContentsMargins(20, 20, 0, 20)
        self.setSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Minimum)

    def _initTitle(self) -> None:
        self.title = QLabel(self.info['short'])
        self.title.setProperty('class', 'Subtitle')
        self.layout().addWidget(self.title)

    def _initDescription(self) -> None:
        self.description = QLabel(self.info['long'])
        self.layout().addWidget(self.description)


class CheckBoxSetting(Setting):
    def __init__(self, info) -> None:
        super().__init__(info)

        self.checkbox = None

        self._initLayout()
        self._initTitle()
        self._initCheckbox()

    def readSetting(self) -> bool:
        return QBoolToBool(super().readSetting())

    def writeSetting(self, value) -> None:
        super().writeSetting(value == 2)

    def _initLayout(self) -> None:
        super()._initLayout(QVBoxLayout())

    def _initCheckbox(self) -> None:
        self.checkbox = QCheckBox(self.info['long'])
        self.checkbox.setChecked(self.readSetting())
        self.checkbox.stateChanged.connect(self.writeSetting)

        self.layout().addWidget(self.checkbox)


class ComboBoxSetting(Setting):
    def __init__(self, info) -> None:
        super().__init__(info)

        self.description = None
        self.comboBox = None

        self._initLayout()
        self._initTitle()
        self._initDescription()
        self._initComboBox()

    def writeSetting(self, *args):
        return super().writeSetting(self.comboBox.currentText())

    def _initLayout(self) -> None:
        super()._initLayout(QVBoxLayout())

    def _initComboBox(self) -> None:
        self.comboBox = QComboBox()
        self.comboBox.setMinimumContentsLength(25)
        self.comboBox.setStyleSheet(
            f'QComboBox::down-arrow{{ image: url({Resource.getIconPath("Arrow Down")}); }}')
        for i, value in enumerate(self.info['options']):
            self.comboBox.addItem(value)
            if value == self.readSetting():
                self.comboBox.setCurrentIndex(i)

        self.comboBox.currentIndexChanged.connect(self.writeSetting)

        layout = QHBoxLayout()
        layout.addWidget(self.comboBox)
        layout.addSpacerItem(QSpacerItem(0, 0,
                                         QSizePolicy.Policy.Expanding,
                                         QSizePolicy.Policy.Minimum))
        self.layout().addLayout(layout)


class ThemeSetting(ComboBoxSetting):

    def _initComboBox(self) -> None:
        self.info['options'] = Resource.listThemes()
        super()._initComboBox()


class PathSetting(Setting):
    def __init__(self, info) -> None:
        super().__init__(info)

        self.lineEdit = None
        self.button = None

        self._initLayout()
        self._initTitle()
        self._initDescription()
        self._initLineEdit()

    def writeSetting(self, value) -> None:
        dir_ = Path(value)
        if path.exists(dir_):
            super().writeSetting(str(dir_))

    def _fileDialog(self) -> None:
        dir_ = QFileDialog.getExistingDirectory(
            None, 'Open Project Directory', self.readSetting(), QFileDialog.Option.ShowDirsOnly)
        if dir_:
            self.lineEdit.setText(dir_)

    def _initLayout(self) -> None:
        super()._initLayout(QVBoxLayout())

    def _initLineEdit(self) -> None:

        self.lineEdit = QLineEdit()
        self.lineEdit.setText(self.readSetting())
        self.lineEdit.textChanged.connect(self.writeSetting)
        self.button = QPushButton(' ... ')
        self.button.clicked.connect(self._fileDialog)
        layout = QHBoxLayout()
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.button)
        layout.addSpacerItem(QSpacerItem(0, 0,
                                         QSizePolicy.Policy.Expanding,
                                         QSizePolicy.Policy.Minimum))
        self.layout().addLayout(layout)
