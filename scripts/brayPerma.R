#!/bin/R

#arg1 = samples as rows and taxa as columns
#arg2 = metadata for permanova
#arg3 = column to use for adonis2

suppressPackageStartupMessages(library(vegan))

args = commandArgs(trailingOnly=TRUE)
len=length(args)

if (len == 4){
	data=read.csv(args[1],row.names=1,check.names=F)
	meta=read.csv(args[2],row.names=1,check.names=F)
	g=args[3]
	#Transpose if data is taxa as rows
	data.dist=as.matrix(vegdist(t(data),method="bray"))
	sub=meta[[g]]
	form=formula(paste("data.dist ~",g))	
	data.perm=adonis2(form, data=meta, permutations=999, na.action=na.omit)
	
	write.csv(data.perm,paste0(args[4],"/permanova.csv"))
}else if (len == 2) {
	data=read.csv(args[1],row.names=1,check.names=F)
	out=args[2]
	
	data.dist=as.matrix(vegdist(data,method="bray"))
	pcoa=cmdscale(data.dist)
	write.csv(pcoa,out)


} else {
	exit	
}
