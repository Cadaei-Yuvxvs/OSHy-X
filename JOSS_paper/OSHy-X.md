---
title: 'Open-Source Hypothalamic-ForniX (OSHy-X) Atlases and Segmentation Tool for 3T and 7T'
tags:
  - Python
  - Docker
  - Singularity
  - ANTs
  - MRI
  - Segmentation
  - Multi-atlas label fusion
authors:
  - name: Jeryn Chang
    orcid: 0000-0002-6659-365X
    affiliation: 1
  - name: Frederik Steyn
    orcid: 0000-0002-4782-3608
    affiliation: "1,2,3,4"
  - name: Shyuan Ngo
    orcid: 0000-0002-1388-2108
    affiliation: "2,3,4,5"
  - name: Robert Henderson
    orcid: 0000-0002-2820-8183
    affiliation: "2,3,4"
  - name: Christine Guo
    affiliation: 6
  - name: Steffen Bollmann
    orcid: 0000-0002-2909-0906
    affiliation: "7,8"
  - name: Jurgen Fripp
    orcid: 0000-0001-9705-0079
    affiliation: 9
  - name: Markus Barth
    orcid: 0000-0002-0520-1843
    affiliation: "7,8"
  - name: Thomas Shaw
    orcid: 0000-0003-2490-0532
    affiliation: "2,7,8"

affiliations:
 - name: School of Biomedical Sciences, The University of Queensland 
   index: 1
 - name: Department of Neurology, Royal Brisbane and Women's Hospital, Australia
   index: 2
 - name: Wesley Medical Research, The Wesley Hospital
   index: 3
 - name: UQ Centre for Clinical Research, The University of Queensland
   index: 4
 - name: Australian Institute of Bioengineering and Nanotechnology, The University of Queensland
   index: 5
 - name: QIMR Berghofer Medical Research Institute, Brisbane, Australia
   index: 6
 - name: Centre for Advanced Imaging, The University of Queensland
   index: 7
 - name: School of Information Technology and Electrical Engineering, The University of Queensland 
   index: 8
 - name: CSIRO Health and Biosecurity, Brisbane, Australia
   index: 9
date: 16 December 2021
bibliography: OSHy-X.bib
---

# Summary

Segmentation and volumetric analysis of the hypothalamus and fornix plays a 
critical role in improving the understanding of degenerative processes that 
might impact the function of these structures. We present Open-Source 
Hypothalamic-ForniX (`OSHy-X`) atlases and tool for multi-atlas fusion 
segmentation for 3T and 7T. The atlases are based on 20 manual segmentations, 
which we demonstrate have high interrater agreement. The versatility of the 
`OSHy-X` tool allows segmentation and volumetric analysis for different field 
strengths and contrasts. We also demonstrate that `OSHy-X` segmentation has 
higher Dice overlaps (3T and 7T inputs: p<0005, p<0.005) than a deep-learning 
segmentation method for the hypothalamus [@Billot:2020]. We have previously 
demonstrated the use of `OSHy-X` on a cohort of 329 non-neurodegenerative 
control participants and 42 patients with ALS to investigate reduced 
hypothalamic volume and its association with appetite, hypermetabolism and 
weight loss [@Chang:2021].

# Statement of need

Segmentation of small structures of the brain including the hypothalamus and fornix is important for primary research of health and disease. Amyotrophic Lateral Sclerosis (ALS) is a fatal neurodegenerative disease that involves the degeneration and death of motor neurons in the brain and spinal cord. Neuronal death and gross volume loss has also been reported in the hypothalamus in ALS [@Gorges:2017] [@Gabery:2021] [@Christidi:2019]. To measure such changes, methods for *in vivo* MRI segmentation of the hypothalamus and fornix include deep learning [@Billot:2020], seed growing techniques [@Wolff:2018], and manual segmentation [@Gorges:2017]. There is a need to develop and distribute open-source atlases of these structures for more accurate and standardised segmentation. Here, we present the Open-Source Hypothalamic-ForniX (`OSHy-X`) atlases and tool for multi-atlas fusion segmentation for 3T and 7T. `OSHy-X` is an atlas repository and containerised `Python` script that automatically segments the hypothalamus and fornix at 3T and 7T in both T1w and T2w scans.

<br>

# Methodology

## Atlas

Twenty atlases were derived from manual segmentation of the hypothalamus-fornix, conducted by two tracers familiar with the hypothalamus and fornix [@Chang:OSF]. Ten non-neurodegenerative disease participants and ten patients with ALS were selected at random from within the larger datasets of the EATT4MND and 7TEA studies for the tracing. Details of the acquisition parameters have been outlined previously [@Chang:2021].

## Tool

A summary of the pipeline is illustrated in \autoref{fig:1}. The user can specify the contrast (T1w/T2w) of the atlases used, the field strength (3T/7T) and any pre-processing steps. `OSHy-X` utilises Joint Label Fusion (`JLF`) [@Wang:2013] from Advanced Normalization Tools (`ANTs`; v2.3.1) for the registration [@Avants:2008] of atlases and segmentation of the target image. B1+ bias field inhomogeneity correction is performed using `MriResearchTools` (v0.5.2). Denoising and cropping are performed using ANTs in Python (`ANTsPy`; v0.2.0).

![Pipeline overview of the OSHy-X segmentation tool. Users input a target image via an one-line command, and the pipeline produces hypothalamus and fornix labels, their volumes, and a mosaic visualisation of the segmentations. The pipeline and data are encapsulated within a Docker or Singularity container.\label{fig:1}](../Media/OSHy-X_figure_1.png)

# Performance

\autoref{fig:2} visually compares the differences in the segmentation of a representative non-neurodegenerative disease participant using manual segmentation and `JLF` using leave-one out cross validation. Overall, `JLF` tends to under-segment throughout the hypothalamus and fornix. To a lesser extent, `JLF` tends to over-segment the anterior and lateral hypothalamus and the body of the fornix. 

![Visualisation of segmentation performance between manual segmentation and `JLF`. The hypothalamus is shown in red and the fornix in blue. The first three rows show segmentation in coronal, sagittal and axial planes; a 3D rendering of the structures is illustrated in the fourth row. The difference between `JLF` and manual segmentation illustrates over-segmented (red) and under-segmented (green) areas.\label{fig:2}](../Media/OSHy-X_figure_2.png){ width=60% }

Dice overlaps (\autoref{fig:3}) and (ICC; 2-way fixed-rater mixed effects model with single measurement) between the two raters indicate excellent segmentation accuracy. The left and right hypothalamus received scores of 0.90 (0.66-0.98 CI) and 0.91 (0.68-0.98 CI). The left and right fornix received scores of 0.97 (0.87-0.99 CI) and 0.68 (0.13-0.91 CI).

![Dice overlaps between two raters for the left and right lobes of the hypothalamus and fornix. The median Dice’s coefficient for the left and right hypothalamus is 0.94 (0.01 IQR) and 0.96 (0.03 IQR). The median Dice’s coefficient for the left and right fornix are 0.91 (0.06 IQR) and 0.91 (0.03 IQR).\label{fig:3}](../Media/OSHy-X_figure_3.png){ width=70% }

In comparison to a deep learning method for segmentation [@Billot:2020]  (available in `FreeSurfer` v7.2), we found that `JLF` has higher Dice overlaps with the manual segmentations for both 3T and 7T (\autoref{fig:4}). Additionally, we found that compared to cropped priors, whole-brain priors for `JLF` offers modest benefits to segmentation accuracy at 3T, but significant performance benefits at 7T compared to the deep learning method. While whole brain instead of cropped priors for `JLF` improves segmentation performance, computational time increases prohibitively.

![Dice overlaps of `JLF` with whole-brain priors and deep learning hypothalamic segmentation methods with manual segmentations. The median Dice’s coefficient for `JLF` with 3T and 7T inputs are 0.82 (0.04 IQR) and 0.83 (0.06 IQR). The median Dice’s coefficient for the deep learning method with 3T and 7T inputs are 0.72 (0.03 IQR) and 0.72 (0.05 IQR). In both 3T and 7T field strengths, `JLF` outperforms the deep learning method (Wilcoxon rank sum test; p<0005 and p<0.005).\label{fig:4}](../Media/OSHy-X_figure_4.png){ width=70% }

# Availability

The `OSHy-X` atlas is freely available at (https://osf.io/zge9t) and the tool is available via the `Neurodesk` data analysis environment (https://neurodesk.github.io) or as a `Docker`/`Singularity` container (https://github.com/Cadaei-Yuvxvs/OSHy-X ).

# Acknowledgements

We thank all individuals who took part in the studies. 

Funding for EATT4MND was provided by Wesley Medical Research (The Wesley Hospital, Brisbane) and The Faculty of Medicine, The University of Queensland.

The authors acknowledge the facilities and scientific and technical assistance of the National Imaging Facility, a National Collaborative Research Infrastructure Strategy (NCRIS) capability, at the Centre for Advanced Imaging, The University of Queensland. This research was undertaken with the assistance of resources and services from the Queensland Cyber Infrastructure Foundation (QCIF). The authors gratefully acknowledge Aiman Al Najjer, Nicole Atcheson, Anita Burns, Saskia Bollmann, and Amelia Ceslis for acquiring data.

JC is supported by the UQ Graduate School Scholarship (RTP). STN is supported by a FightMND Mid-Career Fellowship. MB acknowledges funding from Australian Research Council Future Fellowship grant FT140100865. MB and SB acknowledge the ARC Training Centre for Innovation in Biomedical Imaging Technology (CIBIT). TS is supported by a Motor Neurone Disease Research Australia (MNDRA) Postdoctoral Research Fellowship (PDF2112). 

# References