from PyQt6.QtCore import QObject, QThread, pyqtSignal


class BasicWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, f, *args, thread=None, anchor=None, **kwargs) -> None:
        super().__init__()

        self.f = f
        self.args = args
        self.kwargs = kwargs
        if thread is None and anchor is not None:
            self.thread = QThread(parent=anchor)
        elif thread is not None:
            self.thread = thread
        else:
            raise AttributeError(
                'Pass either a thread object or a caller object.')

        self.moveToThread(self.thread)

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
        self.thread.finished.connect(self.thread.deleteLater)
