#!/bin/bash

eval "$(conda shell.bash hook)"
conda activate hostile

hostile clean --fastq1 $1 --fastq2 $2 -t 2 -o ${3} -t 4

conda deactivate
