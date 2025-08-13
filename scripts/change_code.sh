#!/bin/bash

metadata=$1
header=$(head -n1 $metadata | cut -d, -f2-)
echo $header > tmp
sed -i 's/^/"/' tmp

flag=$(grep "," tmp)

if [[ ! -z $flag ]]
then 
	sed -i 's/,/","/g' tmp
fi

sed -i 's/$/"/' tmp

while read line;do change="[${line}]"; done<tmp

sed "s/meta_cols=/meta_cols=${change}/" shotgun_comparative_blank.py > shotgun_comparative_report.py 
