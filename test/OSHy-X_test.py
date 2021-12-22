import pytest
from pytest_mock import mocker
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

oshy_dat = None
# Create an instance of OSHy_data. Methods are never called outside of this class.
@pytest.fixture
def bimodal_OSHy_data(mocker):
    mocker.patch(
        'OSHyX.ants.image_read',
        return_value="An ANTsImage object"
    )

    mocker.patch(
        'OSHyX.glob.glob',
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
        'OSHyX.ants.image_read',
        return_value="An ANTsImage object"
    )

    mocker.patch(
        'OSHyX.glob.glob',
        return_value=["image.nii.gz" for i in range(10)]
    )

    oshy_dat = OSHy_data(tesla = '3', 
                        weighting = 'T1w',
                        bimodal = False,
                        crop = True)

    return(oshy_dat)


# my_image.run_JLF2(nprocs=args['nthreads'])

# if convert_to_bool(args['mosaic']):
#     my_image.create_mosaic()

# my_image.calc_volume()
# my_image.resample_segmentation()
# my_image.threshold_structures()


@pytest.mark.parametrize(
    "img_filename,denoise,b1_bias,crop,out_dir,weight,expected_outdir,expected_target", 
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
        ("sub-XX_T1w.nii.gz",True,True,True,"out_dir","T2w",
        "out_dir/bar/bar_",
        "out_dir/bar/bar_denoised_bias-corrected_cropped_T2w.nii.gz"
        ),
        ("sub-XX_T1w.nii.gz",True,True,True,"9000","T2w",
        "9000/bar/bar_",
        "9000/bar/bar_denoised_bias-corrected_cropped_T2w.nii.gz"
        ),
        ("sub-XX_T1w.nii.gz",True,True,True,".","T2w",
        "./bar/bar_",
        "./bar/bar_denoised_bias-corrected_cropped_T2w.nii.gz"
        ),
        ("sub-XX_T1w.nii.gz",True,False,False,"out_dir","T2w",
        "out_dir/bar/bar_",
        "out_dir/bar/bar_denoised_T2w.nii.gz"
        ),
        ("sub-XX_T1w.nii.gz",True,True,False,"out_dir","T2w",
        "out_dir/bar/bar_",
        "out_dir/bar/bar_denoised_bias-corrected_T2w.nii.gz"
        ),
        ("sub-XX_T1w.nii.gz",False,True,True,"out_dir","T2w",
        "out_dir/bar/bar_",
        "out_dir/bar/bar_bias-corrected_cropped_T2w.nii.gz"
        ),
        ("sub-XX_T1w.nii.gz",False,False,True,"out_dir","T2w",
        "out_dir/bar/bar_",
        "out_dir/bar/bar_cropped_T2w.nii.gz"
        ),
        ("sub-XX_T1w.nii.gz",True,False,True,"out_dir","T2w",
        "out_dir/bar/bar_",
        "out_dir/bar/bar_denoised_cropped_T2w.nii.gz"
        )
    ])
def test_run_JLF2_bimodal(mocker, bimodal_OSHy_data,img_filename,denoise,
                          b1_bias,crop,out_dir,weight,expected_outdir,
                          expected_target):
    mocker.patch('OSHyX.os.path.exists', return_value=True)
    mocker.patch('OSHyX.ants.image_write', return_value=None)
    mocker.patch('OSHyX.ants.image_read', return_value="An ANTsImage object")
    mocker.patch('OSHyX.ants.denoise_image', return_value="An ANTsImage object")
    mocker.patch('OSHyX.subprocess.Popen', return_value=subprocess.Popen(["echo", "Hello World!"]))
    mocker.patch('OSHyX.os.remove', return_value=None)
    mocker.patch('OSHyX.ants.registration', return_value={'invtransforms':[]})
    mocker.patch('OSHyX.ants.apply_transforms', return_value="An ANTsImage object")
    mocker.patch('OSHyX.ants.crop_image', return_value="An ANTsImage object")

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
        mocker.patch('OSHyX.os.path.exists', return_value=True)
        mocker.patch('OSHyX.ants.image_write', return_value=None)
        mocker.patch('OSHyX.ants.image_read', return_value="An ANTsImage object")
        mocker.patch('OSHyX.ants.denoise_image', return_value="An ANTsImage object")
        mocker.patch('OSHyX.subprocess.Popen', return_value=subprocess.Popen(["echo", "Hello World!"]))
        mocker.patch('OSHyX.os.remove', return_value=None)
        mocker.patch('OSHyX.ants.registration', return_value={'invtransforms':[]})
        mocker.patch('OSHyX.ants.apply_transforms', return_value="An ANTsImage object")
        mocker.patch('OSHyX.ants.crop_image', return_value="An ANTsImage object")
        my_image = Target_img(img_file = 'sub-XX_T1w.nii.gz', 
                            crop = True,
                            weighting = 'T1w',
                            denoise = True, 
                            b1_bias = True,
                            out_dir = 'out_dir',
                            oshy_data = bimodal_OSHy_data
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
