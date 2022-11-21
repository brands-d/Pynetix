from PyQt6.QtCore import QEvent, QTimer
from PyQt6.QtWidgets import QSplitter

from pynetix.other.stylesheet import Style


class Splitter(QSplitter):
    def __init__(self, *args, **kwargs) -> None:
        self.mouse_on = None  # keeps track if mouse still on handler

        return super().__init__(*args, **kwargs)

    def addWidget(self, widget) -> None:
        out = super().addWidget(widget)
        i = self.count() - 1
        self.handle(i).setMouseTracking(True)
        self.handle(i).installEventFilter(self)
        self.handle(i).setDisabled(True)

        return out

    def eventFilter(self, handler, event) -> bool:
        if event.type() == QEvent.Type.Enter:
            self.mouse_on = handler
            handler.setDisabled(False)
            QTimer.singleShot(250, lambda: self.hovering(handler))
        elif event.type() == QEvent.Type.Leave:
            self.mouse_on = None
            handler.setDisabled(True)
            handler.splitter().setStyleSheet(Style.get_style('QSplitter Base'))

        return super().eventFilter(handler, event)

    def hovering(self, handler):
        if self.mouse_on is not None:
            handler.splitter().setStyleSheet(Style.get_style('QSplitter Hover'))
