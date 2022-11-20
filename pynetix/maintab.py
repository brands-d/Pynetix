from PyQt6.QtCore import Qt, QSettings, QVariantAnimation
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QSizePolicy, QSpacerItem


from pynetix.foldwidget import FoldWidget


class MainTab(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.plotarea = None
        self.sidebar = None
        self.splitter = None
        self.filetree = None
        self.tools = None
        self.meta_data = None

        self._init_layout()
        self._init_splitter()
        self._init_sidebar()
        self._init_filetree()
        self._init_tools()
        self._init_metadata()
        self._init_plotarea()

        self.read_settings()

    def read_settings(self) -> None:
        if 'maintab/splitter_sizes' in QSettings().allKeys():
            self.splitter.setSizes(QSettings().value('maintab/splitter_sizes'))

    def _init_layout(self) -> None:
        layout = QHBoxLayout()
        self.setLayout(layout)

    def _init_splitter(self) -> None:
        self.splitter = QSplitter()
        self.splitter.setHandleWidth(0)
        self.layout().addWidget(self.splitter)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setChildrenCollapsible(True)

    def _init_plotarea(self) -> None:
        self.plotarea = QWidget()
        self.plotarea.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.splitter.addWidget(self.plotarea)

    def _init_sidebar(self) -> None:
        self.sidebar = SideBar()
        self.splitter.addWidget(self.sidebar)

    def _init_filetree(self) -> None:
        self.filetree = FoldWidget(QWidget(), 'File Explorer')
        self.sidebar.addWidget(self.filetree)

    def _init_tools(self) -> None:
        self.tools = FoldWidget(QWidget(), 'Tools')
        self.sidebar.addWidget(self.tools)

    def _init_metadata(self) -> None:
        self.meta_data = FoldWidget(QWidget(), 'Meta Data')
        self.sidebar.addWidget(self.meta_data)

    def closeEvent(self, event):
        QSettings().setValue('maintab/splitter_sizes', self.splitter.sizes())

        return super().closeEvent(event)


class SideBar(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.splitter = None
        self._init_layout()
        self._init_splitter()

        self._i = None  # which widget is changing
        self.animation = QVariantAnimation(valueChanged=self._change_sizes)
        self.animation.finished.connect(self._size_change_finished)

    def addWidget(self, widget: QWidget) -> None:
        self.splitter.addWidget(widget)
        widget.folding.connect(lambda: self.initiate_folding(widget))

    def initiate_folding(self, widget: QWidget) -> None:
        self._i = self.splitter.indexOf(widget)

        if widget.folded:
            # widget "wants" to fold but is unfolded
            widget.setMinimumHeight(0)
            widget.prev_height = widget.height()
            self.animation.setStartValue(widget.height())
            self.animation.setEndValue(widget.bar.height())
        else:
            widget.setMaximumHeight(1000000)
            self.animation.setStartValue(widget.height())
            self.animation.setEndValue(widget.prev_height)

        if self._i == 0:
            self.splitter.handle(1).setEnabled(not widget.folded)
        elif self._i == 2 and self.splitter.widget(1).folded:
            self.splitter.handle(1).setEnabled(not widget.folded)
        else:
            self.splitter.handle(2).setEnabled(not widget.folded)

        self.animation.start()

    def _change_sizes(self, value: int) -> None:
        sizes = self.splitter.sizes()
        sizes[self._i] = value
        self.splitter.setSizes(sizes)

    def _size_change_finished(self) -> None:
        widget = self.splitter.widget(self._i)
        if widget.folded:
            widget.setMaximumHeight(0)
        else:
            widget.setMinimumHeight(50)
        self._i = None

    def _init_layout(self) -> None:
        self.setLayout(QVBoxLayout())

        self.setMinimumWidth(100)
        self.setBaseSize(500, 100)
        self.setSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Expanding)

    def _init_splitter(self) -> None:
        self.splitter = QSplitter()
        self.splitter.setHandleWidth(0)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setOrientation(Qt.Orientation.Vertical)

        self.layout().addWidget(self.splitter)
