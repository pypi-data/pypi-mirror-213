import pytest
import h5py
from tests.classes_skels import *
from idspy_toolkit.converter import ids_to_hdf5, hdf5_to_ids
from random import randrange
from typing import Union
from idspy_dictionaries import ids_gyrokinetics as gkids
import idspy_toolkit
import numpy as np

@pytest.fixture(scope="function")
def hdf5_file(tmp_path_factory):
    fn = tmp_path_factory.mktemp("data") / "class_ids_{0:04d}.h5".format(randrange(0, 9999))
    return fn

def test_eigenmode_write(hdf5_file):
    ids = gkids.Eigenmode()
    idspy_toolkit.fill_default_values_ids(new_ids=ids)
    ids.code.parameters = '{"a":2}'
    ids.code.output_flag = 2
    assert ids_to_hdf5(ids, hdf5_file) == (2, 2)
    ids_read = gkids.Eigenmode()
    idspy_toolkit.fill_default_values_ids(new_ids=ids_read)
    hdf5_to_ids(hdf5_file, ids_read)
    assert ids_read.code.parameters == ids.code.parameters
    assert ids_read.code.output_flag == ids.code.output_flag

def test_eigenmode_write_wrong_type(hdf5_file):
    ids = gkids.Eigenmode()
    idspy_toolkit.fill_default_values_ids(new_ids=ids)
    ids.code.parameters = '{"a":2}'
    ids.code.output_flag = [2,3,]
    assert ids_to_hdf5(ids, hdf5_file) == (2, 2)
    ids_read = gkids.Eigenmode()
    idspy_toolkit.fill_default_values_ids(new_ids=ids_read)
    hdf5_to_ids(hdf5_file, ids_read)
    assert ids_read.code.parameters == ids.code.parameters
    np.testing.assert_array_equal(ids_read.code.output_flag, ids.code.output_flag)
