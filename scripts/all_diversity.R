#!/bin/R

suppressPackageStartupMessages(library(microbiome))
suppressPackageStartupMessages(library(vegan))
suppressPackageStartupMessages(library(phyloseq))

args = commandArgs(trailingOnly=TRUE)

norm.genus = read.csv(args[1],row.names=1,check.names=F)

#Metadata should have two columns: Samples,Health
meta = read.csv(args[2],row.names=1,check.names=F)

samples = sample_data(meta)


gen.matrix = as.matrix(norm.genus)
gen.otu = otu_table(gen.matrix, taxa_are_rows = T)
genus.phylo = phyloseq(gen.otu,samples)

diversity <- microbiome::alpha(genus.phylo, index="all")

print("Start Beta")
ord.bray=ordinate(genus.phylo,"PCoA","bray")
dist.bray=distance(genus.phylo,method="bray")
write.csv(as.matrix(dist.bray),paste0(args[3],"_dist_matrix.csv"))
#Get coordinates for RF feature table
#bray.pcoa.coords.df = ord.bray$points
print("Add Bray to table")
meta$bray1 = ord.bray$vectors[,1]
meta$bray2 = ord.bray$vectors[,2]
meta$bray3 = ord.bray$vectors[,3]
write.csv(ord.bray$values$Relative_eig,paste0(args[3],"_bray_variance_explained.csv"))

clr.trans<-microbiome::transform(genus.phylo,"clr")
#Do Euclidean if clr transformed. It equals aitchison
print("Start Ordination")
ord.ait=ordinate(clr.trans,"PCoA","euclidean")
ait.pcoa.coords.df = ord.ait$points
meta$ait1 = ord.ait$vectors[,1]
meta$ait2 = ord.ait$vectors[,2]
meta$ait3 = ord.ait$vectors[,3]
#Meta=cbind(meta,diversity)
write.csv(ord.ait$values$Relative_eig,paste0(args[3],"_ait_variance_explained.csv"))
write.csv(diversity,paste0(args[3],"_alpha_diversity.csv"))
write.csv(meta,paste0(args[3],"_beta_diversity.csv"))
