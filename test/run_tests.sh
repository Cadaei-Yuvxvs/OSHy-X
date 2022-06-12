#!/usr/bin/env bash
set -e 

cp -r . /tmp/OSHy-X

container=$( cat /tmp/OSHy-X/README.md | grep "docker pull" | cut -d " " -f 3 | cut -d "\`" -f 1 )

sudo docker pull $container

out_files=("sub-test_Intensity.nii.gz" "sub-test_denoised_bias-corrected_cropped_T1w.nii.gz" \
"sub-test_resampled_Labels.nii.gz" "sub-test_sub-21_cropped_T1w_3_log.txt"  \
"sub-test_sub-35_cropped_T1w_7_log.txt" "sub-test_Labels.nii.gz" "sub-test_fornix.nii.gz" \
"sub-test_sub-04_cropped_T1w_0_log.txt"  "sub-test_sub-22_cropped_T1w_4_log.txt"  \
"sub-test_sub-40_cropped_T1w_8_log.txt" "sub-test_TargetMaskImageMajorityVoting.nii.gz" \
"sub-test_hypothalamus.nii.gz" "sub-test_sub-05_cropped_T1w_1_log.txt" \
"sub-test_sub-25_cropped_T1w_5_log.txt"  "sub-test_sub-48_cropped_T1w_9_log.txt" \
"sub-test_TargetMaskImageMajorityVoting_Mask.nii.gz" "sub-test_mosaic.png" \
"sub-test_sub-06_cropped_T1w_2_log.txt" "sub-test_sub-26_cropped_T1w_6_log.txt" \
"sub-test_volumes.csv")

echo "[DEBUG] Running Pytest"

sudo docker run -v /tmp/OSHy-X/test:/tmp --entrypoint "python" $container -m pytest /tmp/OSHy-X_test.py

echo "[DEBUG] Running default pipeline"

sudo docker run -v /tmp:/tmp $container -t /OSHy/sub-test.nii.gz -o /tmp

for out_file in ${out_files[@]}; do [ -f /tmp/sub-test/${out_file} ] && echo "[DEBUG] Test OK: Regular output file $outfile exists." || echo "[DEBUG] Test FAILED: Regular output file $outfile does not exist."; done

seg_vols=$( cat /tmp/sub-test/sub-test_volumes.csv | cut -d "," -f 7 | tail -n 4 )
for seg_vol in ${seg_vols[@]}; do [ $seg_vol -ge 350 ] && [ $seg_vol -le 500 ] && echo "[DEBUG] Test OK: Segmented volume is within normal parameters." || echo "[DEBUG] Test FAILED: Segmented volume is not within normal parameters."; done

sudo rm -r /tmp/sub-test
