import json
import sys
from pathlib import Path

import h5py as h5py
import numpy as np

from nanoqnt.model.analyze_nanoqnt import AnalyzeNanoQNT


def make_hdf_from_tiff(filename, num_channels=None):
    """ Transforms a multi-tiff file into an HDF5 file with the channels separated into different datasets.
    """
    filename = Path(filename)
    qnt = AnalyzeNanoQNT()
    qnt.open(str(filename))
    if num_channels is None:
        num_channels = qnt.num_channels
        print(f'Found number of channels: {num_channels}')
    with h5py.File(str(filename.parent / (str(filename.stem) + '.h5')), 'w') as f:
        g = f.create_group('data')
        mdata = g.create_dataset('metadata', data=json.dumps(qnt.metadata).encode('utf-8', 'ignore'))
        for c in range(num_channels):
            g.create_dataset(f'channel_{c}', data=np.array(qnt.data[c:-1:qnt.num_channels]), compression='gzip',
                             compression_opts=1)


def make_hdf():
    filename = sys.argv[1]
    num_channels = None
    if len(sys.argv) > 2:
        num_channels = int(sys.argv[2])
    print(f'Going to process {filename} with {num_channels} channels')
    make_hdf_from_tiff(filename, num_channels)