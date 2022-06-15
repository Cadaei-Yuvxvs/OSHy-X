#!/usr/bin/env bash
set -e 

cp -r . /tmp/OSHy-X

container=$( cat /tmp/OSHy-X/README.md | grep "docker pull" | cut -d " " -f 3 | cut -d "\`" -f 1 )

sudo docker pull $container

out_files_suffix=("_Intensity.nii.gz" "_denoised_bias-corrected_cropped_T1w.nii.gz" \
"_resampled_Labels.nii.gz" "_sub-21_cropped_T1w_3_log.txt"  \
"_sub-35_cropped_T1w_7_log.txt" "_Labels.nii.gz" "_fornix.nii.gz" \
"_sub-04_cropped_T1w_0_log.txt"  "_sub-22_cropped_T1w_4_log.txt"  \
"_sub-40_cropped_T1w_8_log.txt" "_TargetMaskImageMajorityVoting.nii.gz" \
"_hypothalamus.nii.gz" "_sub-05_cropped_T1w_1_log.txt" \
"_sub-25_cropped_T1w_5_log.txt"  "_sub-48_cropped_T1w_9_log.txt" \
"_TargetMaskImageMajorityVoting_Mask.nii.gz" "_mosaic.png" \
"_sub-06_cropped_T1w_2_log.txt" "_sub-26_cropped_T1w_6_log.txt" \
"_volumes.csv")

echo "[DEBUG] Running Pytest"

sudo docker run -v /tmp/OSHy-X/test:/tmp --entrypoint "python" $container -m pytest /tmp/OSHy-X_test.py

echo "[DEBUG] Running default pipeline"

sudo docker run --memory-swap -1 -v /tmp:/tmp $container -t /OSHy/sub-test.nii.gz -o /tmp

for out_file in ${out_files_suffix[@]}
do
    sub_out_file=sub-test${out_file}
    if [ -f /tmp/sub-test/${sub_out_file} ] 
    then
        echo "[DEBUG] Test OK: Regular output file ($sub_out_file) exists."
    else
        echo "[DEBUG] Test FAILED: Regular output file ($sub_out_file) does not exist."
        exit 1
    fi
done

seg_vols=$( cat /tmp/sub-test/sub-test_volumes.csv | cut -d "," -f 7 | tail -n 4 )

for seg_vol in ${seg_vols[@]}
do 
    if [ $(echo "($seg_vol > 100) && ($seg_vol < 700)" | bc -l) -eq 1 ]
    then 
        echo "[DEBUG] Test OK: Segmented volume ($seg_vol) is within normal parameters."
    else 
        echo "[DEBUG] Test FAILED: Segmented volume ($seg_vol) is not within normal parameters."
        exit 1
    fi
done

sudo rm -r /tmp/sub-test

docker system prune --force

echo "[DEBUG] Running bimodal pipeline"

out_bimodal_files_suffix=("_Intensity.nii.gz" "_Labels.nii.gz" \
"_TargetMaskImageMajorityVoting.nii.gz" "_TargetMaskImageMajorityVoting_Mask.nii.gz" \
"_denoised_bias-corrected_cropped_T1w.nii.gz" "_fornix.nii.gz" \
"_hypothalamus.nii.gz" "_mosaic.png" "_resampled_Labels.nii.gz" \
"_sub-04_N4Bias_Denoised_cropped_registered_T2w_0_log.txt" \
"_sub-04_cropped_T1w_1_log.txt" \
"_sub-05_N4Bias_Denoised_cropped_registered_T2w_2_log.txt" \
"_sub-05_cropped_T1w_3_log.txt" \
"_sub-06_N4Bias_Denoised_cropped_registered_T2w_4_log.txt" \
"_sub-06_cropped_T1w_5_log.txt" \
"_sub-21_N4Bias_Denoised_cropped_registered_T2w_6_log.txt" \
"_sub-21_cropped_T1w_7_log.txt" \
"_sub-22_N4Bias_Denoised_cropped_registered_T2w_8_log.txt" \
"_sub-22_cropped_T1w_9_log.txt" \
"_sub-25_N4Bias_Denoised_cropped_registered_T2w_10_log.txt" \
"_sub-25_cropped_T1w_11_log.txt" \
"_sub-26_N4Bias_Denoised_cropped_registered_T2w_12_log.txt" \
"_sub-26_cropped_T1w_13_log.txt" \
"_sub-35_N4Bias_Denoised_cropped_registered_T2w_14_log.txt" \
"_sub-35_cropped_T1w_15_log.txt" \
"_sub-40_N4Bias_Denoised_cropped_registered_T2w_16_log.txt" \
"_sub-40_cropped_T1w_17_log.txt" \
"_sub-48_N4Bias_Denoised_cropped_registered_T2w_18_log.txt" \
"_sub-48_cropped_T1w_19_log.txt" \
"_volumes.csv")

sudo docker run --memory-swap -1 -v /tmp:/tmp $container -t /OSHy/sub-test.nii.gz -o /tmp -b True

for out_file in ${out_bimodal_files_suffix[@]}
do
    sub_out_file=sub-test${out_file}
    if [ -f /tmp/sub-test/${sub_out_file} ] 
    then
        echo "[DEBUG] Test OK: Regular output file ($sub_out_file) exists."
    else
        echo "[DEBUG] Test FAILED: Regular output file ($sub_out_file) does not exist."
        exit 1
    fi
done

seg_vols=$( cat /tmp/sub-test/sub-test_volumes.csv | cut -d "," -f 7 | tail -n 4 )

for seg_vol in ${seg_vols[@]}
do 
    if [ $(echo "($seg_vol > 100) && ($seg_vol < 700)" | bc -l) -eq 1 ]
    then 
        echo "[DEBUG] Test OK: Segmented volume ($seg_vol) is within normal parameters."
    else 
        echo "[DEBUG] Test FAILED: Segmented volume ($seg_vol) is not within normal parameters."
        exit 1
    fi
done

sudo rm -r /tmp/sub-test

docker system prune --force

echo "[DEBUG] Running pipeline with 7T input"

out_7T_files_suffix=("_Intensity.nii.gz" "_denoised_bias-corrected_cropped_T1w.nii.gz" \
"_resampled_Labels.nii.gz" "_sub-H0112_cropped_T1w_3_log.txt"  \
"_sub-P0008_cropped_T1w_7_log.txt" "_Labels.nii.gz" "_fornix.nii.gz" \
"_sub-H0101_cropped_T1w_0_log.txt"  "_sub-H0115_cropped_T1w_4_log.txt"  \
"_sub-P0011_cropped_T1w_8_log.txt" "_TargetMaskImageMajorityVoting.nii.gz" \
"_hypothalamus.nii.gz" "_sub-H0108_cropped_T1w_1_log.txt" \
"_sub-P0003_cropped_T1w_5_log.txt" "_TargetMaskImageMajorityVoting_Mask.nii.gz" \
"_mosaic.png" "_sub-H0111_cropped_T1w_2_log.txt" "_sub-P0016_cropped_T1w_9_log.txt" \
"_sub-P0004_cropped_T1w_6_log.txt" "_volumes.csv")

sudo docker run --memory-swap -1 -v /tmp:/tmp $container -t /OSHy/atlases/7T/sub-P0004_whole_ses-01_T1w_defaced.nii.gz -o /tmp -x 7

for out_file in ${out_7T_files_suffix[@]}
do
    sub_out_file=sub-P0004${out_file}
    if [ -f /tmp/sub-P0004/${sub_out_file} ] 
    then
        echo "[DEBUG] Test OK: Regular output file ($sub_out_file) exists."
    else
        echo "[DEBUG] Test FAILED: Regular output file ($sub_out_file) does not exist."
        exit 1
    fi
done

seg_vols=$( cat /tmp/sub-P0004/sub-P0004_volumes.csv | cut -d "," -f 7 | tail -n 4 )

for seg_vol in ${seg_vols[@]}
do 
    if [ $(echo "($seg_vol > 100) && ($seg_vol < 700)" | bc -l) -eq 1 ]
    then 
        echo "[DEBUG] Test OK: Segmented volume ($seg_vol) is within normal parameters."
    else 
        echo "[DEBUG] Test FAILED: Segmented volume ($seg_vol) is not within normal parameters."
        exit 1
    fi
done

sudo rm -r /tmp/sub-P0004

docker system prune --force

echo "[DEBUG] Running pipeline with T2w input"

out_T2w_files_suffix=("_Intensity.nii.gz" "_fornix.nii.gz" \
"_sub-05_N4Bias_Denoised_cropped_registered_T2w_1_log.txt" \
"_sub-26_N4Bias_Denoised_cropped_registered_T2w_6_log.txt" "_Labels.nii.gz" \
"_hypothalamus.nii.gz" "_sub-06_N4Bias_Denoised_cropped_registered_T2w_2_log.txt" \
"_sub-35_N4Bias_Denoised_cropped_registered_T2w_7_log.txt" \
"_TargetMaskImageMajorityVoting.nii.gz" "_mosaic.png" \
"_sub-21_N4Bias_Denoised_cropped_registered_T2w_3_log.txt" \
"_sub-40_N4Bias_Denoised_cropped_registered_T2w_8_log.txt" \
"_TargetMaskImageMajorityVoting_Mask.nii.gz" "_resampled_Labels.nii.gz" \
"_sub-22_N4Bias_Denoised_cropped_registered_T2w_4_log.txt" \
"_sub-48_N4Bias_Denoised_cropped_registered_T2w_9_log.txt" \
"_denoised_bias-corrected_cropped_T2w.nii.gz" \
"_sub-04_N4Bias_Denoised_cropped_registered_T2w_0_log.txt" \
"_sub-25_N4Bias_Denoised_cropped_registered_T2w_5_log.txt" "_volumes.csv")

sudo docker run --memory-swap -1 -v /tmp:/tmp $container -t /OSHy/test_T2w.nii.gz -o /tmp -w T2w

for out_file in ${out_T2w_files_suffix[@]}
do
    sub_out_file=test${out_file}
    if [ -f /tmp/test/${sub_out_file} ] 
    then
        echo "[DEBUG] Test OK: Regular output file ($sub_out_file) exists."
    else
        echo "[DEBUG] Test FAILED: Regular output file ($sub_out_file) does not exist."
        exit 1
    fi
done

seg_vols=$( cat /tmp/test/test_volumes.csv | cut -d "," -f 7 | tail -n 4 )

for seg_vol in ${seg_vols[@]}
do 
    if [ $(echo "($seg_vol > 50) && ($seg_vol < 700)" | bc -l) -eq 1 ]
    then 
        echo "[DEBUG] Test OK: Segmented volume ($seg_vol) is within normal parameters."
    else 
        echo "[DEBUG] Test FAILED: Segmented volume ($seg_vol) is not within normal parameters."
        exit 1
    fi
done
