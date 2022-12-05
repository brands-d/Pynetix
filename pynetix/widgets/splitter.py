from PySide6.QtCore import QEvent, QTimer
from PySide6.QtWidgets import QSplitter

from pynetix.other.stylesheet import Style


class Splitter(QSplitter):
    def __init__(self, *args, **kwargs) -> None:
        self.mouseOn = None  # keeps track if mouse still on handler
        # bool list of handlers user is able to use.
        # handle.isEnabled not usable because property is needed for styling
        self.enabledHandlers = []

        return super().__init__(*args, **kwargs)

    def addWidget(self, widget) -> None:
        out = super().addWidget(widget)
        i = self.count() - 1
        self.enabledHandlers.append(True)
        self.handle(i).setMouseTracking(True)
        self.handle(i).installEventFilter(self)
        self.handle(i).setDisabled(True)

        return out

    def eventFilter(self, handler, event) -> bool:
        if event.type() == QEvent.Type.Enter:
            # changes style of handler mouse hovers over if handler is enabled
            i = self.getHandlerIndex(handler)
            if self.enabledHandlers[i]:
                self.mouseOn = handler
                handler.setDisabled(False)
                QTimer.singleShot(250, lambda: self.hovering(handler))
        elif event.type() == QEvent.Type.Leave:
            self.mouseOn = None
            handler.setDisabled(True)
            handler.splitter().setStyleSheet(Style.getStyle('QSplitter Base'))

        return super().eventFilter(handler, event)

    def hovering(self, handler):
        if self.mouseOn is not None:
            handler.splitter().setStyleSheet(Style.getStyle('QSplitter Hover'))

    def getHandlerIndex(self, handler):
        for i in range(self.count()):
            if self.handle(i) == handler:
                return i

        raise IndexError
