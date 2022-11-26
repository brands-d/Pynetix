from PySide6.QtWidgets import QTabWidget


class TabWidget(QTabWidget):
    def closeEvent(self, event):
        for i in range(self.count()):
            tab = self.widget(i)
            tab.closeEvent(event)

        return super().closeEvent(event)
