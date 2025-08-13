# MetaTax
Bioinformatics pipeline for short-read taxonomic profiling and statistical analysis of cohorts. At the end of the pipeline the results are packaged into an interactive HTML report, for easy viewing and sharing.

This pipeline uses the same set of genomes as my NIID pipeline, which is a recent set of 21,258 genomes published by [NCBI](https://ncbiinsights.ncbi.nlm.nih.gov/2025/01/14/updated-bacterial-and-archaeal-reference-genome-collection-2/). However, much like MetaPhlAn, the database is comprised of marker genes. These loci are those that are described and extracted by the [UBCG2](http://leb.snu.ac.kr/ubcg2) program. These loci are then made into a custom Kraken2 database. While the database is lightweight, you will need to download the UBCG2 profiles for each taxon as they are used by the script for refining those taxa found by the initial Kraken2 query. This pipeline also incorporates comparative analysis, which includes alpha-diversity rank sum tests, PERMANOVA of Bray-Curtis distance matrix, and differential abundance by ALDEx2 and LinDA. The 'Overview' section below details each part of the pipeline and the functions it performs.

The pipeline can only profile short reads and can handle single-end and paired reads. This pipeline does not perform read trimming or filtering except for host-read removal by Hostile.

## Overview

| Component        | Explanation            |
|:-------------:|:-------------------------:|
**| MetaTax.sh     | Control script           |**
| Hostile        | Host-read removal        |
| library(microbiome) | Total Dataset Alpha Diversity |
| library(phyloseq) | Total Dataset Beta Diversity |
**| MetaTaxCG.sh   | Taxonomic Profiling      |**
| Kraken2        | Initial Taxonomic Profiling|
| Bowtie2        | Profiling Refinement |
| SAM/BEDtools   | Output Transformation for filtering scripts |
**| MetaTaxComp.sh | Comparative Analysis   |**
| Rank Sum Test | Diversity Indices Comparison |
| PERMANOVA | Beta-Diversity Comparison | 
| ALDEx2 /LinDA | Differentially Abundant Taxa | 
