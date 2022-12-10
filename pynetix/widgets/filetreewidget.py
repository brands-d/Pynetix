from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QFileSystemModel, QTreeView

from pynetix.widgets.foldwidget import FoldWidget
from pynetix.other.lib import QBoolToBool, QListToList


class FileTreeWidget(FoldWidget):
    def __init__(self) -> None:
        self.model = None
        self.view = None

        self._initModel()
        self._initView()

        super().__init__(self.view, 'File Tree')

        self.changePath(QSettings().value('path/projectDir'))

    def changePath(self, path) -> None:
        path = Path.home() if path == '~' else Path(path)
        self.model.setRootPath(str(path))
        self.view.setRootIndex(self.model.index(self.model.rootPath()))

    def _itemDoubleClicked(self, index) -> None:
        print(self.model.filePath(index))

    def _initModel(self) -> None:
        self.model = QFileSystemModel()
        self.model.setNameFilters(QListToList(
            QSettings().value('filetree/fileFilter')))
        self.model.setNameFilterDisables(not QBoolToBool(
            QSettings().value('filetree/activateFileFilter')))

    def _initView(self) -> None:
        self.view = QTreeView()
        self.view.setModel(self.model)
        self.view.hideColumn(1)
        self.view.hideColumn(2)
        self.view.hideColumn(3)
        self.view.setHeaderHidden(True)

        self.view.doubleClicked.connect(self._itemDoubleClicked)

    def closeEvent(self, event) -> None:
        QSettings().setValue('filetree/fileFilter', ['*.xlsx'])
        QSettings().setValue('filetree/activateFileFilter',
                             not self.model.nameFilterDisables())
        return super().closeEvent(event)
