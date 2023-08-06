import inspect
import dataclasses
from typing import Union, Type, TypeVar, Any, get_args
from typing_extensions import Protocol
import numpy as np

from idspy_toolkit.snippets import is_dataclass_field, is_dataclass_instance, _format_ids_substring
from idspy_toolkit.utils import snake2camel, extract_ndarray_info, _imas_default_values
from idspy_toolkit.accessor import get_type_arg


class DataClass(Protocol):
    __dataclass_fields__: dict[str, Any]


DC = TypeVar("DC", bound=DataClass)



def get_ids_classes_as_dict(module_alias) -> dict[str, Type]:
    """
    Extracts the names of all dataclasses in the specified module.

    Args:
        module_alias (module): A module object or an alias to a module.

    Returns:
        str:dataclass]: A dictionnary containing the names of all dataclasses
        defined in the module as key and the associated dataclass as value.

    Raises:
        TypeError: If module_alias is not a valid module object or alias.

    Example:
        >>> import my_module
        >>> get_ids_classes_as_dict(my_module)
        {'Person':Person, 'Address':Address}
    """
    if not inspect.ismodule(module_alias):
        raise TypeError(f"module_alias should be a module object or alias, not {type(module_alias)}")
    return {x[0]: x[1] for x in inspect.getmembers(module_alias) if
            inspect.isclass(x[1]) and hasattr(x[1], '__dataclass_fields__')}


def list_ids_members(ids: Type[DC], ) -> list:
    """
    List all attributes' IDs of a dataclass instance and its nested dataclass instances.


    :param ids: A dataclass instance containing attributes to list.
    :type ids: dataclasses

    :return: A list of named groups for each attribute in the given dataclass instance.
    :rtype: list

    :raises: None

    :Example:

    >>> from dataclasses import dataclass
    >>> @dataclass
    ... class Member:
    ...     name: str
    ...     age: int
    ...
    >>> @dataclass
    ... class Group:
    ...     name: str
    ...     members: List[Member]
    ...
    >>> m1 = Member('John', 30)
    >>> m2 = Member('Alice', 25)
    >>> group = Group('Engineering', [m1, m2])
    >>> list_ids_members(group)
    ['Group/name', 'Group/members#0000/name', 'Group/members#0000/age', 'Group/members#0001/name', 'Group/members#0001/age']
    """
    list_members: list = []

    def _list_ids(current_ids: Type[DC], list_attrs: list,
                  named_group: Union[str, None] = None,
                  flat_idx: Union[int, None] = None,
                  delimiter: str = "/") -> None:
        """
        Recursive function to list all attributes' IDs of a dataclass instance and its nested dataclass instances.

        :param current_ids: A dataclass instance to list the IDs.
        :type current_ids: dataclasses

        :param list_attrs: A list of attribute IDs.
        :type list_attrs: list

        :param named_group: A named group to create a root group for the attribute IDs.
        :type named_group: str

        :param flat_idx: An index to distinguish multiple attributes with the same name.
        :type flat_idx: Union[int, None]

        :param delimiter: A delimiter to separate attribute names in the IDs.
        :type delimiter: str

        :return: None

        :raises: TypeError if the input parameter is not a dataclass instance.

        """
        if named_group is None:
            root_grp = delimiter + str(type(current_ids)).split(".")[-1][:-2]
        else:
            root_grp = named_group

        if flat_idx is not None:
            root_grp = "{0}{1}".format(root_grp, _format_ids_substring(flat_idx))

        # do not print sub ids "root path"
        # list_attrs.append(root_grp)
        for field in dataclasses.fields(current_ids):
            field_name = field.name
            field_value = getattr(current_ids, field_name)
            named_group = root_grp + delimiter + field_name
            if isinstance(field_value, (list, tuple)):
                if len(field_value) == 0:
                    continue
                if is_dataclass_instance(field_value[0]):
                    for i, sub_ids in enumerate(field_value):
                        _list_ids(sub_ids, list_attrs, named_group=named_group,
                                  flat_idx=i)
            elif is_dataclass_instance(field_value):
                # call recursive function
                _list_ids(field_value, list_attrs, named_group=named_group)
            else:
                list_attrs.append(named_group)

    # browse the ids
    _list_ids(ids, list_members, )
    return list_members


def __fill_default_values_ids(parent_ids, member_name: str, member_type: Type,
                              root_type: Union[Type, None]):
    """
    populate the member 'member_name' of the dataclass 'parent_ids' with a variable of type 'member_type'.
    the 'root_type' argument is used internally in case of recursive calls
    :param parent_ids: parent class variable
    :param member_name: class member, as string
    :param member_type: member type
    :param root_type: none of type of the member in the root class
    :return: none, operation is made in-place
    :TODO: handle numpy.array
    """

    # if current member is already filled, let it like that
    if getattr(parent_ids, member_name) is not None:
        return

    # if current member is of type list, generate one item of the given type and store is as a 1 element list
    if isinstance(getattr(parent_ids, member_name), (list, tuple)):
        list_item = member_type()
        fill_default_values_ids(list_item, member_type)
        setattr(parent_ids,
                member_name,
                [list_item, ]
                )
    else:
        # defaut case, type of the item can be reached
        try:
            if "ndarray" in str(member_type):
                shape, dtype = extract_ndarray_info(str(member_type))
                setattr(parent_ids,
                        member_name,
                        np.ndarray(shape=shape, dtype=dtype)
                        )
            else:
                setattr(parent_ids,
                        member_name,
                        member_type()
                        )
        except TypeError:

            # otherwise we suppose it's a forwardref and so type can be infered from name
            try:
                setattr(parent_ids,
                        member_name,
                        getattr(root_type, snake2camel(member_name))()
                        )
            # and final case, current item is of type list[item] or deeper kind of list
            except AttributeError:
                if not get_args(member_type):
                    raise
                setattr(parent_ids,
                        member_name,
                        [_imas_default_values(get_args(member_type)[0]), ]
                        )


def fill_default_values_ids(new_ids, root_type: Union[Type, None] = None, fill_list: bool = False) -> None:
    """
        recursively populate an IDS at all levels with default values.
        IDS populating is made in-place
        Usage :
            import ids_gyrokinetics as gkids
            my_ids = gkids.Gyrokinetics()
            populate_new_ids(my_ids)
    :param new_ids:
    :param root_type:
    :param fill_list:
    :return:
    :TODO: check bytes and str
    :TODO: check ndarray generation and not list
    """
    for field_vars in dataclasses.fields(new_ids):
        field_type, _ = get_type_arg(new_ids, field_vars)
        field_name = field_vars.name
        field_value = getattr(new_ids, field_name)

        __fill_default_values_ids(new_ids, field_name, field_type, root_type)

        if isinstance(field_value, (list, tuple)):
            if fill_list is False:
                continue
            else:
                list_item = field_type()
                fill_default_values_ids(list_item, fill_list=True)
                field_value.append(list_item)

        if not dataclasses.is_dataclass(field_value):
            continue

        fill_default_values_ids(getattr(new_ids, field_name), field_type)
