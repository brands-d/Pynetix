from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QSplitter

from pynetix.other.stylesheet import Style


class Splitter(QSplitter):

    def addWidget(self, widget) -> None:
        out = super().addWidget(widget)
        i = self.count() - 1
        self.handle(i).setMouseTracking(True)
        self.handle(i).installEventFilter(self)
        self.handle(i).setDisabled(True)
  
        return out

    def eventFilter(self, handler, event) -> bool:
        if event.type() == QEvent.Type.Enter:
            handler.setDisabled(False)
            handler.splitter().setStyleSheet(Style.get_style('QSplitter Hover'))
        elif event.type() == QEvent.Type.Leave:
            handler.setDisabled(True)
            handler.splitter().setStyleSheet(Style.get_style('QSplitter Base'))

        return super().eventFilter(handler, event)
