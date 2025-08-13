#!/bin/bash

threads=4

R1=$1
R2=$2

final=$3
python3 scripts/parse_bedfile.py Test/kraken.bed DB_dictionary.dict taxonomy.csv 0.1 | sort > test_set

if [ ! -d full_genome ]
then
	mkdir -p full_genome/bow_index
fi

if [ ! -f full_genome/multi.fasta ]
then

	while read line
	do
		name=$(echo $line | cut -d, -f2)
		cat genomes/${name}.fasta >> full_genome/multi.fasta

	done<test_set
fi

eval "$(/home/mjnetherland19/miniconda3/bin/conda shell.bash hook)"
conda activate bowtie2

echo Building Bowtie2 Index `date`
bowtie2-build --threads $threads full_genome/multi.fasta full_genome/bow_index/multi > /dev/null 2>&1

echo Aligning with Bowtie2 `date`
bowtie2 --no-unal --very-sensitive --threads $threads -x full_genome/bow_index/multi -1 $R1 -2 $R2 -S full_genome/temp.sam > /dev/null 2>&1

conda deactivate

echo transformSam `date`
scripts/transformSam full_genome/temp.sam

#echo Removing seconday alignments `date`
#samtools view -@ 4 -h -F 0x904 full_genome/temp_sorted.bam > full_genome/temp_filtered.bam

echo bamtobed `date`
bedtools bamtobed -i full_genome/temp_sorted.bam > full_genome/full_genome.bed

grep ">" full_genome/multi.fasta | cut -d" " -f 1-3 > full_genome/contig_key

sed -i 's/>//g' full_genome/contig_key

#Remove any results less than 13?
python3 bed_quality_distr_full_genome.py full_genome/full_genome.bed full_genome/contig_key | sort -k3 -n -t,

echo Finished `date`
