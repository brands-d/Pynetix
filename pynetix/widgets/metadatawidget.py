from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QSizePolicy, QLayout

from pynetix.widgets.foldwidget import FoldWidget


class MetaDataWidget(FoldWidget):
    def __init__(self) -> None:
        self.items = []
        self.plate = None

        super().__init__(QWidget(), 'Meta Data')

    def setPlate(self, plate) -> None:
        self.plate = plate

        for item in self.items:
            self._removeItem(item)
        self.items.clear()

        for i, metaData in enumerate(self.plate.metaData):
            self._addItem(i, metaData)

    def _addItem(self, i: int, metaData) -> None:
        label = QLabel(metaData + ':  ')
        label.setSizePolicy(QSizePolicy.Policy.Minimum,
                            QSizePolicy.Policy.Preferred)
        self.body.layout().addWidget(label, i, 0)

        edit = QLineEdit()
        edit.setMinimumWidth(200)
        edit.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Preferred)
        edit.setText(str(self.plate.metaData[metaData]))
        # optional lambda variable necessary to change from pass
        # by reference to pass by value
        edit.textChanged.connect(
            lambda v, m=metaData: self.plate.changeMetaData(m, v))
        self.body.layout().addWidget(edit, i, 1)
        self.items.append({'label': label, 'edit': edit})

    def _removeItem(self, item) -> None:
        self.body.layout().removeWidget(item['edit'])
        item['edit'].deleteLater()
        self.body.layout().removeWidget(item['label'])
        item['label'].deleteLater()

    def _initBody(self, *args) -> None:
        body = QWidget()
        body.setLayout(QGridLayout())
        body.layout().setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        super()._initBody(body)

    def closeEvent(self, event) -> None:
        return super().closeEvent(event)
