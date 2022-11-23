from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                             QVBoxLayout, QWidget, QScrollArea)

from pynetix.other.icons import Icon


class FoldWidget(QWidget):
    folding = pyqtSignal()

    def __init__(self, widget, label) -> None:
        super().__init__()

        self.bar = None
        self.body = None

        self._init_layout()
        self._init_bar(label)
        self._init_body(widget)

        self.prev_height = self.height()

    @property
    def is_folded(self) -> bool:
        return self.bar.is_folded

    def get_sidebar(self):
        return self.parent().parent()

    def fold(self) -> None:
        self.bar.fold()

    def unfold(self) -> None:
        self.bar.unfold()

    @is_folded.setter
    def is_folded(self, folded: bool) -> None:
        self.bar.is_folded = folded

    def setMinimumHeight(self, value: int) -> None:
        super().setMinimumHeight(self.bar.height() + value)
        self.body.setMinimumHeight(value)

    def setMaximumHeight(self, value: int) -> None:
        super().setMaximumHeight(self.bar.height() + value)
        self.body.setMaximumHeight(value)

    def _init_layout(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

    def _init_bar(self, label) -> None:
        self.bar = FoldWidgetBar(label)
        self.layout().addWidget(self.bar)

        self.bar.folding.connect(self.folding.emit)

    def _init_body(self, widget) -> None:
        self.body = widget
        scroll = QScrollArea(self.body)
        self.layout().addWidget(scroll)

        self.body.setMinimumHeight(50)
        self.body.setSizePolicy(QSizePolicy.Policy.Preferred,
                                QSizePolicy.Policy.Expanding)


class FoldWidgetBar(QWidget):
    folding = pyqtSignal()

    def __init__(self, label) -> None:
        super().__init__()

        self.label = None
        self.button = None

        self.is_folded = False

        self._init_layout()
        self._init_label(label)
        self._init_button()

    def get_sidebar(self):
        return self.parent().get_sidebar()

    def fold(self) -> None:
        if not self.get_sidebar().is_folding_possible():
            return

        self.is_folded = True

        self.button.clicked.disconnect(self.fold)
        self.button.clicked.connect(self.unfold)

        self.button.setIcon(Icon.get_icon('Arrow Right'))

        self.folding.emit()

    def unfold(self) -> None:
        self.is_folded = False

        self.button.clicked.disconnect(self.unfold)
        self.button.clicked.connect(self.fold)

        self.button.setIcon(Icon.get_icon('Arrow Down'))

        self.folding.emit()

    def _init_layout(self) -> None:
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Minimum)

    def _init_label(self, label: str) -> None:
        self.label = QLabel('  ' + label)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Minimum)

        self.layout().addWidget(self.label)

    def _init_button(self) -> None:
        self.button = QPushButton()
        self.button.setIcon(Icon.get_icon('Arrow Down'))
        self.button.setSizePolicy(QSizePolicy.Policy.Minimum,
                                  QSizePolicy.Policy.Minimum)
        self.layout().insertWidget(0, self.button)

        self.button.clicked.connect(self.fold)
