from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QSizePolicy,
                               QVBoxLayout, QWidget)

from pynetix.other.icons import Icon


class FoldWidget(QWidget):
    folding = Signal()

    def __init__(self, widget, label) -> None:
        super().__init__()

        self.bar = None
        self.body = None

        self._initLayout()
        self._initBar(label)
        self._initBody(widget)

        self.prevHeight = self.height()

    @property
    def isFolded(self) -> bool:
        return self.bar.isFolded

    def getSidebar(self):
        return self.parent().parent()

    def fold(self) -> None:
        self.bar.fold()

    def unfold(self) -> None:
        self.bar.unfold()

    @isFolded.setter
    def isFolded(self, folded: bool) -> None:
        self.bar.isFolded = folded

    def setMinimumHeight(self, value: int) -> None:
        super().setMinimumHeight(self.bar.height() + value)
        self.body.setMinimumHeight(value)

    def setMaximumHeight(self, value: int) -> None:
        super().setMaximumHeight(self.bar.height() + value)
        self.body.setMaximumHeight(value)

    def _initLayout(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

    def _initBar(self, label) -> None:
        self.bar = FoldWidgetBar(label)
        self.layout().addWidget(self.bar)

        self.bar.folding.connect(self.folding.emit)

    def _initBody(self, widget) -> None:
        self.body = widget
        #scroll = QScrollArea(self.body)
        self.layout().addWidget(self.body)

        self.body.setMinimumHeight(50)
        self.body.setSizePolicy(QSizePolicy.Policy.Preferred,
                                QSizePolicy.Policy.Expanding)


class FoldWidgetBar(QWidget):
    folding = Signal()

    def __init__(self, label) -> None:
        super().__init__()

        self.label = None
        self.button = None

        self.isFolded = False

        self._initLayout()
        self._initLabel(label)
        self._initButton()

    def getSidebar(self):
        return self.parent().getSidebar()

    def fold(self) -> None:
        if not self.getSidebar().isFoldingPossible():
            return

        self.isFolded = True

        self.button.clicked.disconnect(self.fold)
        self.label.clicked.disconnect(self.fold)
        self.button.clicked.connect(self.unfold)
        self.label.clicked.connect(self.unfold)

        self.button.setIcon(Icon.getIcon('Arrow Right'))

        self.folding.emit()

    def unfold(self) -> None:
        self.isFolded = False

        self.button.clicked.disconnect(self.unfold)
        self.label.clicked.disconnect(self.unfold)
        self.button.clicked.connect(self.fold)
        self.label.clicked.connect(self.fold)

        self.button.setIcon(Icon.getIcon('Arrow Down'))

        self.folding.emit()

    def _initLayout(self) -> None:
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Minimum)

    def _initLabel(self, label: str) -> None:
        self.label = QPushButton('  ' + label)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Minimum)

        self.layout().addWidget(self.label)

        self.label.clicked.connect(self.fold)

    def _initButton(self) -> None:
        self.button = QPushButton()
        self.button.setIcon(Icon.getIcon('Arrow Down'))
        self.button.setSizePolicy(QSizePolicy.Policy.Minimum,
                                  QSizePolicy.Policy.Minimum)
        self.layout().insertWidget(0, self.button)

        self.button.clicked.connect(self.fold)
