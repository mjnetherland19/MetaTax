#!/bin/bash

prefix="kraken"

while read outdir
do

	while read line; do name=$(echo $line | cut -d, -f1); grep "$name" ${outdir}/${prefix}_parsed.csv >> ${outdir}/to_change ; done<${outdir}/${prefix}_final_taxa.csv

	rescale_RA.py ${outdir}/to_change ${outdir}/${prefix}
done<$1
