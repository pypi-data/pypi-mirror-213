import dataclasses
from dataclasses import Field
from typing import get_type_hints, Any, get_origin, TypeVar, Type, Union
from typing_extensions import Protocol
from idspy_toolkit.utils import camel2snake,  extract_ndarray_info
import inspect
from numpy import ndarray


class DataClass(Protocol):
    __dataclass_fields__: dict[str, Any]


DC = TypeVar("DC", bound=DataClass)


def is_list_member(classname: Any, fieldname: str) -> bool:
    """
    Checks if a field_clazz in a dataclass is a list.

    :param classname: The  dataclass.
    :type classname: dataclass
    :param fieldname: The name of the field_clazz to check.
    :type fieldname: str
    :return: True if the field_clazz is a list, False otherwise.
    :rtype: bool
    """

    # Get the dataclass field_clazz object
    field = classname.__dataclass_fields__[fieldname]

    # Get the type of the field_clazz
    field_type = get_type_hints(classname)[field.name]

    # If the field_clazz type is a list or a new-style list, return True
    if isinstance(field_type, list) or field_type == list:
        return True

    # If the field_clazz type is a generic type that inherits from list or new-style list, return True
    if inspect.isclass(field_type) and (issubclass(field_type, list) or field_type == list):
        return True

    # If the field_clazz type is a type variable with a bound that inherits from list or new-style list, return True
    origin = get_origin(field_type)
    if origin is not None and inspect.isclass(origin) and (issubclass(origin, list) or origin == list):
        return True

    # Otherwise, return False
    return False


def get_type_arg(clazz: Type[DC], field_clazz: Union[str, Field[Any]]) -> Any:
    """
    Get the type argument of a dataclass field.

    :param clazz: The dataclass to get the field from.
    :param field_clazz: The name of the field to get the type argument from.
    :return: A tuple containing the type argument of the field and a boolean value indicating if the field is a list.
    :raises KeyError: If the specified field is not found in the dataclass.

    Examples:
        >>> @dataclass
        ... class Foo:
        ...     bar: list[int]
        ...
        >>> get_type_arg(Foo, 'bar')
        (int, True)
    """
    # had to use a try/except due to handle some forwardref cases in dataclasses
    is_list = False
    try:
        item = get_type_hints(clazz)[field_clazz.name]
        is_list = is_list_member(clazz, field_clazz.name)
    except NameError:
        item = get_type_hints(type(clazz))[field_clazz.name]
        is_list = is_list_member(type(clazz), field_clazz.name)
    except AttributeError:
        item = get_type_hints(clazz)[field_clazz]
        is_list = is_list_member(clazz, field_clazz)

    data_type = getattr(item, "__args__", (item,))[0]

    return data_type, is_list


def __split_path(path: str, root_type_str: str) -> list:
    path_members = [x for x in path.strip().split(r"/") if x]
    if path[0] == r"/":
        if path_members[0] not in root_type_str:
            raise AttributeError("given path does not correspond to current ids type")
        path_members = path_members[1:]
    return path_members


def get_ids_value_from_string(ids: Type[DC], path: str) -> Any:
    """
    Get the value of a field_clazz within a nested dataclass object by specifying the path to it as a string.

    :param ids: The dataclass object to get the field_clazz value from.
    :param path: The path to the field_clazz within the dataclass object.
    :return: The value of the specified field_clazz.
    :raises AttributeError: If the specified path does not correspond to the type of the given dataclass object.
    :raises ValueError: If the specified path contains a non-existent field_clazz or if a list field_clazz is accessed with an out-of-range index.
    :raises TypeError: If the specified path contains a list field_clazz but the next part of the path is not an index.
    :raises KeyError: If the specified path corresponds to an IDS root and not an IDS member.

    Examples:
        >>> @dataclass
        ... class Foo:
        ...     bar: int = 0
        ...
        >>> foo = Foo()
        >>> foo.bar = 42
        >>> get_ids_value_from_string(foo, 'bar')
        42

        >>> @dataclass
        ... class Foo:
        ...     bar: List[str] = []
        ...
        >>> foo = Foo()
        >>> foo.bar = ['hello', 'world']
        >>> get_ids_value_from_string(foo, 'bar#0')
        'hello'
    """
    try:
        path_members = __split_path(path, str(type(ids)))
        current_attr = ids
    except IndexError:
        raise KeyError("get_ids_value_from_string does not allow to get a full IDS, just IDS members")

    for idx, subpath in enumerate(path_members):
        if "#" in subpath:
            name, offset = subpath.strip().split("#")
            offset = int(offset)
            name = camel2snake(name)
            # TODO: check that return value of getattr is a list as expected
            list_attr = getattr(current_attr, name, None)
            len_list_attr = len(list_attr)

            if name is None:
                raise ValueError(f"missing element {subpath}")
            if not isinstance(list_attr, (list, tuple)):
                raise AttributeError(f"element {name} is not a list")
            if len_list_attr < offset and offset > 0:
                raise IndexError(f"element {name} has a len of {len_list_attr} and cannot reach elem #{offset}")
            if len_list_attr == 0:
                raise ValueError(f"element {name} is empty")
            elif len_list_attr <= offset:
                raise IndexError(f"cannot access element {offset + 1}/{len_list_attr} for {name}")
            return get_ids_value_from_string(list_attr[offset], "/".join(path_members[idx + 1:]))
        else:
            if isinstance(current_attr, (list, tuple)):
                raise ValueError(f"attribute [{path_members[idx - 1]}] is a list")
            current_attr = getattr(current_attr, subpath)
    if isinstance(current_attr, bytes):
        return current_attr.decode("utf8")
    return current_attr


def create_instance_from_type(var_type: Any) -> Any:
    """
    Create a variable instance from the given type.

    :param var_type: A type to create a variable from.
    :type var_type: Any
    :return: A variable created from the given type.
    :rtype: Any
    :raises TypeError: If the input type is not a dataclass or a supported built-in type.
    :raises TypeError: If the input type is a dataclass that has a field_clazz with an unsupported type.
    """

    if dataclasses.is_dataclass(var_type):
        dict_args = {}
        for f in dataclasses.fields(var_type):
            arg_type, is_list = get_type_arg(var_type, f.name)
            if is_list is True:
                dict_args.update({f.name: list()})
            else:
                if "ndarray" in str(arg_type):
                    shape, dtype = extract_ndarray_info(str(arg_type))
                    dict_args.update({f.name: ndarray(shape=shape, dtype=dtype)})
                else:
                    dict_args.update({f.name: arg_type()})
        return var_type(**dict_args)
    else:
        return var_type()


def set_ids_value_from_string(ids: Type[DC], path: str, value: Any, create_missing: bool = True):
    """
    Sets the value of an attribute in a nested dataclass given its path.

    :param ids: the nested dataclass instance to modify
    :type ids: dataclasses.dataclass

    :param path: the path of the attribute to modify
    :type path: str

    :param value: the new value to set for the attribute
    :type value: any

    :param create_missing: whether to create missing attributes or not, defaults to False
    :type create_missing: bool

    :raises AttributeError: if the given path does not correspond to the type of the `ids` argument
    :raises AttributeError: if an element in the path is missing or not of dataclass type, if the attribute is a list
     and create_missing is False, if an element in the list does not exist and create_missing is False,
     or if the attribute is a list and the path does not end with '#XXXX'
    :raises IndexError: if an element in the list is out of range

    :return: None
    """

    path_members = __split_path(path, str(type(ids)))
    current_attr = ids

    for idx, subpath in enumerate(path_members[:-1]):
        old_attr = current_attr

        # '#' indicates current item is a list element
        if "#" in subpath:
            name, offset = subpath.strip().split("#")
            offset = int(offset)
            name = camel2snake(name)
            list_attr = getattr(current_attr, name, None)
            len_list_attr = len(list_attr)
            type_arg_list, _ = get_type_arg(old_attr, name)
            # TODO: exact role of create missing
            if name is None:
                if create_missing is False:
                    raise AttributeError(f"missing element {subpath}")
            if not isinstance(list_attr, (list, tuple)):
                raise AttributeError(f"element {name} is not a list")
            if len_list_attr < offset and offset > 0:
                raise IndexError(f"element {name} has a len of {len_list_attr} and cannot reach elem #{offset}")

            if (offset == len_list_attr) and (create_missing is True):
                # create a new subitem and append it to the list
                list_attr.append(create_instance_from_type(type_arg_list))

            elif (offset == len_list_attr) and (create_missing is False):
                raise IndexError(
                    f"element number #{offset} does not exist and cannot be created :"
                    f" create_missing is {create_missing}")

                # set value of indicated subitem
            return set_ids_value_from_string(list_attr[offset], "/".join(path_members[idx + 1:]), value, create_missing)
        else:
            current_attr = getattr(current_attr, subpath, None)
            if current_attr is None:
                if create_missing is False:
                    raise AttributeError(f"missing element {subpath}")
                else:
                    if isinstance(old_attr, (list, tuple)):
                        raise AttributeError(
                            f" item {path_members[idx - 1]} is represented by a list in the dataclass and should be "
                            f"reached with the syntax item#XXXX")
                    if not dataclasses.is_dataclass(old_attr):
                        raise AttributeError(f" item {path_members[idx - 1]} is not of dataclass type {old_attr}")

    if isinstance(current_attr, (list, tuple)):
        raise AttributeError(f"attribute [{path_members[-2]}] is a list so it must be used as {path_members[-2]}#XXXX")
    if current_attr is None:
        raise AttributeError(f"attribute [{path_members[-2]}] is missing in the IDS {type(ids)}")

    # last attribute correspond to a list element
    if "#" in path_members[-1]:
        name, offset = path_members[-1].strip().split("#")
        offset = int(offset)
        attr_value = getattr(current_attr, name)
        if isinstance(attr_value, (list, tuple)):
            return setattr(current_attr, name[offset], value)
        else:
            raise AttributeError(f"attribute {name} is of type {type(attr_value)} and not list")

    attr_type, _ = get_type_arg(current_attr, path_members[-1])
    if isinstance(value, bytes):
        value = value.decode("utf8")
    if isinstance(value, str) and (attr_type is not str):
        raise ValueError(
            f"value for attr {path_members[-1]} is of type {type(value)} and should be of type {attr_type}")

    setattr(current_attr, path_members[-1], value)


def copy_ids(dest_ids: Type[DC], source_ids: Type[DC],
             ignore_missing=False, keep_source_ids=False, bytes_to_str=True) -> None:
    """
    Copy the fields of the dataclass given at source_ids in the dataclass dest_ids.

    Args:
        dest_ids (dataclass): The destination dataclass to copy the fields to.
        source_ids (dataclass): The source dataclass to copy the fields from.
        ignore_missing (bool, optional): If True, missing fields in dest_ids are ignored. Otherwise, a KeyError is
        raised. Defaults to False.
        keep_source_ids (bool, optional): If True, the source fields are set to None after being copied to the
        destination dataclass. Defaults to False.
        bytes_to_str (bool, optional): If True, bytes fields are decoded to str if the destination field_clazz is of type str.
         Otherwise, they are copied as bytes. Defaults to True.

    Raises:
        TypeError: If dest_ids or source_ids is not a dataclass.
        KeyError: If ignore_missing is False and a field_clazz is missing in dest_ids.

    Returns:
        None
    """
    for field in dataclasses.fields(source_ids):
        field_name = field.name
        field_value = getattr(source_ids, field_name)

        # recursively call copy_ids for nested dataclasses
        if dataclasses.is_dataclass(field_value):
            nested_dest = getattr(dest_ids, field_name)
            if not dataclasses.is_dataclass(nested_dest):
                raise TypeError("Both dest_ids and source_ids must be dataclasses.")
            copy_ids(nested_dest, field_value, ignore_missing, keep_source_ids, bytes_to_str)
            if keep_source_ids:
                setattr(source_ids, field_name, None)
        else:
            # check if the field_clazz is present in the destination dataclass
            if not ignore_missing and not hasattr(dest_ids, field_name):
                raise KeyError(f"Field {field_name} is missing from dest_ids.")

            # get the field_clazz type from the destination dataclass
            field_type = get_type_hints(dest_ids)[field_name]

            # convert bytes to str if needed
            if bytes_to_str and isinstance(field_value, bytes) and issubclass(field_type, str):
                field_value = field_value.decode()

            # set the field_clazz value in the destination dataclass
            setattr(dest_ids, field_name, field_value)

            # set the source field_clazz to None if keep_source_ids is True
            if keep_source_ids:
                setattr(source_ids, field_name, None)
