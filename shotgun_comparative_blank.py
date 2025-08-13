import matplotlib.pyplot as plt
import hvplot.pandas
import numpy as np
import pandas as pd
import panel as pn
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")
pn.extension('plotly')
import pickle
import io
import seaborn as sns
from scipy.stats import ranksums

descr=pn.pane.Markdown("""

## Analysis Workflow

1. Host reads removed using Hostile, which aligns to the human T2T-CHM13v2.0 and IPD-IMGT/HLA v3.51 genomic data.
2. Taxonomic profiling conducted using a Kraken2 database of core genes derived from a curated list of genomes. All metrics and analyses were performed using the raw count data matrix.
3. Alpha-diversity indices were calculated using the *microbiome* R package, using species count data.
4. Beta-diversity analyses were performed using the *vegan* and *phyloseq* R packages, using species count data.
5. PERMANOVA calculations were found using *adonis2* from *vegan* with 999 permutations.
6. P-value calculations for alpha-diversity distributions was performed with *ranksums* from Python's *scipy.stats* 

### Differential Abundance

- ALDEx2 transforms count data using the centered log-ratio method and performs Monte-Carlo sampling from the Dirichlet distribution to estimate the effect size of taxonomic differential abundance.

- LinDA implements a simple, robust and highly scalable approach to tackle the compositional effects in differential abundance analysis. It fits linear regression models on the centered log2-ratio transformed data, identifies a bias term due to the transformation and compositional effect, and corrects the bias using the mode of the regression coefficients. It could fit mixed-effect models.

""", width=600)

global comp
global no_tax

taxonomic_rank=["Phylum","Class","Order","Family","Genus","Species"]
measures=["observed","diversity_inverse_simpson","diversity_shannon"]
ETC=[0.01,0.05,0.1,0.5,1,2]
stats=["Total Seqs","% Duplicate","%GC","Mean Seq Length"]
meta_cols=


################################# CREATE CHARTS ############################

##Full Dataset Taxonomic Profile##
def create_stacked_bar(choice,etc):
    df2=pd.DataFrame()

    ranks=["Phylum","Class","Order","Family","Genus","Species"]

    cols=list(df.columns)
    ranks.remove(choice)

    set1=set(cols)
    set2=set(ranks)
    diff=set1.difference(set2)

    temp=df.drop(columns=ranks)

    df2=temp.groupby(choice,dropna=False).sum()

    df2.reset_index(inplace=True)

    melt=pd.melt(df2,id_vars=choice,value_vars=list(diff))
    melt[choice].loc[melt['value'] < etc] = "Other"

    fig = px.histogram(melt, x="variable", y="value",color=choice,title=f"{choice} Abundance (<{etc}% as \'Other\')",barmode="stack",color_discrete_map=colors)
    fig.update_layout(yaxis_title="Relative Abundance")
    fig.update_layout(xaxis_title="")
    fig.update_traces(textfont_color='black')
    fig.update_layout(legend=dict(font=dict(size=12)))
    #fig.update_layout(dict(font=dict(size=14),title_x=0.2,legend=dict(orientation="h",font=dict(size=14),y=-0.30)))
    
    return pn.pane.Plotly(fig,width=1200,height=800)

##Full Dataset Alpha Diversity##
def create_bar_chart(measure):
    return al.hvplot.bar(x="index", y=measure, bar_width=0.8, rot=90,width=1200, height=600,fontsize={'ylabel': '3px', 'ticks': 11}).opts(active_tools=[])

##Full Dataset Beta Diversity##
def create_scatter_chart(switch):
    #Add PC variance explained
    
    cols=list(bd.columns)

    B=[cols[0],"bray1","bray2","bray3"]
    A=[cols[0],"ait1","ait2","ait3"]

    bray=bd[B]
    aitc=bd[A]
    
    B_d={"bray1":"1st PC","bray2":"2nd PC","bray3":"3rd PC"}
    A_d={"ait1":"1st PC","ait2":"2nd PC","ait3":"3rd PC"}

    Bray=bray.rename(columns=B_d)
    Aitc=aitc.rename(columns=A_d)
    
    if switch:
        fig = px.scatter_3d(Bray, x="1st PC", y="2nd PC", z="3rd PC",text=Bray.index, color=cols[0])
    else:
        fig = px.scatter_3d(Bray, x="1st PC", y="2nd PC", z="3rd PC", color=cols[0])
        
    fig.update_traces(marker=dict(size=4,line=dict(width=1,color='DarkSlateGrey')))
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=30))
    fig.update_layout(legend=dict(font=dict(size=18),itemsizing="constant"))

    if switch:
        fig2 = px.scatter_3d(Aitc, x="1st PC", y="2nd PC", z="3rd PC",text=Aitc.index, color=cols[0])
    else:
        fig2 = px.scatter_3d(Aitc, x="1st PC", y="2nd PC", z="3rd PC", color=cols[0])
        
    fig2.update_traces(marker=dict(size=4,line=dict(width=1,color='DarkSlateGrey')))
    fig2.update_layout(margin=dict(l=0, r=0, b=0, t=30))
    fig2.update_layout(legend=dict(font=dict(size=18),itemsizing="constant"))
    
    Fig=pn.pane.Plotly(fig,width=900,height=600,name="Bray-Curtis")
    Fig2=pn.pane.Plotly(fig2,width=900,height=600,name="Aitchison")

    tabs = pn.Tabs(Fig, Fig2, dynamic=True)

    return tabs

##Comp Profile##
def make_average(temp_tax,etc,choice):
    comp_group=pd.merge(taxonomy,temp_tax,left_index=True,right_index=True)
    comp_group.index.name="Species"
    comp_group.reset_index(inplace=True)

    df=comp_group

    df2=pd.DataFrame()

    ranks=["Phylum","Class","Order","Family","Genus","Species"]

    cols=list(df.columns)
    for r in ranks:
        cols.remove(r)
    ranks.remove(choice)

    temp=df.drop(columns=ranks)

    df2=temp.groupby(choice,dropna=False).sum()

    df2.reset_index(inplace=True)

    melt=pd.melt(df2,id_vars=choice,value_vars=cols)

    melt[choice].loc[melt['value'] < etc] = "Other"

    fig = px.histogram(melt, x="value", y="variable",color=choice,title=f"Average Abundance",barmode="stack",color_discrete_map=colors)
    fig.update_layout(yaxis_title="Relative Abundance")
    fig.update_layout(xaxis_title="")
    fig.update_traces(textfont_color='black')
    fig.update_layout(title=dict(font=dict(size=16)))
    fig.update_layout(legend=dict(font=dict(size=12)))
    
    return fig

def create_stacked_bar_column(choice,etc,group):
    
    average=pd.DataFrame()
    Avg=[]
    figures=[]
    m=group
    temp=meta[m]
    merged=pd.merge(no_tax.T,temp,left_index=True,right_index=True)
    merged=merged.loc[~merged[m].isna()]
    
    for u in merged[m].unique():
        temp_merged=merged.loc[merged[m]==u]
        temp_tax=temp_merged.T
        temp_tax.drop(index=m,inplace=True)
        length=len(list(temp_tax.columns))

        average[u] = temp_tax.apply(lambda row: row.sum()/length, axis=1)
        comp_group=pd.merge(taxonomy,temp_tax,left_index=True,right_index=True)
        comp_group.index.name="Species"
        comp_group.reset_index(inplace=True)
        
        df=comp_group
    
        df2=pd.DataFrame()

        ranks=["Phylum","Class","Order","Family","Genus","Species"]
        cols=list(df.columns)
        for r in ranks:
            cols.remove(r)
        ranks.remove(choice)

        temp=df.drop(columns=ranks)

        df2=temp.groupby(choice,dropna=False).sum()

        df2.reset_index(inplace=True)

        melt=pd.melt(df2,id_vars=choice,value_vars=cols)

        melt[choice].loc[melt['value'] < etc] = "Other"


        fig = px.histogram(melt, x="variable", y="value",color=choice,title=f"{u}",barmode="stack",color_discrete_map=colors)
        
        fig.update_layout(yaxis_title="Relative Abundance")
        fig.update_layout(xaxis_title="")
        fig.update_traces(textfont_color='black')
        fig.update_layout(title=dict(font=dict(size=16)))
        fig.update_yaxes(title_font = {"size": 14})
        fig.update_layout(legend=dict(font=dict(size=12)))
        
        figures.append(fig)
        
    Avg.append(make_average(average,etc,choice))
    
    Full=Avg+figures
    
    return pn.Column(*[pn.pane.Plotly(fig,width=1200,height=600) for fig in Full])

#Comp Stats##
def create_full_comp(switch,group):
    mark=pn.pane.Markdown(f"## {Comps[group][0]} vs. {Comps[group][1]}")
    
    alf=comp[group][0]
    beta=comp[group][1]
    perm=comp[group][2]
    aldex=comp[group][3]
    linda=comp[group][4]

    ### Alpha Diversity ###

    merge=pd.merge(alf,meta,left_index=True,right_index=True)

    feats=["observed","diversity_inverse_simpson","diversity_shannon"]

    fig,ax = plt.subplots(1, 3, dpi=200,figsize=(10, 5))
    col=group
    for c,feat in enumerate(feats):
        title=""
        temp=feat.split("_")
        for t in temp:
            title+=t[0].upper()
            title+=t[1:]
            if len(temp) > 1:
                title+=" "

        ymax=round(merge[feat].max())

        melt=pd.melt(merge,id_vars=[col],value_vars=[feat])

        diff=[]
        for u in list(merge[col].unique()):
            diff.append(merge.loc[merge[col]==u])

        d1=list(diff[0][feat])
        d84=list(diff[1][feat])

        pval=round(ranksums(d1, d84)[1], 4)

        sns.boxplot(data=melt, x=col, y="value",palette="Greys",ax=ax[c],hue=col,legend=False)

        inc=(ymax*0.02)

        idx1=0
        idx2=1

        ymax+=inc
        ymin=melt["value"].min() - (ymax*0.1)

        pltx=[idx1,idx1,idx2,idx2]
        plty=[ymax, ymax+inc, ymax+inc, ymax]

        text=f"p-value={pval}"
        summ=idx1+idx2

        ax[c].text(summ*.5, ymax+inc*2, text, ha='center', va='bottom', color="black")
        ax[c].plot(pltx, plty, lw=1.5, c="black")

        ax[c].set_title(title, fontsize=12)
        ax[c].set_ylabel("")
        ax[c].set_xlabel("")
        ax[c].set_ylim(ymin,ymax+(ymax*0.1))
    
    alpha_fig=pn.pane.Matplotlib(fig,width=900,height=600,name="Alpha Diversity")
    
    ### BETA-DIVERSITY ###

    #Need to add PC variance explained
    B=[group,"bray1","bray2","bray3"]
    A=[group,"ait1","ait2","ait3"]

    bray=beta[B]
    aitc=beta[A]
    
    B_d={"bray1":"1st PC","bray2":"2nd PC","bray3":"3rd PC"}
    A_d={"ait1":"1st PC","ait2":"2nd PC","ait3":"3rd PC"}

    Bray=bray.rename(columns=B_d)
    Aitc=aitc.rename(columns=A_d)
    
    if switch:
        fig = px.scatter_3d(Bray, x="1st PC", y="2nd PC", z="3rd PC",text=Bray.index, color=group)
    else:
        fig = px.scatter_3d(Bray, x="1st PC", y="2nd PC", z="3rd PC", color=group)
        
    fig.update_traces(marker=dict(size=4,line=dict(width=1,color='DarkSlateGrey')))
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=30))
    fig.update_layout(legend=dict(font=dict(size=18),itemsizing="constant"))

    if switch:
        fig2 = px.scatter_3d(Aitc, x="1st PC", y="2nd PC", z="3rd PC",text=Aitc.index, color=group)
    else:
        fig2 = px.scatter_3d(Aitc, x="1st PC", y="2nd PC", z="3rd PC", color=group)
        
    fig2.update_traces(marker=dict(size=4,line=dict(width=1,color='DarkSlateGrey')))
    fig2.update_layout(margin=dict(l=0, r=0, b=0, t=30))
    fig2.update_layout(legend=dict(font=dict(size=18),itemsizing="constant"))
    
    Fig=pn.pane.Plotly(fig,width=900,height=600,name="Bray-Curtis")
    Fig2=pn.pane.Plotly(fig2,width=900,height=600,name="Aitchison")

    ##PERMANOVA DF###

    permanova = pn.pane.DataFrame(perm, width=400, name="PERMANOVA")

    ##ALDEx2 DF###
    
    Aldex = pn.pane.DataFrame(aldex, width=400, name="ALDEx2 DA")
    
    ##ALDEx2 Bar Chart###
    
    adding=[]

    comp_lab=Comps[group]
    lizt=list(aldex.index)
    for i in range(0,len(lizt)):
        ef=aldex.iloc[i,0].item()
        if ef < 0:
            adding.append(comp_lab[0])
        elif ef > 0:
            adding.append(comp_lab[1])

    aldex['c']=adding
    fig=px.bar(aldex, x="Effect Size", y=aldex.index, color=aldex.index)
    fig.update_layout(showlegend=False)
    fig.update_layout(yaxis_title="")
    Fig4=pn.Column(pn.pane.Markdown(f'## Negative values enriched in {Comps[group][0]} | Positive values enriched in {Comps[group][1]}'),pn.pane.Plotly(fig),name="ALDEx2 Chart")

    ##LinDA DF###
    Linda = pn.Column(pn.pane.Markdown(f"## Fold change relative to {Comps[group][1]}"),pn.pane.DataFrame(linda, width=400), name="LinDA DA")

    ##LinDA Bar Chart###

    sc = px.scatter(linda, x="log2FoldChange", y="P-value",text=linda.index)
    Fig3=pn.Column(pn.pane.Markdown(f"## Fold change relative to {Comps[group][1]}"),pn.pane.Plotly(sc,width=900,height=600),name="LinDA Chart")
    
    tabs = pn.Tabs(alpha_fig,Fig, Fig2, permanova, Aldex, Fig4, Linda, Fig3, dynamic=True)

    return pn.Column(mark,tabs)

############################# WIDGETS & CALLBACK ###########################
# https://tabler-icons.io/
button1 = pn.widgets.Button(name="Introduction and Methods", button_type="warning", styles={"height": "50px","width": "100%"})
button3 = pn.widgets.Button(name="Composition", button_type="warning", styles={"height":"50px","width": "100%"})
button4 = pn.widgets.Button(name="Full Dataset Alpha", button_type="warning", styles={"height":"50px","width": "100%"})
button5 = pn.widgets.Button(name="Full Dataset Beta", button_type="warning", styles={"height":"50px","width": "100%"})
button6 = pn.widgets.Button(name="Comparative Tax Profile", button_type="warning", styles={"height":"50px","width": "100%"})
button7 = pn.widgets.Button(name="Comparative Statistics", button_type="warning", styles={"height":"50px","width": "100%"})

seq = pn.widgets.Select(name="Statistic", options=stats)
rank = pn.widgets.Select(name="Taxonomic Rank", options=taxonomic_rank)
alpha = pn.widgets.Select(name="Measure", options=measures)
etc = pn.widgets.Select(name="Group Rare Taxa as 'Other' (%)", options=ETC)
switch = pn.widgets.Switch(name='Something else')
groups=pn.widgets.Select(name="Comparative Group", options=meta_cols)

def show_page(page_key):
    mapping = {
        "Page1": CreatePage1(),
        "Page3": CreatePage3(),
        "Page4": CreatePage4(),
        "Page5": CreatePage5(),
        "Page6": CreatePage6(),
        "Page7": CreatePage7(),
    }
    
    main_area.clear()
    main_area.append(mapping[page_key])

############################ CREATE PAGE LAYOUT ##############################
def CreatePage1():
    return pn.Column(descr,align=("start","end"))

def CreatePage3():
    #Taxonomic
    return pn.Column(pn.pane.Markdown("## Composition"),pn.Row(rank,etc),pn.bind(create_stacked_bar,choice=rank,etc=etc),align="center")

def CreatePage4():
    #Alpha
    return pn.Column(pn.pane.Markdown("## Alpha-diversity"),alpha,pn.bind(create_bar_chart,measure=alpha),align="center")

def CreatePage5():
    #Beta
    return pn.Column(pn.pane.Markdown("## Full Dataset Beta-diversity"),pn.Row(switch,"Toggle sample labeling in plot"),pn.bind(create_scatter_chart,switch=switch),align="center")

def CreatePage6():
    #Comparative taxonomic
    return pn.Column(pn.pane.Markdown("## Comparative Analysis - Taxonomic Composition"),pn.Row(rank,etc,groups),pn.bind(create_stacked_bar_column,choice=rank,etc=etc,group=groups),align="center")

def CreatePage7():
    #Comparative module
    return pn.Column(pn.pane.Markdown("## Comparative Analysis Statitics"),pn.Row(groups,switch,"Toggle sample labeling in beta-diversiy plot"),pn.bind(create_full_comp,switch=switch,group=groups),align="center")

########Initialization#########


def main():


    button1.on_click(lambda event: show_page("Page1"))
    button3.on_click(lambda event: show_page("Page3"))
    button4.on_click(lambda event: show_page("Page4"))
    button5.on_click(lambda event: show_page("Page5"))
    button6.on_click(lambda event: show_page("Page6"))
    button7.on_click(lambda event: show_page("Page7"))


    sidebar2 = pn.Column(pn.pane.Markdown("## Pages"), button1, button3, button4, button5, button6, button7, styles={"width": "100%", "padding": "15px"})
    sidebar.clear()
    sidebar.append(sidebar2)


#################### FILE INPUT ##########################

DF = pn.widgets.FileInput(accept=".pkl")

confirmButton1 = pn.widgets.Button(name="Confirm")

def get_data(file):
    if file is not None:
        d = pickle.load(io.BytesIO(file))
        return d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8]

data1 = pn.bind(get_data, DF)

df = pd.DataFrame()
taxonomy = pd.DataFrame()
no_tax = pd.DataFrame()
al = pd.DataFrame()
rd = pd.DataFrame()
meta = pd.DataFrame()
colors={}
Comps={}
comp={}

def confirmselection1(file):
    global df
    global taxonomy
    global no_tax
    global meta
    global al
    global bd
    global comp
    global colors
    global Comps

    df,taxonomy,no_tax,meta,al,bd,comp,colors,Comps = data1()
    main()
   
confirmButton1.on_click(confirmselection1)

sidebar = pn.Column(pn.pane.Markdown("## Pages"), styles={"width": "100%", "padding": "15px"})

#################### MAIN AREA LAYOUT ##########################
main_area = pn.Column(pn.Row(DF, confirmButton1, pn.pane.Markdown("## Upload data.pkl file and click Confirm")),styles={"width":"100%"})


###################### APP LAYOUT ##############################
template = pn.template.BootstrapTemplate(
    title="Shotgun Comparative Analysis HTML Report",
    sidebar=[sidebar],
    main=[main_area],
    header_background="#61cfde", 
    sidebar_width=250, ## Default is 330
    busy_indicator=None,
)

# Serve the Panel app
template.servable()
