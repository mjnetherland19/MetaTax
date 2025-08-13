#!/bin/bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

db_dir="/mnt/e/NCBI_Best_Prokaryote_Genomes/Arius_Shotgun_DB"
contents="${db_dir}/taxonomy.csv"

do_comp() {
	mkdir comparative full_dataset_diversities taxonomic_dataframes report
	
	python3 ${SCRIPT_DIR}/scripts/make_count_matrix.py $dir_prefix
	python3 ${SCRIPT_DIR}/scripts/pandas_merge.py $contents species_RA.csv taxonomic_dataframes/species_taxonomy.csv
	Rscript ${SCRIPT_DIR}/scripts/all_diversity.R species_counts.csv $metadata full_dataset_diversities/total
	MetaTaxComp.sh species_counts.csv $metadata comparative
	mv species* taxonomic_dataframes
	cp ${SCRIPT_DIR}/shotgun_comparative_blank.py .
	python3 scripts/make_pickle.py comparative report
	bash ${SCRIPT_DIR}/scripts/change_code.sh $metadata
	panel convert shotgun_comparative_report.py --to pyodide --out report
}

print_usage() {
  echo "Mandatory args: [-L Text file with list of DIR names]" 
}

while getopts ':L:C:M:h' flag; do
  case "${flag}" in
    L) lizt="${OPTARG}" ;;
    C) dir_prefix="${OPTARG}" ;;
    M) metadata="${OPTARG}" ;;
    h) print_usage
       exit 1 ;;
    *|\?) print_usage
       exit 1 ;;
  esac
done

while read line
do
	R1=${line}/${line}_R1.fast*
	R2=${line}/${line}_R2.fast*
	o=$line

	if [ ! -f $R1 ]
	then
		R1=${line}/${line}_1.fast*
		R2=${line}/${line}_2.fast*
	fi

	if [ ! -f $R2 ]
	then
		eval "$(conda shell.bash hook)"
		conda activate hostile

		hostile clean --aligner bowtie2 --fastq1 ${R1} -o ${o} -t 4

		conda deactivate
		
		R1=${line}/*1.clean*fast*
		
		MetaTaxCG.sh -1 ${R1} -o ${o}
	else
		R1=${line}/*1.clean*fast*
		R2=${line}/*2.clean*fast*

		if [ ! -f $R1 ]
		then
			eval "$(conda shell.bash hook)"
			conda activate hostile

			hostile clean --aligner bowtie2 --fastq1 ${R1} --fastq2 ${R2} -o ${o} -t 4

			conda deactivate
		fi

		
		bash MetaTaxCG.sh -1 ${R1} -2 ${R2} -o ${o}
	fi

done<$lizt

if [[ ! -z ${dir_prefix} ]]
then
	if [[ -z ${metadata} ]]
	then
		echo "Missing metadata"
		exit
	else
		do_comp
	fi
fi
