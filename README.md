# MetaTax
Bioinformatics pipeline for short-read metagenomic taxonomic profiling and statistical analysis of cohorts. At the end of the pipeline the results are packaged into an interactive HTML report, for easy viewing and sharing.

This pipeline uses the same set of genomes as my NIID pipeline, which is a recent set of 21,258 genomes published by [NCBI](https://ncbiinsights.ncbi.nlm.nih.gov/2025/01/14/updated-bacterial-and-archaeal-reference-genome-collection-2/). However, much like MetaPhlAn, the database is comprised of marker genes. These loci are those that are described and extracted by the [UBCG2](http://leb.snu.ac.kr/ubcg2) program. These loci are then made into a custom Kraken2 database. While the database is lightweight, you will need to download the UBCG2 profiles for each taxon (18G) as they are used by the script for refining those taxa found by the initial Kraken2 query. I don't have a good way of hosting the database, so post an 'Issue', if you would like to use this pipeline, and I will get it to you. Comparative analysis is available, which includes alpha-diversity rank sum tests, PERMANOVA of Bray-Curtis distance matrix, and differential abundance by ALDEx2 and LinDA. The 'Overview' section below details each part of the pipeline and the functions it performs.

The pipeline can only profile short reads and can handle single-end and paired reads. This pipeline does not perform read trimming or filtering except for host-read removal by Hostile.

At the end of the pipeline, if comparative analysis was performed, the results are packaged into a data.pkl file and are available for easy viewing in a HTML report made using the Python package [Panel](https://panel.holoviz.org/). I will be adding a simpler report if only taxonomic profiling was run.

The 'report' directory in this repo has an example file of profiling and comparative results from 10 samples (5 case, 5 control) of public data from a [Parkinson's study](https://www.ncbi.nlm.nih.gov/bioproject/834801). Just download the directory, double-click the HTML, use it to find the data.pkl file, click Confirm, and you're ready to explore the data.

## Overview

| Component        | Explanation            |
|:-------------:|:-------------------------:|
| **MetaTax.sh**     | Control script           |
| Hostile        | Host-read removal        |
| library(microbiome) | Total Dataset Alpha Diversity |
| library(phyloseq) | Total Dataset Beta Diversity |
| **MetaTaxCG.sh**   | Taxonomic Profiling      |
| Kraken2        | Initial Taxonomic Profiling|
| Bowtie2        | Profiling Refinement |
| SAM/BEDtools   | Output Transformation for filtering scripts |
| **MetaTaxComp.sh** | Comparative Analysis   |
| Rank Sum Test | Diversity Indices Comparison |
| PERMANOVA | Beta-Diversity Comparison | 
| ALDEx2 /LinDA | Differentially Abundant Taxa | 

## Dependencies
- Hostile
- Kraken2
- Bowtie2
- SAMtools
- Bedtools

**R packages:**
- microbiome
- phyloseq
- vegan
- ALDEx2
- LinDA

After installing the dependencies, clone this repo, and download the UBCG2 profiles and place them in the repo directory. This is essential for the pipeline to operate.

## Usage

Each of the scripts can be used independently or the can be used as a set with MetaTax.sh. Check the metadata.csv file in this repo for the proper formatting. It is also required that your file be called `metadta.csv`.

| Component        | Explanation            |
|-------------|:-------------------------:|
| **MetaTax.sh**                                             |            |
| `MetaTax.sh -L <dir list>`                                  | Taxonomic profiling        |
| `MetaTax.sh -L <dir list> -C <dir prefix> -M <metadata.csv>` | Taxonomic profiling and Comparative analysis |
| **MetaTaxCG.sh**                                           |       |
| `MetaTaxCG.sh -1 <forward read> -2 <reverse read> -t <threads> -o <output dir>`        | Taxonomic Profiling (paired-end)|
| `MetaTaxCG.sh -1 <single end> -t <threads> -o <output dir>`                            | Taxonomic Profiling (single-end) |
| **MetaTaxComp.sh**                                                               |   |
| `MetaTaxComp.sh -C <taxa counts CSV> -M <metadata.csv> -O <outpur dir>` | Comparative analysis |
