# Open Source Hypothalamic-ForniX (OSHy-X) Atlases and Segmentation Tool for 3T and 7T

[![DOI](https://joss.theoj.org/papers/10.21105/joss.04368/status.svg)](https://doi.org/10.21105/joss.04368)

*Version 0.4*

OSHy-X is an atlas repository (https://osf.io/zge9t) and containerised Python script that automatically segments the hypothalamus and fornix at 3T and 7T in both T1w and T2w scans. It is designed to only run inside a container. See [below for installation instructions](#Installation).

OSHy-X is published in the Journal of Open Source Software. Read the paper [here](https://doi.org/10.21105/joss.04368).

![The user inputs a T1w or T2w image. They are given the options for denoising, B1 bias field correction and image cropping. After Joint Label Fusion, the given output are the label, volume and mosaic files.](Media/OSHy_figure_1.GIF "OSHy pipeline")

***

## Installation

You have the option of running OSHy-X via NeuroDesk, a Docker container by itself, or an Apptainer. OSHy-X (and `OSHy.py`) is not designed to run outside of a container.

### Neurodesk

Follow instructions [here](https://neurodesk.github.io/docs/neurodesktop/getting-started/) to install Neurodesk.

### Docker

1. Install Docker [here](https://docs.docker.com/get-docker/).
2. Open a terminal and run:

`docker pull jerync/oshyx_0.4:20220614`
To pull the container. Or run: 

`docker run --rm -v /path/to/data/folder/:/data/ jerync/oshyx_0.4:20220614 --target /data/input_file.nii.gz --outdir /data/output_directory`

### Apptainer (formerly Singularity)
1. Install Apptainer [here](http://apptainer.org/docs/user/main/quick_start.html#quick-installation-steps).
2. Open a terminal and run 
`apptainer build oshyx_0.4.sif docker://jerync/oshyx_0.4:20220614`
to build the container. 

## Usage


### Docker and Apptainer

```
Usage: docker run --rm -v /path/to/data:/data jerync/oshyx_0.4:20220614 
               [-h] -t TARGET [TARGET ...] -o OUTDIR [-c CROP] [-w WEIGHTING]
               [-d DENOISE] [-f FIELDCORRECTION] [-m MOSAIC] [-x TESLA]
               [-b BIMODAL] [-n NTHREADS]

       apptainer run --bind /path/to/data:/data oshyx_0.4.sif 
               [-h] -t TARGET [TARGET ...] -o OUTDIR [-c CROP] [-w WEIGHTING]
               [-d DENOISE] [-f FIELDCORRECTION] [-m MOSAIC] [-x TESLA]
               [-b BIMODAL] [-n NTHREADS]

Options:
  -h, --help            Show this help message and exit
  -t TARGET [TARGET ...], --target TARGET [TARGET ...]
                        A string or list of strings pointing to the target
                        image(s). Must be a NIfTI file. For a test run,
                        specify /OSHy/sub-test.nii.gz
  -o OUTDIR, --outdir OUTDIR
                        A string pointing to the output directory. Please
                        ensure this is within the mounted volume (Specified
                        with the -v flag for the docker run command.
  -c CROP, --crop CROP  Optional. A boolean indicating if the target image and
                        priors are to be cropped. If False, whole-image priors
                        will be used, which will improve the segmentation but
                        significantly increase the runtime. (default: True)
  -w WEIGHTING, --weighting WEIGHTING
                        A string indicating the weighting of the input
                        image(s). This can be either T1w or T2w. (default: T1w
  -d DENOISE, --denoise DENOISE
                        Optional. A boolean indicating if denoising is to be
                        run on the target image. (default: True)
  -f FIELDCORRECTION, --fieldCorrection FIELDCORRECTION
                        Optional. A boolean indicating if B1 bias field
                        correction is to be run on the target image. (default:
                        True)
  -m MOSAIC, --mosaic MOSAIC
                        Optional. A boolean indicating if a mosaic image is to
                        be plotted after running Joint Label Fusion. (default:
                        True)
  -x TESLA, --tesla TESLA
                        Optional. An integer (either 3 or 7) indicating the
                        field strength. (default: 3)
  -b BIMODAL, --bimodal BIMODAL
                        Optional. A boolean indicating if bimodal priors are
                        to be used. If FALSE, then only unimodal priors
                        (specified in --weighting) will be used.(default:
                        False)
  -n NTHREADS, --nthreads NTHREADS
                        Optional. An integer indicating the number of threads.
                        This is passed to the global variable
                        ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS and the -j flag
                        in Joint Label Fusion. (default: 6)
```


## Output

All output is written to the output directory (specified using the `-o/--outdir` flag.)

Contents of the output include:

* `sub-XX_Labels.nii.gz`: Output from Joint Label Fusion. The label file for the left and right hemispheres of the Hypothalamus and Fornix. If `--crop` is `True` then this label file will also be cropped. The labels are as follows:
    - 1 Left Hypothalamus
    - 2 Right Hypothalamus
    - 3 Right Fornix
    - 4 Left Fornix
* `sub-XX_Intensity.nii.gz`: The input intensity image for Joint Label Fusion segmentation.
* `sub-XX_resampled_Labels.nii.gz`: sub-XX_Labels.nii.gz but resampled to the input target image.
* `sub-XX_hypothalamus.nii.gz`: sub-XX_resampled_Labels.nii.gz but with only hypothalamus labels.
* `sub-XX_fornix.nii.gz`: sub-XX_resampled_Labels.nii.gz but with only fornix labels.
* `sub-XX_mosaic.png`: A 16 slice coronal visualisation of the segmentation.
* `*_log.txt`: The log of the piecewise registration between the atlases and the target image.
* `sub-XX_TargetMaskImageMajorityVoting.nii.gz`: Labelled voxels where Joint Label Fusion was not performed. This is the case when 80% or more of the atlases agree on the same voxel.
* `sub-XX_TargetMaskImageMajorityVoting_Mask`: A mask of voxels where Joint Label Fusion segmentation is performed.
* `sub-XX_volumes.csv`: Volumes of the four labels (as described above). Units for volume are in mm<sup>3</sup>.

## Community

We welcome any contributions to OSHy-X, whether they are reports for bugs, feature enhancements, or pull requests.

To contribute to OSHy-X please visit our [contribute page](https://github.com/Cadaei-Yuvxvs/OSHy-X/contribute) and read our contributing guidelines.
