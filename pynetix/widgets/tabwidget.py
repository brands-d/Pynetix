from PySide6.QtWidgets import QTabWidget
from PySide6.QtGui import QCloseEvent


class TabWidget(QTabWidget):
    def closeEvent(self, event) -> None:
        for i in range(self.count()):
            self.closeTab(i, event)

        return super().closeEvent(event)

    def closeTab(self, i: int, event: QCloseEvent) -> None:
        tab = self.widget(i)
        event = event if event is not None else QCloseEvent()
        tab.closeEvent(event)

    def removeTab(self, i: int):
        self.closeTab(i, None)
        super().removeTab(i)
