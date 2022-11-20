from PyQt6.QtCore import QEasingCurve, QSettings, Qt, QVariantAnimation
from PyQt6.QtWidgets import (QHBoxLayout, QSizePolicy, QSplitter,
                             QVBoxLayout, QWidget)

from pynetix.foldwidget import FoldWidget
from pynetix.other.stylesheet import Style


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

        self._i = None  # needed to keep track of which widget is collapsing during animation
        self.animation = QVariantAnimation()
        # for some reason QVariantAnimations first value is the what the last value
        # of the previous run should have been -> tiny flickering in the start of
        # the animation. Solution: skip the first loop
        self.first_loop = False
        self.animation.valueChanged.connect(self._change_sizes)
        self.animation.finished.connect(self._size_change_finished)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        self.update_style()

    def addWidget(self, widget: QWidget) -> None:
        self.splitter.addWidget(widget)
        widget.folding.connect(lambda: self.initiate_folding(widget))

    def is_folding_possible(self):
        number_folded_widget = 0
        for i in range(self.splitter.count()):
            number_folded_widget += int(self.splitter.widget(i).is_folded)

        if number_folded_widget >= self.splitter.count() - 1:
            return False
        else:
            return True

    def initiate_folding(self, widget: QWidget) -> None:
        self._i = self.splitter.indexOf(widget)
        if self._i == 0:
            self.splitter.handle(1).setEnabled(not widget.is_folded)
        elif self._i == 2 and self.splitter.widget(1).is_folded:
            self.splitter.handle(1).setEnabled(not widget.is_folded)
        else:
            self.splitter.handle(2).setEnabled(not widget.is_folded)

        # Widget changes it's status first because the signal emits from
        # bar which never actually changes size. Thus if widget thinks it
        # is folded when this function was called it is not yet actually
        # folded. Thus if true, widget is to be folded.
        self.first_loop = True
        if widget.is_folded:
            # Remove the lower bound on the size (FoldWidget keep track of bar size themselves).
            # Save the previous state to get approx. same size on unfold back.
            # Create animation from now to only the bar.
            widget.setMinimumHeight(0)
            widget.prev_height = widget.height()
            self.animation.setStartValue(widget.height())
            self.animation.setEndValue(widget.minimumHeight())
        else:
            # Remove upper bound on height.
            # Start animation from now to previous size.
            widget.setMaximumHeight(1000000)
            self.animation.setStartValue(widget.height())
            self.animation.setEndValue(widget.prev_height)

        self.animation.start()

    def update_style(self) -> None:
        self.setStyleSheet(Style.get_style('sidebar'))

    def _change_sizes(self, value: int) -> None:
        if not self.first_loop:
            sizes = self.splitter.sizes()
            sizes[self._i] = value
            self.splitter.setSizes(sizes)

        self.first_loop = False

    def _size_change_finished(self) -> None:
        widget = self.splitter.widget(self._i)
        self._i = None

        if widget.is_folded:
            # After animation set maximum height to 0.
            # Necessary to ensure moving splitters by hand does
            # not expand the bar. Cannot be done before animation
            # because it would instantly fold the widget.
            widget.setMaximumHeight(0)
        else:
            # Set lower bound on height again. Was removed during
            # folding process. Cannot be done before animation
            # because the widget would instantly unfold up to the
            # lower bound.
            widget.setMinimumHeight(50)

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
