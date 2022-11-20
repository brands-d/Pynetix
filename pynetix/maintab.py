from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QSizePolicy
from PyQt6.QtCore import Qt, QSettings, QVariantAnimation

from pynetix.foldwidget import FoldWidget, TreeWidget


class MainTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName('MainTab')

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
        # layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def _init_splitter(self) -> None:
        self.splitter = QSplitter()
        # self.splitter.setHandleWidth(0)
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
            self.animation.setStartValue(widget.height())
            self.animation.setEndValue(widget.prev_height)

        self.animation.start()

    def _change_sizes(self, value: int) -> None:
        sizes = self.splitter.sizes()
        sizes[self._i] = value
        self.splitter.setSizes(sizes)

    def _size_change_finished(self) -> None:
        widget = self.splitter.widget(self._i)
        if not widget.folded:
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
        # self.splitter.setHandleWidth(0)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setOrientation(Qt.Orientation.Vertical)

        self.layout().addWidget(self.splitter)


"""
class OldSideBar(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.meta_data = None
        self.tools = None
        self.filetree = None
        self.splitter = None
        self.widget_order = []

        self._init_layout()
        self._init_splitter()
        self._init_filetree()
        self._init_tools()
        self._init_metadata()

    def change_fold(self, widget):
        if widget.is_folded:
            index = self.widget_order.index(widget)
            self.splitter.insertWidget(index, widget)
        else:
            self.layout().insertWidget(1, widget)

    def _init_layout(self) -> None:
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def _init_splitter(self) -> None:
        self.splitter = QSplitter()
        self.splitter.setHandleWidth(0)
        self.layout().addWidget(self.splitter)
        self.layout().setStretchFactor(self.splitter, 1)
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.setChildrenCollapsible(False)

    def _init_filetree(self) -> None:
        self.filetree = TreeWidget()
        self.splitter.addWidget(self.filetree)
        self.filetree.fold_changed.connect(
            lambda: self.change_fold(self.filetree))

        self.widget_order.append(self.filetree)

    def _init_tools(self) -> None:
        self.tools = FoldWidget(QWidget(), 'Tools', folded=True)
        self.layout().addWidget(self.tools)
        self.tools.fold_changed.connect(
            lambda: self.change_fold(self.tools))

        self.widget_order.append(self.tools)

    def _init_metadata(self) -> None:
        self.meta_data = FoldWidget(QWidget(), 'Meta Data', folded=True)
        self.layout().addWidget(self.meta_data)
        self.meta_data.fold_changed.connect(
            lambda: self.change_fold(self.meta_data))

        self.widget_order.append(self.meta_data)
"""
