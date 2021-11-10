#!/bin/bash

docker run --rm repronim/neurodocker:0.7.0 generate docker \
--pkg-manager apt -b debian:bullseye-slim \
--ants version=2.3.1 \
--miniconda version=latest use_env=base conda_install="python=3.8 pandas scikit-learn" pip_install=antspyx \
--run "mkdir -p /OSHy/atlases/3T" \
--run "mkdir /OSHy/atlases/7T" \
--run "mkdir /OSHy/templates" \
--copy OSHy/code/OSHy.py /OSHy/ \
--copy $( find ./data/atlases/3T -iname *gz ) /OSHy/atlases/3T/ \
--copy $( find ./data/atlases/7T -iname *gz ) /OSHy/atlases/7T/ \
--copy $( find ./data/templates -iname *gz ) /OSHy/templates/ \
--entrypoint "python /OSHy/OSHy.py" \
> OSHy.Dockerfile

docker build --tag oshyx:0.1 --file OSHy.Dockerfile .

# Example of running OSHy in "one line of code".
# docker run --rm \
# -v /path/to/data:/data oshyx:0.1 \
# -t /test/sub-H0101_ses-01_T1w.nii.gz /test/sub-H0112_ses-01_T1w.nii.gz /test/sub-P0004_ses-01_T1w.nii.gz /test/sub-P0016_ses-01_T1w.nii.gz /test/sub-H0108_ses-01_T1w.nii.gz /test/sub-H0115_ses-01_T1w.nii.gz /test/sub-P0008_ses-01_T1w.nii.gz /test/sub-H0111_ses-01_T1w.nii.gz /test/sub-P0003_ses-01_T1w.nii.gz /test/sub-P0011_ses-01_T1w.nii.gz \
# -o /data/out -d True -n True -m True -x 7 -b False
