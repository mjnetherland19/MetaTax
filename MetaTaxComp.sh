#!/bin/bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

print_usage() {
  echo "Mandatory args: [-C taxa counts] [-M metadata.csv file] [-O output dir]" 
}

while getopts ':C:M:O:' flag; do
  case "${flag}" in
    C) counts="${OPTARG}" ;;
    M) meta="${OPTARG}";;
    O) comp_out="${OPTARG}";;
    h) print_usage
       exit 1 ;;
    *) print_usage
       exit 1 ;;
  esac
done

if [ ! -d $comp_out ]
then
	mkdir $comp_out
fi

python3 ${SCRIPT_DIR}/scripts/sub_meta_for_comparative_analysis.py $counts $meta $comp_out

for comp in ${comp_out}/*
do
	base=$(basename $comp)
	echo $base
	
	Rscript ${SCRIPT_DIR}/scripts/brayPerma.R ${comp}/${base}_taxa.csv ${comp}/${base}_meta.csv ${base} ${comp}/${base}
	Rscript ${SCRIPT_DIR}/scripts/all_diversity.R ${comp}/${base}_taxa.csv ${comp}/${base}_meta.csv ${comp}/${base}
	Rscript ${SCRIPT_DIR}/scripts/do_aldex2.R ${comp}/${base}_scan.txt ${comp}/${base}_taxa.csv $comp
	python3 ${SCRIPT_DIR}/scripts/get_aldex2_DA.py ${comp}/aldex2.out ${comp}/${base}
	Rscript ${SCRIPT_DIR}/scripts/do_linda.R ${comp}/${base}_taxa.csv ${comp}/${base}_meta.csv $base $comp
	python3 ${SCRIPT_DIR}/scripts/get_linda_DA.py ${comp}/linda.out ${comp}/${base}
	sed -i '1,5d' ${comp}/permanova.out
	sed -i '5,6d' ${comp}/permanova.out
done
