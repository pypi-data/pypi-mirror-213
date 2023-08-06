import sys

from PyQt5.QtWidgets import QApplication

from nanoqnt.model.stage_control import StageControl
from nanoqnt.view.stage_control import StageControlWindow


def start_stage_control():
    model = StageControl()
    app = QApplication([])
    window = StageControlWindow(model)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    start_stage_control()
