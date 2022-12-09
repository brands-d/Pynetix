from PySide6.QtCore import QEasingCurve, QSettings, Qt, QVariantAnimation
from PySide6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget

from pynetix.resources.resources import Resource
from pynetix.widgets.splitter import Splitter


class SideBar(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.splitter = None

        self._initLayout()
        self._initSplitter()

        self._i = None  # needed to keep track of which widget is collapsing during animation
        self.animation = QVariantAnimation()
        # for some reason QVariantAnimations first value is the what the last value
        # of the previous run should have been -> tiny flickering in the start of
        # the animation. Solution: skip the first loop
        self.firstLoop = False
        self.animation.valueChanged.connect(self._changeSizes)
        self.animation.finished.connect(self._sizeChangeFinished)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def addWidget(self, widget: QWidget) -> None:
        self.splitter.addWidget(widget)
        widget.folding.connect(lambda: self.initiateFolding(widget))

    def isFoldingPossible(self):
        numberFoldedWidget = 0
        for i in range(self.splitter.count()):
            numberFoldedWidget += int(self.splitter.widget(i).isFolded)

        if numberFoldedWidget >= self.splitter.count() - 1:
            return False
        else:
            return True

    def initiateFolding(self, widget: QWidget) -> None:
        self._i = self.splitter.indexOf(widget)
        if self._i == 0 or (self._i == 2 and self.splitter.widget(1).isFolded):
            self.splitter.enabledHandlers[1] = not widget.isFolded

        else:
            self.splitter.enabledHandlers[2] = not widget.isFolded

        # Widget changes it's status first because the signal emits from
        # bar which never actually changes size. Thus if widget thinks it
        # is folded when this function was called it is not yet actually
        # folded. Thus if true, widget is to be folded.
        self.firstLoop = True
        if widget.isFolded:
            # Remove the lower bound on the size (FoldWidget keep track of bar size themselves).
            # Save the previous state to get approx. same size on unfold back.
            # Create animation from now to only the bar.
            widget.setMinimumHeight(0)
            widget.prevHeight = widget.height()
            self.animation.setStartValue(widget.height())
            self.animation.setEndValue(widget.minimumHeight())
        else:
            # Remove upper bound on height.
            # Start animation from now to previous size.
            widget.setMaximumHeight(1000000)
            self.animation.setStartValue(widget.height())
            self.animation.setEndValue(widget.prevHeight)

        self.animation.start()

    def readSettings(self) -> None:
        try:
            self.splitter.setSizes(QSettings().value('sidebar/splitterSizes'))
        except TypeError:
            # this setting is not available
            pass

        """
        # produces weird results for some reason
        foldedWidgets = QSettings().value('sidebar/foldedWidgets')
        for i in range(self.splitter.count()):
            if foldedWidgets[i]:
                self.splitter.widget(i).fold()"""

    def closeEvent(self, event) -> None:
        QSettings().setValue('sidebar/splitterSizes', self.splitter.sizes())
        foldedWidgets = [self.splitter.widget(
            i).isFolded for i in range(self.splitter.count())]
        QSettings().setValue('sidebar/foldedWidgets', foldedWidgets)

        return super().closeEvent(event)

    def _changeSizes(self, value: int) -> None:
        if not self.firstLoop:
            sizes = self.splitter.sizes()
            sizes[self._i] = value
            self.splitter.setSizes(sizes)

        self.firstLoop = False

    def _sizeChangeFinished(self) -> None:
        widget = self.splitter.widget(self._i)
        self._i = None

        if widget.isFolded:
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

    def _initLayout(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.setMinimumWidth(100)
        self.setBaseSize(500, 100)
        self.setSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Expanding)

    def _initSplitter(self) -> None:
        self.splitter = Splitter()
        self.splitter.setHandleWidth(0)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setOrientation(Qt.Orientation.Vertical)

        self.layout().addWidget(self.splitter)
