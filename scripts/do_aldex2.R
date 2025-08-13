#!/bin/R
#Needs taxa as rows
#Positive effect size means greater abundance in the second group and negative in the first one.
#Check 'denom' parameter

library(ALDEx2)

args = commandArgs(trailingOnly=TRUE)

conds <- scan(args[1], what = "character") 
taxa.df=read.csv(args[2],row.names=1,check.names=F)

x.aldex <- aldex(taxa.df, conds, mc.samples=128, test="t", effect=TRUE, include.sample.summary=FALSE, denom="all", verbose=FALSE, paired.test=FALSE, gamma=NULL)

write.csv(x.aldex,paste0(args[3],"/aldex2.out"))
