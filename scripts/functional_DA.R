suppressPackageStartupMessages(library(DESeq2))

args = commandArgs(trailingOnly=TRUE)

kegg=read.csv(args[1],row.names=1,check.names=F)
meta=read.csv(args[2],row.names=1,check.names=F)
form=formula(paste("~ Subject +",args[3]))
meta$Subject=as.factor(meta$Subject)
meta[[args[3]]]=as.factor(meta[[args[3]]])
dds <- DESeqDataSetFromMatrix(countData = kegg, colData = meta,design=form)
ds <- DESeq(dds)
res <- results(ds)
write.csv(res,paste0(args[3],"_deseq_res.csv"))
