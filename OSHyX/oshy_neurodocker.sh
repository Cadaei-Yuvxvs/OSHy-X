#!/bin/bash

docker run --rm repronim/neurodocker:0.7.0 generate docker \
--pkg-manager apt -b debian:bullseye-slim \
--ants version=2.3.1 \
--miniconda version=latest use_env=base conda_install="python=3.8 pandas=1.3.5 scikit-learn=1.0.1 julia=1.6.3" pip_install="antspyx psutil pytest==6.2 pytest-mock==3.6.1" \
--env JULIA_DEPOT_PATH=/opt/julia_depot \
--run "julia -e 'using Pkg; Pkg.add(\"MriResearchTools\");'" \
--run "pip install --force-reinstall scipy" \
--run "mkdir -p /OSHy/atlases/3T" \
--run "mkdir /OSHy/atlases/7T" \
--run "mkdir /OSHy/templates" \
--copy OSHy/OSHyX/OSHy.py /OSHy/ \
--copy OSHy/OSHyX/__init__.py /OSHy/ \
--copy $( find ./data/atlases/3T -iname *gz ) /OSHy/atlases/3T/ \
--copy $( find ./data/atlases/7T -iname *gz ) /OSHy/atlases/7T/ \
--copy $( find ./data/templates -iname *gz ) /OSHy/templates/ \
--copy ./data/sub-test.nii.gz /OSHy \
--copy ./data/test_T2w.nii.gz /OSHy \
--entrypoint "python -u /OSHy/OSHy.py" \
> OSHy.Dockerfile

docker build --tag jerync/oshyx_0.4:20220614 --file OSHy.Dockerfile .
