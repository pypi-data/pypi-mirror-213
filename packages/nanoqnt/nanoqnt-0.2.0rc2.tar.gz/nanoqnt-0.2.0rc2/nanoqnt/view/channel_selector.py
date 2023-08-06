from PyQt5 import uic
from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget

from nanoqnt.view import VIEW_FOLDER


class ChannelSelector(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(str(VIEW_FOLDER / 'GUI' / 'channel_selector.ui'), self)
        self.update_channels(0)
        self.channel_box.currentIndexChanged.connect(self.update_channels)
        self.channels = []
        self.accept_button.clicked.connect(self.close)

    def update_channels(self, number):
        self.channels = []
        layout = self.channels_widget.layout()
        for i in range(layout.rowCount()):
            layout.removeRow(0)

        for i in range(number + 1):
            self.channels.append(QLineEdit(f"Name {i}"))
            layout.addRow(QLabel(f"Channel {i}"), self.channels[-1])
