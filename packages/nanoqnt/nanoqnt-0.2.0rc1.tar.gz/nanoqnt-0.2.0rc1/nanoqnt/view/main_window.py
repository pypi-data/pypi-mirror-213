from pathlib import Path

import matplotlib.pyplot as plt
import pyqtgraph as pg
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox

from nanoqnt.view import VIEW_FOLDER
from nanoqnt.view.channel_selector import ChannelSelector
from nanoqnt.view.particle_widget import ParticleWidget

home_path = Path.home()


class NanoQNTMainWindow(QMainWindow):
    def __init__(self, model=None):
        """
        :param AnalyzeNanoQNT model: Model used to analyze the data
        """
        super().__init__(parent=None)
        uic.loadUi(str(VIEW_FOLDER / 'GUI' / 'data_exploration.ui'), self)
        self.setWindowTitle('NanoQNT Analysis')

        self.analyze_model = model

        self.action_open.triggered.connect(self.open)
        self.action_mass_histogram.triggered.connect(self.histogram_mass)
        self.action_data_frame.triggered.connect(self.data_over_frame)
        self.action_data_plots.triggered.connect(self.total_histograms)
        self.action_export_all_data.triggered.connect(self.export_all_data)
        self.action_save_data.triggered.connect(self.export_data)
        self.action_calculate_bkg.triggered.connect(self.calculate_background)
        self.action_show_bkg.triggered.connect(self.show_background)

        self.frame_slider.valueChanged.connect(self.update_slider)
        self.step_size_line.editingFinished.connect(self.calculate_concentration)
        self.find_particles_check.toggled.connect(self.update_images)
        self.calculate_button.clicked.connect(self.calculate_all)
        self.action_about.triggered.connect(self.show_about)

        self.circles = []
        self.curr_index = 0

        self.channel_widget = ChannelSelector()
        self.channel_widget.accept_button.clicked.connect(self.channels_updated)

        self.nanoqnt_images = []

    def open(self):
        last_dir = self.analyze_model.metadata.get('last_dir', home_path)
        file = QFileDialog.getOpenFileName(self, 'Open Data', str(last_dir), filter='*.tif')[0]
        if file != '':
            file = Path(file)
        else:
            return

        self.channel_widget.show()

        self.analyze_model.open(str(file))
        self.setWindowTitle(f'NanoQNT Analysis: {file.name}')

    def update_slider(self, index):
        self.curr_index = index - 1
        self.frame_num.setText(str(index))
        self.update_images()

    def update_images(self, auto_range=False, auto_levels=False):
        if self.analyze_model.data is None:
            return

        for i, channel_image in enumerate(self.nanoqnt_images):
            index = self.curr_index * len(self.nanoqnt_images) + i
            circles = None
            if self.find_particles_check.isChecked():
                diameter = int(channel_image.size_line.text())
                minmass = int(channel_image.min_mass_line.text())
                method = self.engine_box.currentText()

                self.analyze_model.find_particles(index, diameter, minmass, method=method)
                particles_df = self.analyze_model.particle_df[index]
                circles = [pg.CircleROI([p[1] - 12, p[0] - 12], [25, 25],
                                        pen=pg.mkPen('r', width=2),
                                        movable=False,
                                        resizable=False,
                                        rotatable=False,
                                        removable=False,
                                        )
                           for p in zip(particles_df['x'], particles_df['y'])]
            channel_image.update_image(self.analyze_model.data[index], circles, auto_range=auto_range,
                                       auto_levels=auto_levels)

    def histogram_mass(self):
        index = self.curr_index
        diameter = int(self.size_line.text())
        minmass = int(self.min_mass_line.text())

        self.analyze_model.find_particles(index, diameter, minmass)

        fig, ax = plt.subplots(1)
        ax.hist(self.analyze_model.particle_df[index]['mass'], bins=50)
        fig.suptitle(f'Mass Histogram Frame Number: {self.curr_index}')
        fig.show()

    def calculate_all(self):
        QApplication.setOverrideCursor(Qt.BusyCursor)
        diameter = [int(channel_image.size_line.text()) for channel_image in self.nanoqnt_images]
        minmass = [int(channel_image.min_mass_line.text()) for channel_image in self.nanoqnt_images]
        engine = self.engine_box.currentText()
        frames_no = [int(self.start_frame_line.text()) - 1, int(self.end_frame_line.text())]
        self.analyze_model.find_all_particles(frames_no, diameter, minmass, engine)
        search_radius = int(self.search_radius_line.text())
        min_frames = int(self.min_frames_line.text())
        self.analyze_model.link_particles(search_radius, memory=0, min_frames=min_frames)
        self.analyze_model.calculate_intensities()
        self.analyze_model.multi_color_link()
        self.calculate_concentration()
        QApplication.setOverrideCursor(Qt.ArrowCursor)

    def data_over_frame(self):
        t1 = self.analyze_model.linked_particles

        fig, ax = plt.subplots(3, sharex=True)
        ax[0].plot(t1['ecc'].groupby('frame').mean())
        ax[0].set_ylabel('Eccentricity')
        ax[1].plot(t1['size'].groupby('frame').mean())
        ax[1].set_ylabel('Size')
        ax[2].plot(t1['mass'].groupby('frame').mean())
        ax[2].set_ylabel('Mass')
        ax[2].set_xlabel('Frame Num')
        fig.show()

    def total_histograms(self):
        if self.analyze_model.linked_particles is None:
            print('No particles to plot!')
            msg = QMessageBox.warning(self, "Run Analysis First", "Before being able to show the histogram of "
                                                                  "all "
                                                                  "the particles, you must run the analysis using "
                                                                  "the calculate all button.",
                                      QMessageBox.Ok)
            return

        for channel in range(self.analyze_model.num_channels):
            t1 = self.analyze_model.summary_data[channel]
            fig1, ax1 = plt.subplots(1)
            t1[f'i_{channel}'].hist(bins=100, ax=ax1)
            ax1.set_xlabel('Total Intensity (counts)')
            ax1.set_title(f'Channel: {channel}')
            fig1.show()

            for channel_2 in range(channel + 1, self.analyze_model.num_channels):
                fig, ax = plt.subplots(1)  # , figsize=(10, 8))
                ax.plot(self.analyze_model.summary_data[channel][f'i_{channel}'],
                        self.analyze_model.summary_data[channel][f'i_{channel_2}'],
                        'o',
                        alpha=0.1)
                ax.set_xlabel(self.channel_names[channel], fontsize=14)
                ax.set_ylabel(self.channel_names[channel_2], fontsize=14)
                plt.gca().tick_params(labelsize=12)
                # ax.set_yscale('log')
                # ax.set_xscale('log')
                fig.show()

    def calculate_concentration(self):
        step_size = float(self.step_size_line.text())
        self.analyze_model.calculate_concentration(step_size)
        for i in range(self.analyze_model.num_channels):
            self.nanoqnt_images[i].concentration_line.setText(f"{self.analyze_model.concentration[i]:.2E}")
            self.nanoqnt_images[i].total_particles_line.setText(f"{self.analyze_model.total_num_particles[i]}")

    def export_all_data(self):
        path = self.analyze_model.filename.parent
        filename = QFileDialog.getSaveFileName(self, 'Save to file', str(path), '*.csv')[0]

        if filename is not None:
            self.analyze_model.save_all_data(filename)

    def export_data(self):
        path = self.analyze_model.filename.parent
        filename = QFileDialog.getSaveFileName(self, 'Save to file', str(path), '*.csv')[0]

        if filename is not None:
            self.analyze_model.save_data(filename)

    def channels_updated(self):
        self.analyze_model.num_channels = self.channel_widget.channel_box.currentIndex() + 1
        self.channel_names = [line.text() for line in self.channel_widget.channels]

        self.nanoqnt_images = [ParticleWidget() for _ in range(self.analyze_model.num_channels)]

        plot_layout = self.video_widget.layout()
        for i in reversed(range(plot_layout.count())):
            plot_layout.itemAt(i).widget().setParent(None)

        if self.analyze_model.num_channels == 1:
            plot_layout.addWidget(self.nanoqnt_images[0], 0, 0)
        elif self.analyze_model.num_channels == 2:
            plot_layout.addWidget(self.nanoqnt_images[0], 0, 0)
            plot_layout.addWidget(self.nanoqnt_images[1], 0, 1)
        elif self.analyze_model.num_channels == 3:
            plot_layout.addWidget(self.nanoqnt_images[0], 0, 0)
            plot_layout.addWidget(self.nanoqnt_images[1], 0, 1)
            plot_layout.addWidget(self.nanoqnt_images[2], 1, 0)
        elif self.analyze_model.num_channels == 4:
            plot_layout.addWidget(self.nanoqnt_images[0], 0, 0)
            plot_layout.addWidget(self.nanoqnt_images[1], 0, 1)
            plot_layout.addWidget(self.nanoqnt_images[2], 1, 0)
            plot_layout.addWidget(self.nanoqnt_images[3], 1, 1)

            # print(plot_layout.itemAt(i).widget().image.view.state)

        if self.analyze_model.num_channels > 1:
            for i, plot in enumerate(self.nanoqnt_images[:-1]):
                view = plot.image.view
                view.linkView(self.nanoqnt_images[i + 1].image.view.XAxis, self.nanoqnt_images[i + 1].image.view)
                view.linkView(self.nanoqnt_images[i + 1].image.view.YAxis, self.nanoqnt_images[i + 1].image.view)

        self.frame_slider.setRange(1, int(self.analyze_model.num_frames / self.analyze_model.num_channels))
        self.frame_slider.setEnabled(True)
        self.start_frame_line.setText("1")
        self.end_frame_line.setText(str(int(self.analyze_model.num_frames / self.analyze_model.num_channels)))
        self.update_slider(1)

        self.update_images(auto_range=True, auto_levels=True)
        for i in reversed(range(plot_layout.count())):
            plot_layout.itemAt(i).widget().autoRange()
            plot_layout.itemAt(i).widget().min_mass_line.editingFinished.connect(self.update_images)
            plot_layout.itemAt(i).widget().size_line.editingFinished.connect(self.update_images)

    def calculate_background(self):
        print('Calculating background')
        QApplication.setOverrideCursor(Qt.BusyCursor)
        frames_no = [int(self.start_frame_line.text()) - 1, int(self.end_frame_line.text())]
        self.analyze_model.calculate_background(frames_no=frames_no)
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        print('Done calculating background')

    def show_background(self):
        fig, ax = plt.subplots(1)
        ax.imshow(self.analyze_model.bkg)
        fig.suptitle(f'Mass Histogram Frame Number: {self.curr_index}')
        fig.show()

    def show_about(self):
        QMessageBox.about(self, 'About NanoQNTPy', 'Beta version 0.1')
