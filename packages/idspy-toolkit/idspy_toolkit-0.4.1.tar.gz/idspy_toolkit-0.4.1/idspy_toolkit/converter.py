"""

"""
import dataclasses
from typing import Any, Union, Tuple, TypeVar, Type
from typing_extensions import Protocol
from os import rename as os_rename
import os
import h5py
import numpy as np
import simplejson as js

from idspy_toolkit.snippets import is_dataclass_instance, is_dataclass_field, sort_h5_keys, _format_ids_substring
from idspy_toolkit.constants import IMAS_DEFAULT_INT, IMAS_DEFAULT_FLOAT, IMAS_DEFAULT_CPLX, IMAS_DEFAULT_STR
from idspy_toolkit.accessor import set_ids_value_from_string


class DataClass(Protocol):
    __dataclass_fields__: dict[str, Any]


DC = TypeVar("DC", bound=DataClass)


def _create_hdf5_dataset(value_name: str, value, parent_group) -> int:
    """
        create the dataset and write the associated value
        dict as serialized as strings
    :param value_name:
    :param value:
    :param parent_group:
    :return: number of created dataset or ValueError in case where value is a list with more than one type of elements
    """
    if value is None:
        raise ValueError("cannot write None value in hdf5 file")

    if isinstance(value, np.ndarray):
        if value.ndim == 0:
            value = float(value)

    str_type = h5py.special_dtype(vlen=str)
    parent_group.attrs["len"] = 1
    parent_group.attrs["type"] = "item"
    created_dataset = 1
    if isinstance(value, str):
        parent_group.create_dataset(value_name,
                                    data=value.encode("utf8"),
                                    dtype=str_type)
    elif isinstance(value, dict):
        value_as_str = js.dumps(value)
        parent_group.create_dataset(value_name,
                                    data=value_as_str.encode("utf8"),
                                    dtype=str_type)
    elif isinstance(value, (list, tuple)):
        same_type = all(isinstance(sub, type(value[0])) for sub in value[1:])
        if same_type is False:
            del parent_group.attrs["len"]
            del parent_group.attrs["type"]
            raise ValueError(f"different types for value {value}")
        value_ref = value[0]
        if is_dataclass_instance(value_ref):
            del parent_group.attrs["len"]
            del parent_group.attrs["type"]
            raise ValueError(f"cannot write a dataclass as a dataset {value}")
        parent_group.attrs["len"] = len(value)
        parent_group.attrs["type"] = "list"

        if isinstance(value_ref, dict):
            created_dataset = len(value)
            for i, val in enumerate(value):
                value_as_str = js.dumps(val)
                parent_group.create_dataset(value_name + f"_{i}", data=value_as_str,
                                            dtype=str_type)
        elif isinstance(value_ref, (list, tuple)):
            inner_val = np.asarray(value)
            created_dataset = 1
            parent_group.create_dataset(value_name, data=inner_val, )
        else:
            created_dataset = 1
            try:
                parent_group.create_dataset(value_name, data=value, )
            except TypeError:
                print(f"error raised for {value_name}:{value}/{type(value)}")
                raise
    else:
        parent_group.create_dataset(value_name, data=value, )

    return created_dataset


def get_inner_type_list(item: Union[list, tuple]) -> Union[Any, None]:
    test_var = item

    while isinstance(test_var, (list, tuple)):
        try:
            test_var = test_var[0]
        except IndexError:
            return None

    return test_var

def _is_list_empty(item: Any) -> bool:
    """
    Check if the given item is an empty list, tuple, or numpy array.

    :param item: The item to be checked.
    :type item: Any

    :return: True if the item is an empty list, tuple, or numpy array, False otherwise.
    :rtype: bool
    """
    if isinstance(item, (list, tuple)):
        if len(item) == 0:
            return True
    elif isinstance(item, np.ndarray):
        if item.ndim == 0:
            return False
        else:
            if len(item) == 0:
                return True
    return False


def _is_item_list(item: Any) -> bool:
    """
    Check if the given item is a list, tuple, or numpy array.

    :param item: The item to be checked.
    :type item: Any

    :return: True if the item is a list, tuple, or numpy array, False otherwise.
    :rtype: bool
    """
    if isinstance(item, (list, tuple)):
        return True
    elif isinstance(item, np.ndarray):
        if item.ndim == 0:
            return False
        else:
            return True
    return False


def ids_to_hdf5(ids: Type[DC], filename: str, overwrite:bool = False) -> Tuple[int, int]:
    """
    store an IDS class to a HDF5 file
    dict are stored as serialized json
    List of dict are serialized as a sequence of dataset
    List of values (int/float) as multidimensional dataset
    :param ids: IDS to store
    :param filename: name of the HDF5 file
    :param overwrite: what to do if file already exists?
    :return: IOError if HDF5 file already exist and overwrite is False, number of written groups and keys otherwise
    :TODO: manage empty files and empty group/dataclass
    :TODO: store strings as bytes
    """
    total_group: int = 0
    total_dataset: int = 0

    def _hdf5_header_metadata(parent_group):
        """
        write all main metadata to HDF5 root path
        ids script version
        dd version
        structure

        """
        pass

    def __check_all_fields_none(current_ids, default_vals_list):
        number_fields = len(list(dataclasses.fields(current_ids)))
        list_default = []
        for field in dataclasses.fields(current_ids):
            field_value = getattr(current_ids, field.name)
            if isinstance(field_value, (list, tuple)):
                if len(field_value) == 0:
                    list_default.append(None)
            elif isinstance(field_value, np.ndarray):
                if field_value.ndim == 0:
                    if field_value[()] in default_vals_list:
                        list_default.append(None)
                else:
                    if len(field_value) == 0:
                        list_default.append(None)
            elif field_value in default_vals_list:
                list_default.append(None)
        return len(list_default) == number_fields

    def _browse_ids(current_ids, parent_group, ids_group: int, ids_dataset: int,
                    named_group: Union[str, None] = None,
                    flat_idx: Union[int, None] = None) -> tuple[int, int]:
        if named_group is None:
            root_grp = str(type(current_ids)).split(".")[-1][:-2]
        else:
            root_grp = named_group
        list_default_values = (IMAS_DEFAULT_INT, IMAS_DEFAULT_FLOAT,
                               IMAS_DEFAULT_CPLX, IMAS_DEFAULT_STR, None)
        if flat_idx is not None:
            root_grp = "{0}{1}".format(root_grp, _format_ids_substring(flat_idx))

        all_none = __check_all_fields_none(current_ids, list_default_values)

        if all_none is True:
            return ids_group, ids_dataset

        current_grp = parent_group.create_group(root_grp)
        ids_group += 1

        for field in dataclasses.fields(current_ids):
            field_name = field.name
            field_value = getattr(current_ids, field_name)
            # check if field contains one of the 'default' value
            is_item_list = _is_item_list(field_value)
            if is_item_list is True:
                if _is_list_empty(field_value):
                    continue
            else:
                if field_value in list_default_values:
                    continue

            if isinstance(field_value, (list, tuple)):
                if len(field_value) == 0:
                    continue
                if is_dataclass_instance(field_value[0]):
                    for i, sub_ids in enumerate(field_value):
                        ids_group, ids_dataset = _browse_ids(sub_ids, current_grp,
                                                             ids_group, ids_dataset,
                                                             named_group=field_name,
                                                             flat_idx=i)
                else:
                    ids_dataset += _create_hdf5_dataset(field_name, field_value,
                                                        current_grp)
            elif is_dataclass_instance(field_value):
                # call recursive function
                ids_group, ids_dataset = _browse_ids(field_value, current_grp,
                                                     ids_group, ids_dataset,
                                                     named_group=field_name)
            else:
                ids_dataset += _create_hdf5_dataset(field_name, field_value,
                                                    current_grp)
        return ids_group, ids_dataset

    if overwrite is False :
        tmp_file = filename
        if os.path.exists(filename):
            raise IOError(f"HDF5 file {filename} already exist")
    if overwrite is True :
        tmp_file = filename+".tmp"
    # open the hdf5 file
    with h5py.File(tmp_file, "w") as h5f:
        total_group, total_dataset = _browse_ids(ids, h5f, total_group, total_dataset)
    if overwrite is True:
        os.remove(filename)
        os_rename(tmp_file, filename)
    print(f"IDS written to file : {filename}")
    return total_group, total_dataset


def _iterate_hdf5_dataset(name: str, hdf5obj: Any, h5struct: list) -> None:
    if isinstance(hdf5obj, h5py.Dataset):
        h5struct.append(r"/" + name)
    return None


def hdf5_to_ids(filename: str, ids: Type[DC]) -> Type[DC]:
    """
    read an IDS from an HDF5 file and return it
    :param filename: hdf5 filename
    :param ids: ids dataclass, has to be a fully develop IDS
    :return: IDS dataclass
    """
    if not os.path.exists(filename):
        raise IOError(f"HDF5 file {filename} not found")

    h5struct_ds:list = []
    # open the hdf5 file and read it recursively
    with h5py.File(filename, "r") as h5f:
        h5f.visititems(lambda x, y: _iterate_hdf5_dataset(x, y, h5struct_ds))
        if len(h5struct_ds) == 0:
            raise ValueError(f"file [{filename}] seems to not contain any data")
        h5struct_ds = sort_h5_keys(h5struct_ds)

        for keys in h5struct_ds:
            set_ids_value_from_string(ids, keys, h5f[keys][()])
    return ids
