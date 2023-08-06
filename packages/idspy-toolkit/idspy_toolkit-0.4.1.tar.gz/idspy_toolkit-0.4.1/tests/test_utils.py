import dataclasses

import pytest
from idspy_toolkit.utils import snake2camel, camel2snake, _imas_default_values, get_field_with_type, extract_ndarray_info
from tests.classes_skels import ClassListNested, ClassListNightmare, ClassListNestedList


def test_snake2camel():
    # Test the snake2camel function
    assert snake2camel("device_type") == "DeviceType"
    assert snake2camel("first_name") == "FirstName"
    assert snake2camel("my_snake_string") == "MySnakeString"
    assert snake2camel("all_caps") == "AllCaps"
    assert snake2camel("") == ""


def test_camel2snake():
    # Test the camel2snake function
    assert camel2snake("DeviceType") == "device_type"
    assert camel2snake("FirstName") == "first_name"
    assert camel2snake("MySnakeString") == "my_snake_string"
    assert camel2snake("AllCaps") == "all_caps"
    assert camel2snake("") == ""


def test_imas_default_values():
    # Test the _imas_default_values function
    assert _imas_default_values(int) == 999999999
    assert _imas_default_values(float) == 9.0e40
    assert _imas_default_values(str) == ""
    assert _imas_default_values(complex) == complex(9.0e40, -9.0e40)
    assert _imas_default_values(list) == []
    #  assert _imas_default_values([int,]) == [999999999,]
    assert _imas_default_values(bool) is False


def test_class_type_extraction():
    test1 = ClassListNested()
    with pytest.raises(TypeError):
        get_field_with_type(test1, ClassListNested.space)
    assert get_field_with_type(test1, "space") == (567, int)
    field_space = [x for x in dataclasses.fields(test1) if x.name == "space"][0]
    assert get_field_with_type(test1, field_space) == (567, int)

def test_extract_ndarray():
    good_str = r"numpy.ndarray[(<class 'int'>,), float]"
    good_str_2 = r"numpy.ndarray[(<class 'int'>, <class 'int'>,), float]"
    bad_str_1 = r"numpy.ndarray[float, float]"
    bad_str_2 = r"numpy.ndarray[(<class 'float'>,), float]"
    extract_ndarray_info(good_str)
    extract_ndarray_info(good_str_2)
    with pytest.raises(ValueError):
        extract_ndarray_info(bad_str_1)
    with pytest.raises(ValueError):
        extract_ndarray_info(bad_str_2)
