from PyQt6.QtCore import QPropertyAnimation, Qt, pyqtSignal
from PyQt6.QtWidgets import (QHBoxLayout, QLabel, QToolButton, QVBoxLayout,
                             QWidget, QSizePolicy)


class FoldWidgetBar(QWidget):
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
        layout.setContentsMargins(0,0,0,0)
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


class FoldWidget(QWidget):
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
