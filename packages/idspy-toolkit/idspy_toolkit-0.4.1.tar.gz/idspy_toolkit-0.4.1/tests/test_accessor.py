import pytest
import dataclasses
from typing import Optional
from numpy import ndarray

from tests.classes_skels import *
from idspy_toolkit.accessor import get_ids_value_from_string, \
    set_ids_value_from_string, is_list_member, copy_ids, get_type_arg
from idspy_toolkit.toolkit import list_ids_members

@dataclasses.dataclass
class SubSubClass:
    member_subsubclass_aa: Optional[str] = dataclasses.field(default=""
                                                             )
    member_subsubclass_bb: Optional[int] = dataclasses.field(default=999999999
                                                             )
    member_subsubclass_cc: Optional[float] = dataclasses.field(default=None
                                                               )


@dataclasses.dataclass
class SubClass:
    member_subclass: Optional[SubSubClass] = dataclasses.field(
        default=None
    )


@dataclasses.dataclass
class BaseClass:
    list_member: list[SubClass] = dataclasses.field(
        default_factory=list,

    )
    list_member_foreign: list["SubclassNested"] = dataclasses.field(
        default_factory=list,

    )
    nda_member: Optional[ndarray[(int, int), float]] = dataclasses.field(
        default=None,
    )

    @dataclasses.dataclass
    class SubclassNested:
        member_subsubclass_aa: Optional[str] = dataclasses.field(default=""
                                                                 )


@dataclasses.dataclass
class DbgSubDataClass:
    subfield1: str
    subfield2: int


@dataclasses.dataclass
class DbgMainDataClass:
    field1: str
    field2: int
    subfield_list: list[DbgSubDataClass]


@dataclasses.dataclass(slots=True)
class SubDataClass:
    subfield1: str
    subfield2: int


@dataclasses.dataclass(slots=True)
class MainDataClass:
    field1: str
    field2: int
    subfield: SubDataClass
    subfield_list: list[SubDataClass]


@dataclasses.dataclass
class MyClass:
    my_list: list[int]
    my_string: str

def test_get_type_arg():
    assert get_type_arg(MyClass, "my_list") == (int, True)
    assert get_type_arg(MyClass, "my_string") == (str, False)
    with pytest.raises(KeyError):
        get_type_arg(MyClass, "nonexistent_field")


def test_is_list_member():
    assert is_list_member(BaseClass, "list_member") is True
    assert is_list_member(BaseClass, "list_member_foreign") is True
    assert is_list_member(BaseClass, "nda_member") is False
    assert is_list_member(MainDataClass, "subfield_list") is True

def test_get_ids_value_from_string():
    # create source dataclass with nested dataclass containing list
    source_subfield_list = [
        SubDataClass("subfield1_1", 1),
        SubDataClass("subfield1_2", 2),
        SubDataClass("subfield1_3", 3),
        SubDataClass("subfield1_4", 4),
        SubDataClass("subfield1_5", 5)
    ]
    source_dataclass = MainDataClass("field1", 123, SubDataClass("subfield1", 1), source_subfield_list)

    # create destination dataclass with different values
    dest_subfield_list = [
        SubDataClass("dest_subfield1_1", 10),
        SubDataClass("dest_subfield1_2", 20),
        SubDataClass("dest_subfield1_3", 30),
        SubDataClass("dest_subfield1_4", 40),
        SubDataClass("dest_subfield1_5", 50)
    ]
    dest_dataclass = MainDataClass("dest_field1", 456, SubDataClass("dest_subfield1", 100), dest_subfield_list)

    # copy source to destination
    copy_ids(dest_dataclass, source_dataclass)
    with pytest.raises(KeyError):
        get_ids_value_from_string(source_dataclass, "/MainDataClass/subfield_list#000000/")
    with pytest.raises(KeyError):
        get_ids_value_from_string(source_dataclass, "/MainDataClass/subfield_list#000001/")
    with pytest.raises(KeyError):
        get_ids_value_from_string(source_dataclass, "/MainDataClass/subfield_list#000001")

    # check that destination dataclass now has same values as source dataclass
    assert get_ids_value_from_string(dest_dataclass, "field1") == "field1"
    assert get_ids_value_from_string(dest_dataclass, "field2") == 123
    assert get_ids_value_from_string(dest_dataclass, "subfield/subfield1") == "subfield1"
    assert get_ids_value_from_string(dest_dataclass, "subfield/subfield2") == 1
    assert get_ids_value_from_string(source_dataclass, "subfield_list#000001/subfield1") == "subfield1_2"

def test_set_ids_value_from_string():
    # Create a test instance of MainDataClass
    test_mc = DbgMainDataClass(
        field1="value1",
        field2=123,
        subfield_list=[
            DbgSubDataClass(subfield1="subvalue1", subfield2=456),
            DbgSubDataClass(subfield1="subvalue2", subfield2=789)
        ]
    )

    # Test setting an existing value
    set_ids_value_from_string(test_mc, "field1", "new_value")
    assert test_mc.field1 == "new_value"

    # Test setting a value in a subfield
    set_ids_value_from_string(test_mc, "subfield_list#0000/subfield2", 999)
    assert test_mc.subfield_list[0].subfield2 == 999

    # Test creating a missing subfield
    set_ids_value_from_string(test_mc, "subfield_list#0002/subfield1", "new_subvalue")
    assert test_mc.subfield_list[2].subfield1 == "new_subvalue"

    # Test setting a value in a subfield of type list without number
    with pytest.raises(AttributeError):
        set_ids_value_from_string(test_mc, "subfield_list/subfield2", 777)

    # Test setting a value in a subfield of type list without number with create_missing=False
    with pytest.raises(AttributeError):
        set_ids_value_from_string(test_mc, "subfield_list/subfield2", 777, create_missing=False)

    # Test setting a value in a non-list subfield with create_missing=True
    with pytest.raises(AttributeError):
        set_ids_value_from_string(test_mc, "field3/subfield1", "new_value", create_missing=True)

    # Test setting a value in a list subfield without specifying an index
    with pytest.raises(ValueError):
        set_ids_value_from_string(test_mc, "subfield_list", "new_value")

    # Test setting a value in a list subfield with an invalid index
    with pytest.raises(AttributeError):
        set_ids_value_from_string(test_mc, "subfield_list#0001/subfield2#99", 999)
