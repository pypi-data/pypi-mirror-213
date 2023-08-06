import pyqtgraph as pg
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from nanoqnt.view import VIEW_FOLDER


class ParticleWidget(QWidget):
    """Wrapper class to display image data with few signals to update the frame. It is meant to handle also
    multi-color data"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(str(VIEW_FOLDER / 'GUI' / 'particles_widget.ui'), self)
        self.image = pg.ImageView()
        self.image.setPredefinedGradient('thermal')

        self.circles = []

        plot_layout = self.video_widget.layout()
        plot_layout.addWidget(self.image)

    def autoRange(self):
        """ Wrapper to the default PyQtGraph auto range to see if it integrates better with the overall UI"""
        # self.image.view.setXRange(0, 2000)
        self.image.view.setRange(xRange=(0, 2000), yRange=(0, 2000))

    def update_image(self, image, circles=None, auto_range=False, auto_levels=False):
        for r in self.circles:
            self.image.removeItem(r)
            self.circles = []

        self.image.setImage(image, autoRange=auto_range, autoLevels=auto_levels)

        if circles is not None:

            self.circles = circles

            for p in self.circles:
                try:  # Very dangerous, but this is a feature fixed by PyQtGraph only on version > 0.13.2
                    p.removeHandle(0)
                except:
                    pass
                self.image.addItem(p)
            self.found_particles_line.setText(str(len(circles)))

        if auto_range:
            self.autoRange()
        if auto_levels:
            self.image.autoLevels()

    def removeItem(self, r):
        self.image.removeItem(r)

    def setImage(self, *args, **kwarks):
        self.image.setImage(*args, **kwarks)

    def addItem(self, p):
        self.image.addItem(p)

    def autoLevels(self):
        self.image.autoLevels()
