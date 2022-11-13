from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, QThread, pyqtSignal


class BasicWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, f, *args, thread=None, **kwargs) -> None:
        super().__init__()

        self.f = f
        self.args = args
        self.kwargs = kwargs
        self.app = QApplication.instance()
        self.thread = QThread(parent=self.app) if thread is None else thread
        self.moveToThread(self.thread)
        self.app.add_task(self)

        self._connect()

    def start(self) -> None:
        self.thread.start()

    def _run(self) -> QThread:
        self.f(*self.args, **self.kwargs)
        self.finished.emit()

    def _connect(self) -> None:
        self.finished.connect(self.thread.quit)
        self.finished.connect(self.deleteLater)

        self.thread.started.connect(self._run)
        self.thread.finished.connect(lambda: self.app.remove_task(self))
