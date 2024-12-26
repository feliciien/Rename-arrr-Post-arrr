#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication
from rename_arrr.gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
