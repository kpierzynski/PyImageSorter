from PySide6.QtWidgets import QWidget, QListWidget, QListWidgetItem
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPainter


class QEasyList(QListWidget):
    selected = Signal(QWidget)

    def __init__(self, listItems: list[QWidget] = []):
        super().__init__()
        self.list = []

        for widget in listItems:
            self.addWidget(widget)

        self.doubleClicked.connect(self._doubleClick)

    def paintEvent(self, event):
        super().paintEvent(event)

        if not len(self.list):
            painter = QPainter(self.viewport())
            painter.save()

            col = self.palette().placeholderText().color()
            painter.setPen(col)

            painter.drawText(self.viewport().rect().adjusted(0, 10, 0, 0),
                             Qt.AlignHCenter, "Empty")
            painter.restore()

    def addWidget(self, widget: QWidget) -> None:
        self.list.append(widget)

        item = QListWidgetItem(self)
        item.setSizeHint(widget.sizeHint())

        self.addItem(item)
        self.setItemWidget(item, widget)

    def clearWidgets(self) -> None:
        self.list.clear()
        self.clear()

    def _doubleClick(self, index):
        item = self.itemFromIndex(index)
        widget = self.itemWidget(item)

        self.selected.emit(widget)
