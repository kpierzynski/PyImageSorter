from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QIcon, QKeySequence, QAction


class Toolbar(QToolBar):
    def __init__(self, parent):
        super().__init__(parent=parent)

        parent.addToolBar(self)
        self.setWindowTitle("Main toolbar")

        self.prev = self.addAction(QIcon.fromTheme("previous"), "Previous")
        self.prev.setEnabled(False)
        self.prev.setShortcut(QKeySequence.MoveToPreviousChar)

        self.next = self.addAction(QIcon.fromTheme("next"), "Next")
        self.next.setEnabled(False)
        self.next.setShortcut(QKeySequence.MoveToNextChar)

        self.addSeparator()

        self.delete = self.addAction(QIcon.fromTheme('user-trash'), 'Delete')
        self.delete.setEnabled(False)
        self.delete.setShortcut(QKeySequence.Delete)

        self.addSeparator()

    def unlock(self):
        self.delete.setEnabled(True)
        self.next.setEnabled(True)
        self.prev.setEnabled(True)

    def lock(self):
        self.delete.setEnabled(False)
        self.next.setEnabled(False)
        self.prev.setEnabled(False)
