import pytest
import pytest_mock
from code.OSHy import convert_to_bool

@pytest.mark.parametrize("boolstrings", [
    "true",
    "True",
    "tRue",
    "TRUE",
])

def test_convert_to_bool:
    assert convert_to_bool(boolstrings)

@pytest.mark.parametrize("boolstrings", [
    "false",
    "False",
    "faLse",
    "FALSE",
])

def test_convert_to_bool:
    assert not convert_to_bool(boolstrings)

@pytest.mark.parametrize("boolstrings", [
    "falsee",
    "Frue",
    "Tralse",
    "SUPER",
    "",
    " ",
])

def test_convert_to_bool:
    with pytest.raises(Exception) as error_info:
        convert_to_bool(boolstrings)
    assert str(error_info.value) == 'Please check your spelling for True or False.'

if __name__ == "__main__":

    pass