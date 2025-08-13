#!/bin/R
#Needs taxa as rows

library(LinDA)

args = commandArgs(trailingOnly=TRUE)

taxa.df=read.csv(args[1],row.names=1, check.names=F)
meta.df=read.csv(args[2],row.names=1)

linda.obj <- linda(taxa.df, meta.df, formula = paste0("~",args[3]), alpha = 0.05,prev.cut = 0.1, lib.cut = 1000, winsor.quan = 0.97)

write.csv(linda.obj$output,paste0(args[4],"/linda.out"))
