#!/bin/bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

database="${SCRIPT_DIR}/MetaTax_DB"
dictionary="${SCRIPT_DIR}/DB_dictionary.dict"
contents="${SCRIPT_DIR}/taxonomy.csv"

prefix="kraken"
threads=4
coverage=0.04
outdir="meta_tax_out"
keep=0
echo $outdir

print_usage() {
  echo "Mandatory args: [-1 forward read file]
Optional args :[-2 reverse read file] [-p prefix for result files] [-t threads for Kraken2] [-c core gene coverage threshold] [-o output directory]"
}

while getopts ':1:2:o:p:t:c:k:h' flag; do
	echo $flag
	case "${flag}" in
		1) R1="${OPTARG}" ;;
		2) R2="${OPTARG}" ;;
		o) outdir="${OPTARG}" ;;
		p) prefix="${OPTARG}" ;;
		t) threads="${OPTARG}" ;;
		c) coverage="${OPTARG}" ;;
		k) keep="${OPTARG}" ;;
		h) print_usage
		exit 1 ;;
		*) print_usage
		exit 1 ;;
	esac
done


present=$(pwd)

if [ ! -d $outdir ]
then
	mkdir $outdir
fi

if [ -d temp ] || [ -f temp ]
then
	echo "Please move to a directory that has no existing directory called \'temp\' and run again"
	exit
else

	mkdir temp
fi

echo Running Kraken `date` > ${outdir}/${prefix}.log

if [ -z $R2 ]
then

	kraken2 --db ${database} --confidence 0.3 --threads $threads --report ${outdir}/${prefix}.tsv $R1 > /dev/null
else
	kraken2 --db ${database} --confidence 0.3 --threads $threads --report ${outdir}/${prefix}.tsv --paired $R1 $R2 > /dev/null
fi


echo Parsing Kraken Output `date` >> ${outdir}/${prefix}.log
${SCRIPT_DIR}/scripts/parse_kraken_report.py ${outdir}/${prefix}.tsv ${outdir}/${prefix}_parsed.csv

echo Getting Taxa Names `date` >> ${outdir}/${prefix}.log
cat ${outdir}/${prefix}_parsed.csv | cut -d, -f1 > ${present}/temp/taxa_names

sed -i '1d' ${present}/temp/taxa_names

echo Getting Core Genes `date` >> ${outdir}/${prefix}.log
${SCRIPT_DIR}/scripts/get_core_genes.py ${present}/temp/taxa_names $database ${present}/temp

#make sure 'bow_index' is a directory in the pwd
mkdir ${present}/temp/bow_index

echo Building Bowtie2 Index `date` >> ${outdir}/${prefix}.log
bowtie2-build --threads $threads ${present}/temp/temp_multifasta ${present}/temp/bow_index/multi > /dev/null 2>&1

echo Aligning with Bowtie2 `date` >> ${outdir}/${prefix}.log
bowtie2 --no-unal --very-sensitive --threads $threads -x ${present}/temp/bow_index/multi -1 $R1 -2 $R2 -S ${present}/temp/temp.sam > /dev/null 2>&1

echo Filter and Transform SAM output `date` >> ${outdir}/${prefix}.log
${SCRIPT_DIR}/scripts/transformSam ${present}/temp/temp.sam

echo bamtobed `date` >> ${outdir}/${prefix}.log
bedtools bamtobed -i ${present}/temp/temp_sorted.bam > ${outdir}/${prefix}.bed

echo Filter bedfile `date` >> ${outdir}/${prefix}.log
${SCRIPT_DIR}/scripts/filter_bed.py ${outdir}/${prefix}.bed 31 ${outdir}

echo Pare bedfile `date` >> ${outdir}/${prefix}.log
${SCRIPT_DIR}/scripts/parse_bedfile.py ${outdir}/filtered_31.bed $dictionary $contents $coverage > ${outdir}/${prefix}_final_taxa.csv

while read line; do name=$(echo $line | cut -d, -f1); grep "$name" ${outdir}/${prefix}_parsed.csv >> ${present}/temp/to_change ; done<${outdir}/${prefix}_final_taxa.csv

echo Rescale `date` >> ${outdir}/${prefix}.log
${SCRIPT_DIR}/scripts/rescale_RA.py ${present}/temp/to_change ${outdir}/${prefix}

echo Finished `date` >> ${outdir}/${prefix}.log

if [ $keep -eq 0 ]
then
	rm -r temp
fi

