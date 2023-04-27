from PySide6.QtWidgets import QWidget, QListWidget, QListWidgetItem
from PySide6.QtCore import Signal


class QEasyList(QListWidget):
    selected = Signal(QWidget)

    def __init__(self, listItems: list[QWidget] = []):
        super().__init__()

        for widget in listItems:
            self.addWidget(widget)

        self.doubleClicked.connect(self._doubleClick)

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
