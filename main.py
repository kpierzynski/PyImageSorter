from PySide6.QtWidgets import QApplication
from MainWindow import MainWindow

import sys
import signal

app = QApplication(sys.argv)

window = MainWindow()
window.show()

signal.signal(signal.SIGINT, signal.SIG_DFL)

app.exec()
