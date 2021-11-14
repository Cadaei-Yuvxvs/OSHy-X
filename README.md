# Open Source Hypothalamic-ForniX (OSHy-X) Atlases and Segmentation Tool for 3T and 7T

*Version 0.1*

OSHy-X is an atlas repository (https://osf.io/zge9t) and containerised Python script that automatically segments the hypothalamus and fornix at 3T and 7T in both T1w and T2w scans. 

If you intend to use OSHy-X, please cite this abstract: TBA

![The user inputs a T1w or T2w image. They are given the options for denoising, B1 bias field correction and image cropping. After Joint Label Fusion, the given output are the label, volume and mosaic files.](Media/OSHy_figure_1.GIF "OSHy pipeline")

***

## Installation

You have the option of running OSHy-X via NeuroDesk, a Docker container by itself, or a Singularity container.

### Neurodesk

Follow instructions [here](https://neurodesk.github.io/docs/neurodesktop/getting-started/) to install Neurodesk.

### Docker

1. Install Docker [here](https://docs.docker.com/get-docker/).
2. Open a terminal and run `docker pull jerync/oshyx_0.1:20211114`

### Singularity

***

## Usage

### Neurodesk

### Docker

```
Usage: docker run --rm -v /path/to/data:/data jerync/oshyx_0.1:20211114 
               [-h] -t TARGET [TARGET ...] -o OUTDIR [-c CROP] [-w WEIGHTING]
               [-d DENOISE] [-f FIELDCORRECTION] [-m MOSAIC] [-x TESLA]
               [-b BIMODAL] [-n NTHREADS]

Options:
  -h, --help            Show this help message and exit
  -t TARGET [TARGET ...], --target TARGET [TARGET ...]
                        A string or list of strings pointing to the target
                        image(s). Must be a NIfTI file.
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

### Singularity

***

## Output

All output is written to the output directory (specified using the `-o/--outdir` flag.)

Contents of the output include:

* `sub-XX_Labels.nii.gz`: Output from Joint Label Fusion. The label file for the left and right hemispheres of the Hypothalamus and Fornix. If `--crop` is `True` then this label file will also be cropped. The labels are as follows:
    1. Left Hypothalamus
    2. Right Hypothalamus
    3. Right Fornix
    4. Left Fornix
* `sub-XX_ressampled_Labels.nii.gz`: sub-XX_Labels.nii.gz but resampled to the input target image.
* `sub-XX_hypothalamus.nii.gz`: sub-XX_resampled_Labels.nii.gz but with only hypothalamus labels.
* `sub-XX_fornix.nii.gz`: sub-XX_resampled_Labels.nii.gz but with only fornix labels.
* `sub-XX_mosaic.png`: A 16 slice coronal visualisation of the segmentation.
* `sub-XX_volumes.csv`: Volumes of the four labels (as described above). Units for volume are in mm<sup>3</sup>.
