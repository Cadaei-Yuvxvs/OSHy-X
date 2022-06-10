import pytest
from pytest_mock import mocker
from OSHy import *

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

# Test OSHy_data instantiation
## tesla
@pytest.mark.parametrize("tesla", [
    3,7,1.06,9000,True,False,[],('3'),{},'37','7T','3T'
])
def test_OSHy_data_tesla(mocker, tesla):
    mocker.patch(
        'OSHy.ants.image_read',
        return_value="An ANTsImage object"
    )

    mocker.patch(
        'OSHy.glob.glob',
        return_value=["image.nii.gz" for i in range(10)]
    )

    with pytest.raises(Exception) as error_info:
        oshy_dat = OSHy_data(tesla = tesla, 
                            weighting = 'T1w',
                            bimodal = True,
                            crop = True)
    
    assert str(error_info.value) == "tesla must be a string of '3' or '7'."

@pytest.mark.parametrize("tesla", [
    '3','7'
])
def test_OSHy_data_tesla(mocker, tesla):
    mocker.patch(
        'OSHy.ants.image_read',
        return_value="An ANTsImage object"
    )

    mocker.patch(
        'OSHy.glob.glob',
        return_value=["image.nii.gz" for i in range(10)]
    )

    oshy_dat = OSHy_data(tesla = tesla,
                         weighting = 'T1w',
                         bimodal = True,
                         crop = True)
    assert oshy_dat.tesla == tesla

## weighting
@pytest.mark.parametrize("weighting", [
    3,7,1.06,9000,True,False,[],('T1w'),{},'T3w','w1T'
])
def test_OSHy_data_weighting(mocker, weighting):
    mocker.patch(
        'OSHy.ants.image_read',
        return_value="An ANTsImage object"
    )

    mocker.patch(
        'OSHy.glob.glob',
        return_value=["image.nii.gz" for i in range(10)]
    )

    with pytest.raises(Exception) as error_info:
        oshy_dat = OSHy_data(tesla = '7', 
                            weighting = weighting,
                            bimodal = True,
                            crop = True)
    
    assert str(error_info.value) == "weighting must be a string of 'T1w' or 'T2w'."

@pytest.mark.parametrize("weighting,expected_weighting", [
    ('T1w','T1w'),
    ('t1w','T1w'),
    ('T1W','T1w'),
    ('t1W','T1w'),
    ('T2w','T2w'),
    ('t2w','T2w'),
    ('T2W','T2w'),
    ('t2W','T2w')
])
def test_OSHy_data_weighting(mocker, weighting, expected_weighting):
    mocker.patch(
        'OSHy.ants.image_read',
        return_value="An ANTsImage object"
    )

    mocker.patch(
        'OSHy.glob.glob',
        return_value=["image.nii.gz" for i in range(10)]
    )

    oshy_dat = OSHy_data(tesla = '7',
                         weighting = weighting,
                         bimodal = True,
                         crop = True)
    assert oshy_dat.weighting == expected_weighting

## bimodal
@pytest.mark.parametrize("bimodal", [
    7,1.06,[],('T1w'),{},'foo',
])
def test_OSHy_data_bimodal(mocker, bimodal):
    mocker.patch(
        'OSHy.ants.image_read',
        return_value="An ANTsImage object"
    )

    mocker.patch(
        'OSHy.glob.glob',
        return_value=["image.nii.gz" for i in range(10)]
    )

    with pytest.raises(Exception) as error_info:
        oshy_dat = OSHy_data(tesla = '7', 
                            weighting = 'T1w',
                            bimodal = bimodal,
                            crop = True)
    
    assert str(error_info.value) == "bimodal must be a boolean."

@pytest.mark.parametrize("bimodal", [
    True,False
])
def test_OSHy_data_bimodal(mocker, bimodal):
    mocker.patch(
        'OSHy.ants.image_read',
        return_value="An ANTsImage object"
    )

    mocker.patch(
        'OSHy.glob.glob',
        return_value=["image.nii.gz" for i in range(10)]
    )

    oshy_dat = OSHy_data(tesla = '7',
                         weighting = 'T1w',
                         bimodal = bimodal,
                         crop = True)

    assert isinstance(oshy_dat.tesla, bool)

## crop
@pytest.mark.parametrize("crop", [
    7,1.06,[],('T1w'),{},'foo',
])
def test_OSHy_data_crop(mocker, crop):
    mocker.patch(
        'OSHy.ants.image_read',
        return_value="An ANTsImage object"
    )

    mocker.patch(
        'OSHy.glob.glob',
        return_value=["image.nii.gz" for i in range(10)]
    )

    with pytest.raises(Exception) as error_info:
        oshy_dat = OSHy_data(tesla = '7', 
                            weighting = 'T1w',
                            bimodal = True,
                            crop = crop)
    
    assert str(error_info.value) == "crop must be a boolean."

@pytest.mark.parametrize("crop,expected_crop", [
    (True, "cropped"),
    (False, "whole")
])
def test_OSHy_data_bimodal(mocker, crop, expected_crop):
    mocker.patch(
        'OSHy.ants.image_read',
        return_value="An ANTsImage object"
    )

    mocker.patch(
        'OSHy.glob.glob',
        return_value=["image.nii.gz" for i in range(10)]
    )

    oshy_dat = OSHy_data(tesla = '7',
                         weighting = 'T1w',
                         bimodal = True,
                         crop = crop)

    assert oshy_dat.crop == expected_crop


# Create an instance of OSHy_data. Methods are never called outside of this class.
@pytest.fixture
def bimodal_OSHy_data(mocker):
    mocker.patch(
        'OSHy.ants.image_read',
        return_value="An ANTsImage object"
    )

    mocker.patch(
        'OSHy.glob.glob',
        return_value=["image.nii.gz" for i in range(10)]
    )

    oshy_dat = OSHy_data(tesla = '3', 
                        weighting = 'T1w',
                        bimodal = True,
                        crop = True)

    return(oshy_dat)

@pytest.fixture
def unimodal_OSHy_data(mocker):
    mocker.patch(
        'OSHy.ants.image_read',
        return_value="An ANTsImage object"
    )

    mocker.patch(
        'OSHy.glob.glob',
        return_value=["image.nii.gz" for i in range(10)]
    )

    oshy_dat = OSHy_data(tesla = '3', 
                        weighting = 'T1w',
                        bimodal = False,
                        crop = True)

    return(oshy_dat)

# Test Target_img instantiation
@pytest.mark.parametrize(
    "img_filename,out_dir,expected_sub_outdir", 
    [
        ("sub-XX_T1w.nii.gz", "output", "output/sub-XX"),
        ("123_T1w.nii.gz", "output", "output/123"),
        ("123", "output", "output/123"),
        ("foo_bar_abc", "output", "output/foo"),
        (" sub-XX_T1w.nii.gz ", "output", "output/sub-XX"),
        ("sub-XX_T1w.nii.gz", "123", "123/sub-XX"),
        ("sub-XX_T1w.nii.gz", ".", "./sub-XX"),
        ("sub-XX_T1w.nii.gz", " output ", "output/sub-XX"),
    ])
def test_Target_img(mocker,img_filename,out_dir,expected_sub_outdir,bimodal_OSHy_data):
    mocker.patch('OSHy.os.path.exists', return_value=True)
    mocker.patch('OSHy.ants.image_write', return_value=None)
    mocker.patch('OSHy.ants.image_read', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.denoise_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.subprocess.Popen', return_value=subprocess.Popen(["echo", "Hello World!"]))
    mocker.patch('OSHy.os.remove', return_value=None)
    mocker.patch('OSHy.ants.registration', return_value={'invtransforms':[]})
    mocker.patch('OSHy.ants.apply_transforms', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.crop_image', return_value="An ANTsImage object")

    my_image = Target_img(img_file = img_filename, 
                        crop = True,
                        weighting = 'T1w',
                        denoise = True, 
                        b1_bias = True,
                        out_dir = out_dir,
                        oshy_data = bimodal_OSHy_data
                        )

    assert my_image.sub_outdir == expected_sub_outdir

@pytest.mark.parametrize(
    "denoise,b1_bias,crop,expected_preprocess", 
    [
        (True,True,True,"denoised_bias-corrected_cropped_"),
        (True,True,False,"denoised_bias-corrected_"),
        (True,False,False,"denoised_"),
        (False, False, False, ""),
        (False, False, True, "cropped_"),
        (False, True, True, "bias-corrected_cropped_"),
        (True, False, True, "denoised_cropped_")
    ])
def test_Target_img(mocker,denoise,b1_bias,crop,expected_preprocess,bimodal_OSHy_data):
    mocker.patch('OSHy.os.path.exists', return_value=True)
    mocker.patch('OSHy.ants.image_write', return_value=None)
    mocker.patch('OSHy.ants.image_read', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.denoise_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.subprocess.Popen', return_value=subprocess.Popen(["echo", "Hello World!"]))
    mocker.patch('OSHy.os.remove', return_value=None)
    mocker.patch('OSHy.ants.registration', return_value={'invtransforms':[]})
    mocker.patch('OSHy.ants.apply_transforms', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.crop_image', return_value="An ANTsImage object")

    my_image = Target_img(img_file = 'sub-XX_T1w.nii.gz', 
                        crop = crop,
                        weighting = 'T1w',
                        denoise = denoise, 
                        b1_bias = b1_bias,
                        out_dir = 'out_dir',
                        oshy_data = bimodal_OSHy_data
                        )

    assert my_image.preprocess == expected_preprocess

@pytest.mark.parametrize("weighting,expected_weighting", [
    ('T1w','T1w'),
    ('t1w','T1w'),
    ('T1W','T1w'),
    ('t1W','T1w'),
    ('T2w','T2w'),
    ('t2w','T2w'),
    ('T2W','T2w'),
    ('t2W','T2w')
])
def test_Target_img(mocker,weighting,expected_weighting,bimodal_OSHy_data):
    mocker.patch('OSHy.os.path.exists', return_value=True)
    mocker.patch('OSHy.ants.image_write', return_value=None)
    mocker.patch('OSHy.ants.image_read', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.denoise_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.subprocess.Popen', return_value=subprocess.Popen(["echo", "Hello World!"]))
    mocker.patch('OSHy.os.remove', return_value=None)
    mocker.patch('OSHy.ants.registration', return_value={'invtransforms':[]})
    mocker.patch('OSHy.ants.apply_transforms', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.crop_image', return_value="An ANTsImage object")

    my_image = Target_img(img_file = 'sub-XX_T1w.nii.gz', 
                        crop = True,
                        weighting = weighting,
                        denoise = True, 
                        b1_bias = True,
                        out_dir = 'out_dir',
                        oshy_data = bimodal_OSHy_data
                        )

    assert my_image.weighting == expected_weighting

@pytest.mark.parametrize("img_file",
    [
        1,2.0,{'file'},('file'),['file'],True,False,""
    ])
def test_Target_img(mocker,img_file,bimodal_OSHy_data):
    mocker.patch('OSHy.os.path.exists', return_value=True)
    mocker.patch('OSHy.ants.image_write', return_value=None)
    mocker.patch('OSHy.ants.image_read', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.denoise_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.subprocess.Popen', return_value=subprocess.Popen(["echo", "Hello World!"]))
    mocker.patch('OSHy.os.remove', return_value=None)
    mocker.patch('OSHy.ants.registration', return_value={'invtransforms':[]})
    mocker.patch('OSHy.ants.apply_transforms', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.crop_image', return_value="An ANTsImage object")

    with pytest.raises(Exception) as error_info:
        my_image = Target_img(img_file = img_file, 
                            crop = True,
                            weighting = 'T1w',
                            denoise = True, 
                            b1_bias = True,
                            out_dir = 'out_dir',
                            oshy_data = bimodal_OSHy_data
                            )
    assert "Target must be a string" in str(error_info.value)

@pytest.mark.parametrize("out_dir",
    [
        1,2.0,{'file'},('file'),['file'],True,False,""
    ])
def test_Target_img(mocker,out_dir,bimodal_OSHy_data):
    mocker.patch('OSHy.os.path.exists', return_value=True)
    mocker.patch('OSHy.ants.image_write', return_value=None)
    mocker.patch('OSHy.ants.image_read', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.denoise_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.subprocess.Popen', return_value=subprocess.Popen(["echo", "Hello World!"]))
    mocker.patch('OSHy.os.remove', return_value=None)
    mocker.patch('OSHy.ants.registration', return_value={'invtransforms':[]})
    mocker.patch('OSHy.ants.apply_transforms', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.crop_image', return_value="An ANTsImage object")

    with pytest.raises(Exception) as error_info:
        my_image = Target_img(img_file = "sub-XX_T1w.nii.gz", 
                            crop = True,
                            weighting = 'T1w',
                            denoise = True, 
                            b1_bias = True,
                            out_dir = out_dir,
                            oshy_data = bimodal_OSHy_data
                            )
    assert "Output directory must be a string" in str(error_info.value)

@pytest.mark.parametrize("weighting",
    [
        1,2.0,{'file'},('file'),['file'],True,False,""
    ])
def test_Target_img(mocker,weighting,bimodal_OSHy_data):
    mocker.patch('OSHy.os.path.exists', return_value=True)
    mocker.patch('OSHy.ants.image_write', return_value=None)
    mocker.patch('OSHy.ants.image_read', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.denoise_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.subprocess.Popen', return_value=subprocess.Popen(["echo", "Hello World!"]))
    mocker.patch('OSHy.os.remove', return_value=None)
    mocker.patch('OSHy.ants.registration', return_value={'invtransforms':[]})
    mocker.patch('OSHy.ants.apply_transforms', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.crop_image', return_value="An ANTsImage object")

    with pytest.raises(Exception) as error_info:
        my_image = Target_img(img_file = "sub-XX_T1w.nii.gz", 
                            crop = True,
                            weighting = weighting,
                            denoise = True, 
                            b1_bias = True,
                            out_dir = 'out_dir',
                            oshy_data = bimodal_OSHy_data
                            )
    assert "Weighting must be a string" in error_info.value

@pytest.mark.parametrize("crop",
    [
        1,2.0,{'file'},('file'),['file'],""
    ])
def test_Target_img(mocker,crop,bimodal_OSHy_data):
    mocker.patch('OSHy.os.path.exists', return_value=True)
    mocker.patch('OSHy.ants.image_write', return_value=None)
    mocker.patch('OSHy.ants.image_read', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.denoise_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.subprocess.Popen', return_value=subprocess.Popen(["echo", "Hello World!"]))
    mocker.patch('OSHy.os.remove', return_value=None)
    mocker.patch('OSHy.ants.registration', return_value={'invtransforms':[]})
    mocker.patch('OSHy.ants.apply_transforms', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.crop_image', return_value="An ANTsImage object")

    with pytest.raises(Exception) as error_info:
        my_image = Target_img(img_file = "sub-XX_T1w.nii.gz", 
                            crop = crop,
                            weighting = 'T1w',
                            denoise = True, 
                            b1_bias = True,
                            out_dir = 'out_dir',
                            oshy_data = bimodal_OSHy_data
                            )
    assert str(error_info.value) == "crop must be a boolean."

@pytest.mark.parametrize("denoise",
    [
        1,2.0,{'file'},('file'),['file'],""
    ])
def test_Target_img(mocker,denoise,bimodal_OSHy_data):
    mocker.patch('OSHy.os.path.exists', return_value=True)
    mocker.patch('OSHy.ants.image_write', return_value=None)
    mocker.patch('OSHy.ants.image_read', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.denoise_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.subprocess.Popen', return_value=subprocess.Popen(["echo", "Hello World!"]))
    mocker.patch('OSHy.os.remove', return_value=None)
    mocker.patch('OSHy.ants.registration', return_value={'invtransforms':[]})
    mocker.patch('OSHy.ants.apply_transforms', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.crop_image', return_value="An ANTsImage object")

    with pytest.raises(Exception) as error_info:
        my_image = Target_img(img_file = "sub-XX_T1w.nii.gz", 
                            crop = True,
                            weighting = 'T1w',
                            denoise = denoise, 
                            b1_bias = True,
                            out_dir = 'out_dir',
                            oshy_data = bimodal_OSHy_data
                            )
    assert str(error_info.value) == "denoise must be a boolean."

@pytest.mark.parametrize("b1_bias",
    [
        1,2.0,{'file'},('file'),['file'],""
    ])
def test_Target_img(mocker,b1_bias,bimodal_OSHy_data):
    mocker.patch('OSHy.os.path.exists', return_value=True)
    mocker.patch('OSHy.ants.image_write', return_value=None)
    mocker.patch('OSHy.ants.image_read', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.denoise_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.subprocess.Popen', return_value=subprocess.Popen(["echo", "Hello World!"]))
    mocker.patch('OSHy.os.remove', return_value=None)
    mocker.patch('OSHy.ants.registration', return_value={'invtransforms':[]})
    mocker.patch('OSHy.ants.apply_transforms', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.crop_image', return_value="An ANTsImage object")

    with pytest.raises(Exception) as error_info:
        my_image = Target_img(img_file = "sub-XX_T1w.nii.gz", 
                            crop = True,
                            weighting = 'T1w',
                            denoise = True, 
                            b1_bias = b1_bias,
                            out_dir = 'out_dir',
                            oshy_data = bimodal_OSHy_data
                            )
    assert str(error_info.value) == "b1_bias must be a boolean."

# Test methods of Target_img
@pytest.mark.parametrize(
    "img_filename,denoise,b1_bias,crop,out_dir,weight,"\
    "expected_outdir,"\
    "expected_target", 
    [
        ("sub-XX_T1w.nii.gz",True,True,True,"out_dir","T1w",
        "out_dir/sub-XX/sub-XX_",
        "out_dir/sub-XX/sub-XX_denoised_bias-corrected_cropped_T1w.nii.gz"
        ),
        ("foo_T1w.nii.gz",True,True,True,"out_dir","T1w",
        "out_dir/foo/foo_",
        "out_dir/foo/foo_denoised_bias-corrected_cropped_T1w.nii.gz"
        ),
        ("bar",True,True,True,"out_dir","T1w",
        "out_dir/bar/bar_",
        "out_dir/bar/bar_denoised_bias-corrected_cropped_T1w.nii.gz"
        ),
        ("42_ses-01_T1w.nii.gz",True,True,True,"out_dir","T1w",
        "out_dir/42/42_",
        "out_dir/42/42_denoised_bias-corrected_cropped_T1w.nii.gz"
        ),
        ("sub-01_T1w.nii.gz",True,True,True,"out_dir","T2w",
        "out_dir/sub-01/sub-01_",
        "out_dir/sub-01/sub-01_denoised_bias-corrected_cropped_T2w.nii.gz"
        ),
        ("sub-01_T1w.nii.gz",True,True,True,"9000","T2w",
        "9000/sub-01/sub-01_",
        "9000/sub-01/sub-01_denoised_bias-corrected_cropped_T2w.nii.gz"
        ),
        ("sub-01_T1w.nii.gz",True,True,True,".","T2w",
        "./sub-01/sub-01_",
        "./sub-01/sub-01_denoised_bias-corrected_cropped_T2w.nii.gz"
        ),
        ("sub-01_T1w.nii.gz",True,False,False,"out_dir","T2w",
        "out_dir/sub-01/sub-01_",
        "out_dir/sub-01/sub-01_denoised_T2w.nii.gz"
        ),
        ("sub-01_T1w.nii.gz",True,True,False,"out_dir","T2w",
        "out_dir/sub-01/sub-01_",
        "out_dir/sub-01/sub-01_denoised_bias-corrected_T2w.nii.gz"
        ),
        ("sub-01_T1w.nii.gz",False,True,True,"out_dir","T2w",
        "out_dir/sub-01/sub-01_",
        "out_dir/sub-01/sub-01_bias-corrected_cropped_T2w.nii.gz"
        ),
        ("sub-01_T1w.nii.gz",False,False,True,"out_dir","T2w",
        "out_dir/sub-01/sub-01_",
        "out_dir/sub-01/sub-01_cropped_T2w.nii.gz"
        ),
        ("sub-01_T1w.nii.gz",True,False,True,"out_dir","T2w",
        "out_dir/sub-01/sub-01_",
        "out_dir/sub-01/sub-01_denoised_cropped_T2w.nii.gz"
        )
    ])
def test_run_JLF2_bimodal(mocker, bimodal_OSHy_data,img_filename,denoise,
                          b1_bias,crop,out_dir,weight,expected_outdir,
                          expected_target):
    mocker.patch('OSHy.os.path.exists', return_value=True)
    mocker.patch('OSHy.ants.image_write', return_value=None)
    mocker.patch('OSHy.ants.image_read', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.denoise_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.subprocess.Popen', return_value=subprocess.Popen(["echo", "Hello World!"]))
    mocker.patch('OSHy.os.remove', return_value=None)
    mocker.patch('OSHy.ants.registration', return_value={'invtransforms':[]})
    mocker.patch('OSHy.ants.apply_transforms', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.crop_image', return_value="An ANTsImage object")

    my_image = Target_img(img_file = img_filename, 
                        crop = crop,
                        weighting = weight,
                        denoise = denoise, 
                        b1_bias = b1_bias,
                        out_dir = out_dir,
                        oshy_data = bimodal_OSHy_data
                        )

    spy = mocker.spy(subprocess, 'Popen')
    assert my_image.run_JLF2(5) == None

    spy.assert_called_once_with(
        [
            "antsJointLabelFusion2.sh", 
            "-d", "3", "-j", 5,
            "-o", expected_outdir,
            "-t", expected_target,
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-b" ,"1", "-b", "2", "-b" "3", "-b", "4", "-a", "4", "-s", "10"], 
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
    )

def test_run_JLF2_unimodal(mocker, unimodal_OSHy_data):
    mocker.patch('OSHy.os.path.exists', return_value=True)
    mocker.patch('OSHy.ants.image_write', return_value=None)
    mocker.patch('OSHy.ants.image_read', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.denoise_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.subprocess.Popen', return_value=subprocess.Popen(["echo", "Hello World!"]))
    mocker.patch('OSHy.os.remove', return_value=None)
    mocker.patch('OSHy.ants.registration', return_value={'invtransforms':[]})
    mocker.patch('OSHy.ants.apply_transforms', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.crop_image', return_value="An ANTsImage object")
    my_image = Target_img(img_file = 'sub-XX_T1w.nii.gz', 
                        crop = True,
                        weighting = 'T1w',
                        denoise = True, 
                        b1_bias = True,
                        out_dir = 'out_dir',
                        oshy_data = unimodal_OSHy_data
                        )

    spy = mocker.spy(subprocess, 'Popen')
    assert my_image.run_JLF2(5) == None

    spy.assert_called_once_with(
        [
            "antsJointLabelFusion2.sh", 
            "-d", "3", "-j", 5,
            "-o", "out_dir/sub-XX/sub-XX_",
            "-t", "out_dir/sub-XX/sub-XX_denoised_bias-corrected_cropped_T1w.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-g", "image.nii.gz", "-l", "image.nii.gz",
            "-b" ,"1", "-b", "2", "-b" "3", "-b", "4", "-a", "4", "-s", "10"], 
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
    )

def test_create_mosaic(mocker, bimodal_OSHy_data):
    mocker.patch('OSHy.os.path.exists', return_value=True)
    mocker.patch('OSHy.ants.image_write', return_value=None)
    mocker.patch('OSHy.ants.image_read', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.denoise_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.subprocess.Popen', return_value=subprocess.Popen(["echo", "Hello World!"]))
    mocker.patch('OSHy.os.remove', return_value=None)
    mocker.patch('OSHy.ants.registration', return_value={'invtransforms':[]})
    mocker.patch('OSHy.ants.apply_transforms', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.crop_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.plot', return_value=None)

    my_image = Target_img(img_file = "sub-XX.nii.gz", 
                        crop = True,
                        weighting = 'T1w',
                        denoise = True, 
                        b1_bias = True,
                        out_dir = "output",
                        oshy_data = bimodal_OSHy_data
                        )

    my_image.run_JLF2(1)
    
    spy = mocker.spy(ants, 'plot')
 
    assert my_image.create_mosaic() == None

    spy.assert_called_once_with("An ANTsImage object", "An ANTsImage object", overlay_cmap='jet', 
        overlay_alpha=0.8, axis=1, nslices = 16, title="sub-XX", 
        filename="output/sub-XX/sub-XX_mosaic.png")

def test_calc_volume(mocker, bimodal_OSHy_data):
    mocker.patch('OSHy.os.path.exists', return_value=True)
    mocker.patch('OSHy.ants.image_write', return_value=None)
    mocker.patch('OSHy.ants.image_read', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.denoise_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.subprocess.Popen', return_value=subprocess.Popen(["echo", "Hello World!"]))
    mocker.patch('OSHy.os.remove', return_value=None)
    mocker.patch('OSHy.ants.registration', return_value={'invtransforms':[]})
    mocker.patch('OSHy.ants.apply_transforms', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.crop_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.plot', return_value=None)
    mocker.patch('OSHy.glob.glob', return_value=["globbed"])

    my_image = Target_img(img_file = "sub-XX.nii.gz", 
                        crop = True,
                        weighting = 'T1w',
                        denoise = True, 
                        b1_bias = True,
                        out_dir = "output",
                        oshy_data = bimodal_OSHy_data
                        )

    my_image.run_JLF2(1)
    my_image.create_mosaic()

    spy = mocker.spy(subprocess, 'Popen')

    assert my_image.calc_volume() == None

    spy.assert_called_once_with(
            [
                "ImageMath", "3",
                "output/sub-XX/sub-XX_volumes.csv", "LabelStats",
                "globbed",
                "output/sub-XX/sub-XX_denoised_bias-corrected_cropped_T1w.nii.gz"
            ], 
            stdout=subprocess.PIPE, stdin=subprocess.PIPE, 
            stderr=subprocess.STDOUT)

def test_resample_segmentation(mocker, bimodal_OSHy_data):
    mocker.patch('OSHy.os.path.exists', return_value=True)
    mocker.patch('OSHy.ants.image_write', return_value=None)
    mocker.patch('OSHy.ants.image_read', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.denoise_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.subprocess.Popen', return_value=subprocess.Popen(["echo", "Hello World!"]))
    mocker.patch('OSHy.os.remove', return_value=None)
    mocker.patch('OSHy.ants.registration', return_value={'invtransforms':[]})
    mocker.patch('OSHy.ants.apply_transforms', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.crop_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.plot', return_value=None)
    mocker.patch('OSHy.glob.glob', return_value=["globbed"])
    mocker.patch('OSHy.ants.resample_image_to_target', return_value="Resampled to target!")

    my_image = Target_img(img_file = "sub-XX.nii.gz", 
                        crop = True,
                        weighting = 'T1w',
                        denoise = True, 
                        b1_bias = True,
                        out_dir = "output",
                        oshy_data = bimodal_OSHy_data
                        )

    my_image.run_JLF2(1)
    my_image.create_mosaic()
    my_image.calc_volume()

    spy_resample = mocker.spy(ants, 'resample_image_to_target')
    spy_write = mocker.spy(ants, 'image_write')

    assert my_image.resample_segmentation() == None

    spy_resample.assert_called_once_with(
               "An ANTsImage object", "An ANTsImage object", interp_type="genericLabel"
            )

    spy_write.assert_called_once_with(
        "Resampled to target!", 
        filename = "output/sub-XX/sub-XX_resampled_Labels"\
                    ".nii.gz"
    )

def test_threshold_structures(mocker, bimodal_OSHy_data):
    mocker.patch('OSHy.os.path.exists', return_value=True)
    mocker.patch('OSHy.ants.image_write', return_value=None)
    mocker.patch('OSHy.ants.image_read', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.denoise_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.subprocess.Popen', return_value=subprocess.Popen(["echo", "Hello World!"]))
    mocker.patch('OSHy.os.remove', return_value=None)
    mocker.patch('OSHy.ants.registration', return_value={'invtransforms':[]})
    mocker.patch('OSHy.ants.apply_transforms', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.crop_image', return_value="An ANTsImage object")
    mocker.patch('OSHy.ants.threshold_image', return_value="Thresholded target!")
    mocker.patch('OSHy.ants.plot', return_value=None)
    mocker.patch('OSHy.glob.glob', return_value=["globbed"])
    mocker.patch('OSHy.ants.resample_image_to_target', return_value="Resampled to target!")

    my_image = Target_img(img_file = "sub-XX.nii.gz", 
                        crop = True,
                        weighting = 'T1w',
                        denoise = True, 
                        b1_bias = True,
                        out_dir = "output",
                        oshy_data = bimodal_OSHy_data
                        )

    my_image.run_JLF2(1)
    my_image.create_mosaic()
    my_image.calc_volume()
    my_image.resample_segmentation()
    
    spy_threshold = mocker.spy(ants, 'threshold_image')
    spy_write = mocker.spy(ants, 'image_write')

    assert my_image.threshold_structures() == None

    spy_threshold.assert_any_call("Resampled to target!", 1, 2)
    spy_threshold.assert_any_call("Resampled to target!", 3, 4)

    spy_write.assert_any_call("Thresholded target!", 
    filename="output/sub-XX/sub-XX_hypothalamus.nii.gz"
    )
    spy_write.assert_any_call("Thresholded target!", 
    filename="output/sub-XX/sub-XX_fornix.nii.gz"
    )