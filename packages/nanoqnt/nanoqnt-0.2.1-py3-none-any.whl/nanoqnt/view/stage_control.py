from threading import Thread

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from nanoqnt.view import VIEW_FOLDER


class StageControlWindow(QMainWindow):
    def __init__(self, model=None):
        """
        :param StageControl model: Model used to control the stage
        """
        super().__init__(parent=None)
        uic.loadUi(str(VIEW_FOLDER / 'GUI' / 'scan_control.ui'), self)
        self.model = model

        self.start_live_button.clicked.connect(self.model.live)
        self.stop_live_button.clicked.connect(self.model.stop_live)
        self.snap_button.clicked.connect(self.model.snap)
        self.scan_button.clicked.connect(self.scan)
        self.goto_button.clicked.connect(self.move)

    def scan(self):
        start = int(self.start_line.text())
        end = int(self.stop_line.text())
        step_size = int(self.step_line.text())
        self.model.prepare_scan(start)

        self.msgbox = QMessageBox()
        self.msgbox.setText(f'Open Multi-D Acq. in Micromanager and set the count to {int((end - start) / step_size)}')
        self.msgbox.exec()

        self.scan_thread = Thread(
            target=self.model.scan, args=(start, end, step_size)
            )
        self.scan_thread.start()

    def move(self):
        goto = int(self.goto_line.text())
        self.model.move(goto)
