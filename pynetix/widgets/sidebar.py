from PySide6.QtCore import QEasingCurve, QSettings, Qt, QVariantAnimation
from PySide6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget

from pynetix.other.stylesheet import Style
from pynetix.widgets.splitter import Splitter


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
        if self._i == 0 or (self._i == 2 and self.splitter.widget(1).is_folded):
            self.splitter.enabled_handlers[1] = not widget.is_folded
            #self.splitter.handle(1).setEnabled(not widget.is_folded)
        # elif self._i == 2 and self.splitter.widget(1).is_folded:
            #self.splitter.handle(1).setEnabled(not widget.is_folded)
        else:
            self.splitter.enabled_handlers[2] = not widget.is_folded
            #self.splitter.handle(2).setEnabled(not widget.is_folded)

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
        self.setStyleSheet(Style.get_style('SideBar'))

    def read_settings(self) -> None:
        try:
            self.splitter.setSizes(QSettings().value('sidebar/splitter_sizes'))
        except TypeError:
            # this setting is not available
            pass

        """
        # produces weird results for some reason
        folded_widgets = QSettings().value('sidebar/folded_widgets')
        for i in range(self.splitter.count()):
            if folded_widgets[i]:
                self.splitter.widget(i).fold()"""

    def closeEvent(self, event) -> None:
        QSettings().setValue('sidebar/splitter_sizes', self.splitter.sizes())
        folded_widgets = [self.splitter.widget(
            i).is_folded for i in range(self.splitter.count())]
        QSettings().setValue('sidebar/folded_widgets', folded_widgets)

        return super().closeEvent(event)

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
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.setMinimumWidth(100)
        self.setBaseSize(500, 100)
        self.setSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Expanding)

    def _init_splitter(self) -> None:
        self.splitter = Splitter()
        self.splitter.setHandleWidth(0)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setOrientation(Qt.Orientation.Vertical)

        self.layout().addWidget(self.splitter)
