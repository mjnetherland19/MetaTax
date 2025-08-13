#!/bin/bash

while read line
do
	if [ -f ${line}/${line}_ko_profiles.csv ]
	then
		>tmp.ko

		j=1; while read Line; do name=$(echo $Line | cut -d, -f1); num=$(echo $Line | cut -d, -f2); i=0; while [ $i -lt $num ];do echo "${j},${name}" >> tmp.ko; ((i+=1)); ((j+=1));done;done<${line}/${line}_ko_profiles.csv

		sed 's/,/\t/g' tmp.ko > ${line}/${line}.ko

		python3 ~/opt/MinPath/MinPath.py -ko ${line}/${line}.ko -report ${line}/${line}_minpath.report -details ${line}/${line}_minpath.details
	
	else
		echo "No functional results for $line"

	fi
done<$1
