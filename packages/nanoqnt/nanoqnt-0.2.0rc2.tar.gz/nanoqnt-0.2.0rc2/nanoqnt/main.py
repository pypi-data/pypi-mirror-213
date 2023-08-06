import os
import sys
from multiprocessing import freeze_support

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication

from nanoqnt.model.analyze_nanoqnt import AnalyzeNanoQNT
from nanoqnt.view.main_window import NanoQNTMainWindow

try:
    from ctypes import windll  # Only exists on Windows.

    myappid = 'Dispertech.NanoQNT.Analysis.0.2.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


def start_nanoqnt():
    basedir = os.path.dirname(__file__)
    model = AnalyzeNanoQNT()
    app = QApplication([])
    app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'dispertech-logo.ico')))
    main_window = NanoQNTMainWindow(model)
    main_window.show()
    app.exec()
    sys.exit()


if __name__ == '__main__':
    freeze_support()
    start_nanoqnt()
