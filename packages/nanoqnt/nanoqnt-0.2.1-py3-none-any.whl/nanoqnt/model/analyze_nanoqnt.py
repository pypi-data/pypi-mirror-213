import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import pims as pims
import trackpy as tp
import yaml
from scipy.spatial import KDTree
from skimage import morphology
from skimage.measure import label, regionprops_table
from trackpy.find import where_close
from trackpy.utils import pandas_concat

logger = logging.getLogger(__name__)


class AnalyzeNanoQNT:
    def __init__(self):
        self.filename = None
        self.data = None
        self.metadata = {}
        self.particle_df = []
        self.particles = pd.DataFrame()
        self.num_frames = 0
        self.find_settings = {}
        self.filename = Path.home()
        self.concentration = {}  # pcles/ml
        self.linked_particles = None
        self.total_num_particles = 0
        self.summarized_particles = None

        self.ignore_edge_pixels = 8

        self.num_channels = 1
        self.channels_data = {}
        self.channels_names = []
        self.bkg = None


    def open(self, filename):
        """ Opens the file with the data. Normally a multi-tiff file, but it can be adapted to other formats.
        It also looks for the comments.txt file (create by uManager) in order to load some metadata

        :param filename: The full-path to the file to be opened
        """
        self.filename = Path(filename)
        self.metadata['filename'] = str(filename)
        self.metadata['last_dir'] = str(self.filename.parent)
        self.data = pims.open(filename)
        self.num_frames = len(self.data)  # This is really the number of frames in the data, not the number of
        # multi-channel frames

        self.particle_df = [pd.DataFrame() for _ in range(len(self.data))]
        self.particles = pd.DataFrame()
        self.find_settings = {}
        self.linked_particles = None
        self.summarized_particles = None
        self.total_num_particles = 0
        self.channels_data = {}

        comments_file = self.filename.parent / 'comments.txt'
        try:
            with open(comments_file, 'r') as f:
                self.metadata['uManager'] = json.load(f)
        except FileNotFoundError:
            self.metadata['uManager'] = {'comments': 'file not found'}

        try:
            comment = self.metadata['uManager']['map']['General annotation']['scalar']['comments']['scalar']
            start = comment.index('(') + 1
            end = comment.index(')')
            self.num_channels = len(comment[start:end].split(' '))
            self.channels_names = [i for i in range(self.num_channels)]
        except:
            pass

    def find_particles(self, frame_num, diameter, minmass, method='mask'):
        """ Finds particles in a given frame and stores the data frame in a list indexed by the frame number.

        :param int frame_num: The number of the frame (0-indexed) to analyze
        :param int diameter: The expected diameter of the particles. Must be an odd number and is passed directly to
        Trackpy
        :param int minmass: Filter to select bright enough spots. The parameter is passed directly to Trackpy.
        :param str method: Either select trackpy or mask. Default is mask.
        """
        if method == 'python' or method == 'numba':
            if frame_num in self.find_settings:
                settings = self.find_settings[frame_num]
                if diameter == settings['diameter'] and minmass == settings['minmass']:
                    return self.particle_df[frame_num]
            self.find_settings[frame_num] = {
                'diameter': diameter,
                'minmass': minmass,
                }
            df = tp.locate(self.data[frame_num], diameter, minmass=minmass, characterize=False)
            df = df.loc[df['y'] >= self.ignore_edge_pixels]
            self.particle_df[frame_num] = df
            return df

        elif method == 'mask':
            mask = self.data[frame_num] > minmass
            mask = morphology.remove_small_objects(mask, diameter)
            label_img = label(mask)
            props = regionprops_table(label_img, intensity_image=np.array(self.data[frame_num]), properties=('centroid',
                                                                                                             'intensity_mean',))
            df = pd.DataFrame(props).rename(columns={'centroid-0': 'y', 'centroid-1': 'x', 'intensity_mean': 'mass'})
            to_drop = where_close(df[['x', 'y']], separation=diameter * 2, intensity=df['mass'])
            df = df.drop(to_drop)
            df = df.loc[df['y'] >= self.ignore_edge_pixels]
            self.particle_df[frame_num] = df
            return df

    def find_all_particles(self, frames_no, diameter, minmass, method='numba'):
        """ Finds all the particles in a given range of frames. If the data has multiple channels, then it can handle
        different settings for each one. In that case, diameter and minmass must be iterables and in the appropriate
        order, i.e., the first setting will be for the first channel, etc.

        The data is structured as a dictionary, where each channel is a different key, and then the localizations are
        stored as a pandas dataframe.

        :param list frames_no:
        :param tuple diameter:
        :param tuple minmass:
        :param str method:
        :return dict: dictionary of particles found in each channel
        """
        try:
            if len(diameter) != self.num_channels:
                diameter = self.num_channels * [diameter]
        except TypeError:
            diameter = self.num_channels * [diameter]
        try:
            if len(minmass) != self.num_channels:
                minmass = self.num_channels * [minmass]
        except TypeError:
            minmass = self.num_channels * [minmass]

        if len(frames_no) == 1:
            frames_no = (0, self.num_frames)

        self.particles = {}

        self.metadata.update({
            'frames': frames_no,
            'diameter': diameter,
            'minmass': minmass,
            'engine': method,
            })

        if method == 'mask':
            for channel in range(self.num_channels):
                all_features = []
                for frame in range(frames_no[0], frames_no[1]):
                    real_frame = frame * self.num_channels + channel
                    df = self.find_particles(real_frame, diameter[channel], minmass[channel], method='mask')
                    df['frame'] = frame
                    all_features.append(df)
                self.particles[channel] = pandas_concat(all_features).reset_index(drop=True)
            return self.particles

        for channel in range(self.num_channels):
            data = np.array(self.data[frames_no[0] * self.num_channels + channel:frames_no[
                                                                                     1] * self.num_channels + channel:self.num_channels])
            data = [data[i, ...] for i in range(data.shape[0])]

            self.particles[channel] = tp.batch(data,
                                               diameter[channel],
                                               minmass=minmass[channel],
                                               characterize=False,
                                               preprocess=False,
                                               processes='auto',
                                               engine=method)

    def link_particles(self, search_radius, memory=0, min_frames=0):
        self.linked_particles = {}
        for channel in range(self.num_channels):
            self.linked_particles[channel] = tp.link(self.particles[channel], search_radius, memory=memory)
            self.linked_particles[channel] = tp.filter_stubs(self.linked_particles[channel], min_frames)

        self.metadata.update({
            'search_radius': search_radius,
            'min_frames': min_frames,
            'memory': memory
            })

    def calculate_intensities(self):
        """Calculates the intensities of the linked particles assuming they were the product of the mask method.
        The methods that rely on the trackpy algorithm already include the intensity.
        """
        self.summary_data = {}
        intensity_columns = [f'i_{channel}' for channel in range(self.num_channels)]

        if (engine := self.metadata.get('engine')) == 'python' or engine == 'numba':
            logger.info('Using the trackpy intensities')
            for channel in range(self.num_channels):
                self.summary_data[channel] = self.linked_particles[channel].groupby('particle').mean()
                self.summary_data[channel]['frame'] = self.summary_data[channel]['frame'].astype('int')
                self.summary_data[channel]['x'] = self.summary_data[channel]['x'].astype('int')
                self.summary_data[channel]['y'] = self.summary_data[channel]['y'].astype('int')
                for colum in intensity_columns:
                    self.summary_data[channel][colum] = np.nan
                self.summary_data[channel][f'i_{channel}'] = self.summary_data[channel]['mass']
                self.summary_data[channel] = self.summary_data[channel].reset_index(drop=True)
            return

        fit_size = 10
        x_fit = np.linspace(0, 2 * fit_size, 2 * fit_size + 1)
        y_fit = np.linspace(0, 2 * fit_size, 2 * fit_size + 1)
        x_fit, y_fit = np.meshgrid(x_fit, y_fit)
        initial_guess = (200, fit_size, fit_size, 2, 2, 200)

        for channel in range(self.num_channels):
            self.summary_data[channel] = pd.DataFrame(columns=['particle', 'frame', 'x', 'y'] + intensity_columns)

            for p in self.linked_particles[channel]['particle'].unique():
                pcle = self.linked_particles[channel].loc[self.linked_particles[channel]['particle'] == p]
                ix = pcle['mass'].idxmax()
                x = int(pcle.loc[ix]['y'])
                y = int(pcle.loc[ix]['x'])
                frame = int(pcle.loc[ix]['frame'])
                # TODO: This is hardcoded and dangerous. The margin used to drop particles must be properly considered
                if x < 20 or x > 2048 - 20 or y < 20 or y > 2048 - 20:
                    continue

                # try:
                #     f = frame*self.num_channels + channel
                #     popt, pcov = opt.curve_fit(twoD_Gaussian, (x_fit, y_fit),
                #                                np.array(self.data[f][x - fit_size:x + fit_size + 1,
                #                                         y - fit_size:y + fit_size + 1]).reshape(-1),
                #                                p0=initial_guess)
                # except Exception as e:
                #     print(e)
                #     continue

                df = pd.DataFrame.from_dict({
                    'particle': [p],
                    'frame': [pcle.loc[ix]['frame']],
                    'x': [pcle.loc[ix]['x']],
                    'y': [pcle.loc[ix]['y']],
                    f'i_{channel}': [pcle['mass'].max()]
                    })
                self.summary_data[channel] = pd.concat((self.summary_data[channel], df), ignore_index=True)
            self.summary_data[channel] = self.summary_data[channel].reset_index(drop=True)

    def multi_color_link(self):  # TODO: Add max frame distance as a parameter instead of fixing it to 5
        """ Find the same particles in every channel and add the intensity information on each """
        kd_trees = {}
        for channel in range(self.num_channels):
            kd_trees[channel] = KDTree(np.array(self.summary_data[channel][['x', 'y', 'frame']]))

        for channel in range(self.num_channels):
            for channel_2 in range(channel + 1, self.num_channels):
                for ix, p in self.summary_data[channel].iterrows():
                    dist, ind = kd_trees[channel_2].query((p['x'], p['y'], p['frame']), p=2, distance_upper_bound=15)
                    if ind == kd_trees[channel_2].n:
                        continue
                    if abs(self.summary_data[channel_2].loc[ind]['frame'] - p['frame']) > 5:
                        logger.info('Frames too far apart with ', ix, p['x'], p['y'], p['frame'])
                        continue
                    self.summary_data[channel].loc[ix, f'i_{channel_2}'] = \
                        self.summary_data[channel_2].loc[ind][f'i_{channel_2}']
                    self.summary_data[channel_2].loc[ind, f'i_{channel}'] = p[f'i_{channel}']

    def save_all_data(self, filename):
        self.linked_particles.to_csv(str(filename))

    def save_data(self, filename):
        """ Saves only the most important information to the file: particle and intensity information.
        """

        if len(self.channels_names) != self.num_channels:
            self.channels_names = [i for i in range(self.num_channels)]

        if not type(filename) is Path:
            filename = Path(filename)

        for i in range(self.num_channels):
            stem = filename.stem
            file_name = filename.with_stem(f'{stem}_{i}')
            self.summary_data[i].to_csv(str(file_name))

        # Exporting summary data
        with open(filename.with_suffix('.md'), 'w') as f:
            info = ""
            for channel in range(self.num_channels):
                info += f"# Channel {self.channels_names[channel]}\n\n"
                info += f" - *Found particles*: {len(self.summary_data[channel])}\n"
                if self.num_channels > 1:
                    for sub_channel in range(self.num_channels):
                        info += f" - Particles also in *{self.channels_names[sub_channel]}*: " \
                                f"{len(self.summary_data[channel][f'i_{sub_channel}'].dropna())}\n"
                info += f" - *Concentration*: {self.concentration.get(channel, 0):.2E} pcles/ml"
                info += '\n\n'
            f.write(info)

        with open(filename.with_suffix('.yml'), 'w') as f:
            yaml.dump(self.metadata, f)

    def calculate_concentration(self, step_size=5):
        """ Calculates the concentration on each channel in the dataset. After linking the particles,
        the concentration is calculated by simply counting the number of detections and dividing by the volume. The
        volume is derived from the field of view (given a magnification and sensor size) and the third dimension from
        the number of steps and the step size.

        TODO: Real-space FOV is hard-coded (as well as the region in the edges of the image that is discarded).
        """
        self.total_num_particles = {}
        self.concentration = {}
        if self.linked_particles is None:
            return
        fraction_sensor_used = (2048 - self.ignore_edge_pixels) / 2048
        field_of_view = fraction_sensor_used * (13.3 / 20) ** 2  # (Sensor size/magnification) # mm2
        for channel in range(self.num_channels):
            frames = self.linked_particles[channel]['frame'].max() - self.linked_particles[channel]['frame'].min() + 1
            volume = field_of_view * frames * step_size / 1000  # In mm3 (step_size in microns)
            volume = volume / 1000  # in ml
            num_particles = len(self.linked_particles[channel].groupby('particle').sum())

            self.total_num_particles[channel] = num_particles
            self.concentration[channel] = num_particles / volume

        self.metadata.update({'concentration': self.concentration})
