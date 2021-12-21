import pytest
import pytest_mock
from OSHyX import *

# Test convert_to_bool
@pytest.mark.parametrize("boolstrings", [
    "true",
    "True",
    "tRue",
    "TRUE",
])

def test_convert_to_bool(boolstrings):
    assert convert_to_bool(boolstrings)

@pytest.mark.parametrize("boolstrings", [
    "false",
    "False",
    "faLse",
    "FALSE",
])

def test_convert_to_bool(boolstrings):
    assert not convert_to_bool(boolstrings)

@pytest.mark.parametrize("boolstrings", [
    "falsee",
    "Frue",
    "Tralse",
    "SUPER",
    "",
    " ",
    "a",
    1,
    False,
    True,
    [],
    {}
])

def test_convert_to_bool(boolstrings):
    with pytest.raises(Exception) as error_info:
        convert_to_bool(boolstrings)
    assert str(error_info.value) == 'Please check your spelling for True or False.'

@pytest.mark.parametrize("boolstrings", [
    1,
    False,
    True,
    [],
    {}
])

def test_convert_to_bool(boolstrings):
    with pytest.raises(Exception) as error_info:
        convert_to_bool(boolstrings)
    assert str(error_info.value) == 'Input must be a string.'

# Mock functions

mocker.patch(
    'OSHyX.ants.image_read',
    return_value=ants.make_image((100,100,100))
)

mocker.patch(
    'OSHyX.glob.glob',
    return_value=["image.nii.gz" for i in range(10)]
)

# Create an instance of OSHy_data. Methods are never called outside of the class.
oshy_dat = OSHy_data(tesla = '3', 
                    weighting = 'T1w',
                    bimodal = True,
                    crop = True)
# Create an instance of Target_img

# my_image = Target_img(img_file = 'sub-XX_T1w.nii.gz', 
#                       crop = True,
#                       weighting = 'T1w',
#                       denoise = True, 
#                       b1_bias = True,
#                       out_dir = 'out_dir',
#                       oshy_data = oshy_dat
#                       )
