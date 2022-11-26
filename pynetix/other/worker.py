from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread


class Task(QThread):
    def __init__(self, f, *args, **kwargs):
        super().__init__()
        self.f = lambda: f(*args, **kwargs)
        self.result = None

    def start(self) -> None:
        QApplication.instance().add_task(self)
        super().start()

    def quit(self) -> None:
        QApplication.instance().remove_task(self)
        super().quit()

    def run(self) -> None:
        self.result = self.f()
