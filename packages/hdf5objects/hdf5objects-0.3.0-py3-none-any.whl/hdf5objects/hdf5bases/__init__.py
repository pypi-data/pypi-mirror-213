"""__init__.py
The base objects for HDF5 objects.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Local Packages #
from .hdf5map import HDF5Map
from .hdf5basecomponent import HDF5BaseComponent
from .hdf5baseobject import HDF5BaseObject
from .hdf5attributes import HDF5Attributes
from .hdf5group import HDF5Group
from .hdf5dataset import HDF5Dataset, DatasetMap
from .hdf5file import HDF5File
from .hdf5caster import HDF5Caster


# Assign Cyclic Definitions
HDF5Map.default_attributes_type = HDF5Attributes
HDF5Map.default_type = HDF5Group

HDF5Group.default_group_map = HDF5Map
HDF5Group.default_dataset_map = DatasetMap

HDF5BaseObject.file_type = HDF5File
HDF5BaseObject.default_map = HDF5Map()
