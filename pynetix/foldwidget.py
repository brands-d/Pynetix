from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QPropertyAnimation, Qt, pyqtSignal, QSettings
from PyQt6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QVBoxLayout,
                             QWidget, QSizePolicy, QTreeView, QApplication)


class FoldWidget(QWidget):
    def __init__(self, widget, label) -> None:
        super().__init__()

        self.bar = None
        self.body = None

        self.folded = False
        self.prev_height = 0
        self.max_height = QApplication.instance().primaryScreen().size().height()

        self._init_layout()
        self._init_bar(label)
        self._init_body(widget)

        self.animation = QPropertyAnimation(self.body, b'maximumHeight')
        self.animation.finished.connect(self._folding_finished)

    def folding(self, folded) -> None:
        if folded:
            # not folded -> folded
            self.folded = True
            self.body.setMinimumHeight(0)
            self.body.setMaximumHeight(self.body.height())
            self.prev_height = self.body.height()
            self.animation.setEndValue(0)
            self.animation.setDuration(self.body.height()/1.5)
        else:
            # folded -> unfolded
            self.folded = False
            self.body.prev_height = 0
            self.animation.setEndValue(self.prev_height)
            self.animation.setDuration(self.prev_height/1.5)

        self.animation.start()

    def _folding_finished(self):
        if not self.folded:
            self.body.setMaximumHeight(16777215)
            self.body.setMinimumHeight(50)

        """if folded:
            self.body.setMaximumHeight(self.body.height())
            self.body.setMinimumHeight(0)
            new_height = 0
            duration = self.body.height()/1.5
        else:
            self.body.setMinimumHeight(50)
            new_height = self.max_height
            duration = self.max_height/1.5

        self.animation.setDuration(duration)
        self.animation.setEndValue(new_height)
        self.animation.start()"""

    def _init_layout(self) -> None:
        self.setLayout(QVBoxLayout())

    def _init_bar(self, label) -> None:
        self.bar = FoldWidgetBar(label)
        self.layout().addWidget(self.bar)

        self.bar.folded.connect(self.folding)

    def _init_body(self, widget) -> None:
        self.body = widget
        self.layout().addWidget(self.body)

        self.body.setMinimumHeight(50)
        self.body.setMaximumHeight(self.max_height)
        self.body.setSizePolicy(QSizePolicy.Policy.Preferred,
                                QSizePolicy.Policy.Expanding)


class FoldWidgetBar(QWidget):
    folded = pyqtSignal(bool)

    def __init__(self, label) -> None:
        super().__init__()

        self.label = None
        self.button = None

        self._init_layout()
        self._init_label(label)
        self._init_button()

    def fold(self) -> None:
        self.button.clicked.disconnect(self.fold)
        self.button.clicked.connect(self.unfold)

        self.folded.emit(True)

    def unfold(self) -> None:
        self.button.clicked.disconnect(self.unfold)
        self.button.clicked.connect(self.fold)

        self.folded.emit(False)

    def _init_layout(self) -> None:
        self.setLayout(QHBoxLayout())

        self.setSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Minimum)

    def _init_label(self, label) -> None:
        self.label = QLabel(label)
        self.layout().addWidget(self.label)

    def _init_button(self) -> None:
        self.button = QPushButton()
        self.layout().insertWidget(0, self.button)

        self.button.clicked.connect(self.fold)


class OldFoldWidgetBar(QWidget):
    fold_changed = pyqtSignal()

    def __init__(self, label='') -> None:
        super().__init__()

        self.is_folded = False

        self.button = None
        self.label = None

        self._init_layout()
        self._init_button()
        self._init_label(label)

    def fold(self) -> None:
        if self.is_folded:
            return

        self.button.setArrowType(Qt.ArrowType.RightArrow)

        self.button.clicked.disconnect(self.fold)
        self.button.clicked.connect(self.unfold)
        self.is_folded = True

    def unfold(self) -> None:
        if not self.is_folded:
            return

        self.button.setArrowType(Qt.ArrowType.DownArrow)

        self.button.clicked.disconnect(self.unfold)
        self.button.clicked.connect(self.fold)
        self.is_folded = False

    def _init_layout(self) -> None:
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def _init_button(self) -> None:
        self.button = QToolButton()
        self.button.setAutoRaise(True)
        arrow = Qt.ArrowType.RightArrow if self.is_folded else Qt.ArrowType.DownArrow
        self.button.setArrowType(arrow)
        self.layout().addWidget(self.button)

        self.button.clicked.connect(self.fold)
        self.button.clicked.connect(self.fold_changed.emit)

    def _init_label(self, label) -> None:
        self.label = QLabel(label)
        self.layout().addWidget(self.label)


class OldFoldWidget(QWidget):
    fold_changed = pyqtSignal()

    def __init__(self, body, label='', animation_duration=5000, folded=False) -> None:
        super().__init__()

        self.is_folded = False

        self.body = None
        self.bar = None

        self._init_layout()
        self._init_bar(label)
        self._init_body(body)

        # animation does not work
        self.animation = QPropertyAnimation(self.body, b'maximumHeight')
        self.animation.setDuration(animation_duration)

        if folded:
            self.fold()

    def fold(self) -> None:
        if self.is_folded:
            return

        self.animation.setEndValue(0)
        self.animation.start()

        self.bar.fold()
        self.bar.fold_changed.disconnect(self.fold)
        self.bar.fold_changed.connect(self.unfold)

        self.is_folded = True

    def unfold(self) -> None:
        if not self.is_folded:
            return

        self.animation.setEndValue(16777215)
        self.animation.start()

        self.bar.unfold()
        self.bar.fold_changed.disconnect(self.unfold)
        self.bar.fold_changed.connect(self.fold)

        self.is_folded = False

    def _init_layout(self) -> None:
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def _init_bar(self, label) -> None:
        self.bar = FoldWidgetBar('   ' + label)
        self.layout().addWidget(self.bar)
        self.bar.fold_changed.connect(self.fold_changed.emit)
        self.bar.fold_changed.connect(self.fold)

    def _init_body(self, body):
        self.body = body
        self.layout().addWidget(self.body)
        self.body.setSizePolicy(QSizePolicy.Policy.Expanding,
                                QSizePolicy.Policy.Expanding)


class TreeWidget(FoldWidget):
    def __init__(self, *args, **kwargs) -> None:
        self.model = QFileSystemModel()
        self.model.setRootPath('/Users/dominik/Desktop/Pynetix')
        # self.model.setRootPath(QSettings().value('paths/project'))
        self.tree = QTreeView()
        self.tree.setModel(self.model)

        super().__init__(self.tree, 'File Explorer', *args, **kwargs)
