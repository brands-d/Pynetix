from pathlib import Path
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QFileSystemModel, QTreeView
from pynetix.widgets.foldwidget import FoldWidget


class FileTreeWidget(FoldWidget):
    def __init__(self) -> None:
        self.model = None
        self.view = None

        self._init_model()
        self._init_view()

        super().__init__(self.view, 'File Tree')

        if 'path/project_dir' in QSettings().allKeys():
            path = QSettings().value('path/project_dir')
        else:
            pass
        path = Path.home()
        self.change_path(path)

    def change_path(self, path):
        path = str(path)
        self.model.setRootPath(path)
        self.view.setRootIndex(self.model.index(self.model.rootPath()))

    def _init_model(self) -> None:
        self.model = QFileSystemModel()

    def _init_view(self) -> None:
        self.view = QTreeView()
        self.view.setModel(self.model)
        self.view.hideColumn(1)
        self.view.hideColumn(2)
        self.view.hideColumn(3)
        self.view.setHeaderHidden(True)
        
        # root path should be set in settings only
        # self.view.doubleClicked.connect(self._item_double_clicked)

    def closeEvent(self, event) -> None:
        path = self.model.rootPath()
        QSettings().setValue('path/project_dir', path)
        return super().closeEvent(event)
