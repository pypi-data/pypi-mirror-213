import pandas as pd
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scanpy as sc
import scanpy.external as sce
import matplotlib 
from matplotlib import rcParams
import matplotlib.font_manager
import matplotlib.font_manager as fm
import anndata
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import math
from scipy import ndimage
from scipy.spatial import distance_matrix
import requests
import matplotlib.colors as mcolors

def plot1feature(tissue_obj, mz_use, title='',cmap = "magma_r", 
                              max_num=50000, min_num=0, figsize = (6,5)):
    #print('Feature mz:',mz_use)
    tissue_mz = tissue_obj.to_img_mtx(mz=mz_use,smooth=False)
    df1=tissue_mz
    fig, ((ax1,axcb1)) = plt.subplots(1, 2, figsize = figsize,dpi = 300,gridspec_kw={'width_ratios':[1,0.05]})
    

    g1 = sns.heatmap(df1,vmax=max_num,vmin=min_num,
                    mask=(df1==0),cmap=cmap,
                    ax=ax1,cbar_ax=axcb1)
    g1.set_ylabel('');g1.set_xlabel('');g1.set_xticks([]);g1.set_yticks([])
    

    scalebar1 = AnchoredSizeBar(ax1.transData,30, '', 'lower right',frameon=False,size_vertical=2,sep=1,
                               fontproperties=fm.FontProperties(size=10))

##300um
    ax1.add_artist(scalebar1)
    plt.tight_layout()
    return fig

def plot1feature_subset(tissue_obj,  mz_use, title='',cmap = "magma_r",
                              max_num=50000, min_num=0, figsize = (6,5), subset=[95,185,35,175]):
    #print('Feature mz:',mz_use)
    tissue_mz = tissue_obj.to_img_mtx(mz=mz_use,smooth=False)
    df1=tissue_mz.iloc[subset[0]:subset[1], subset[2]:subset[3]]

    fig, ((ax1)) = plt.subplots(1, 1, figsize = figsize,dpi = 300,gridspec_kw={'width_ratios':[1]})
    
    #max_num= max(df1.max().max(),df2.max().max(),df3.max().max())

    g1 = sns.heatmap(df1,vmax=max_num,vmin=min_num,
                    mask=(df1==0),cmap=cmap,
                    ax=ax1, cbar=False)
    g1.set_ylabel('');g1.set_xlabel('');g1.set_xticks([]);g1.set_yticks([])
    plt.tight_layout()
    return fig

def twofeatureplot(
    tissue_obj, mz_use,  
    title='',
    cmap = ["Reds", "Greens"], 
                   
    max_num_1=50000, min_num_1=0, 
    max_num_2=50000, min_num_2=0,
    alpha = [0.5, 0.5],
    figsize = (6,5)
):
    #print('Feature mz:',mz_use)
    df1 = tissue_obj.to_img_mtx(mz=mz_use[0],smooth=False)
    df2 = tissue_obj.to_img_mtx(mz=mz_use[1],smooth=False)

    fig, ax1  = plt.subplots(1, 1, figsize = figsize,dpi = 300)
    g1 = sns.heatmap(df1,
                     vmax=max_num_1,vmin=min_num_1,
                     mask=(df1==0),cmap=cmap[0],
#                      ax=ax1,cbar_ax=axcb1)
                     ax=ax1, alpha=alpha[0],
                    cbar_kws={"shrink": 0.5})
    # use matplotlib.colorbar.Colorbar object
    cbar = g1.collections[0].colorbar
    # here set the labelsize by 20
    cbar.ax.tick_params(labelsize=6)
    g2 = sns.heatmap(df2,
                     vmax=max_num_2,vmin=min_num_2,
                     mask=(df2==0),cmap=cmap[1],
#                      ax=ax1,cbar_ax=axcb1)
                     ax=ax1, alpha=alpha[1],
                    cbar_kws={"shrink": 0.5})
    # use matplotlib.colorbar.Colorbar object
    cbar2 = g2.collections[1].colorbar
    # here set the labelsize by 20
    cbar2.ax.tick_params(labelsize=6) 
    #g1.set_title('Donor#1 Cortex\n',fontsize=16)
    g1.set_ylabel('');g1.set_xlabel('');g1.set_xticks([]);g1.set_yticks([])
    g2.set_ylabel('');g2.set_xlabel('');g2.set_xticks([]);g2.set_yticks([])

    scalebar1 = AnchoredSizeBar(ax1.transData,30, '', 'lower right',frameon=False,size_vertical=2,sep=1,
                               fontproperties=fm.FontProperties(size=10))

    ax1.add_artist(scalebar1)
    plt.show()
    
    return fig


def twofeatureplot_subset(
    tissue_obj, mz_use,    
    title='',
    cmap = ["Reds", "Greens"], 
                 
    max_num_1=50000, min_num_1=0, 
    max_num_2=50000, min_num_2=0,
    alpha = [0.5, 0.5],
    figsize = (6,5),subset=[95,185,35,175]
    
):
    #print('Feature mz:',mz_use)
    df1 = tissue_obj.to_img_mtx(mz=mz_use[0],smooth=False).iloc[subset[0]:subset[1], subset[2]:subset[3]]
    df2 = tissue_obj.to_img_mtx(mz=mz_use[1],smooth=False).iloc[subset[0]:subset[1], subset[2]:subset[3]]

    fig, ax1  = plt.subplots(1, 1, figsize = figsize,dpi = 300)
    g1 = sns.heatmap(df1,
                     vmax=max_num_1,vmin=min_num_1,
                     mask=(df1==0),cmap=cmap[0],
                     ax=ax1, alpha=alpha[0],
                    cbar=False)

    g2 = sns.heatmap(df2,
                     vmax=max_num_2,vmin=min_num_2,
                     mask=(df2==0),cmap=cmap[1],
                     ax=ax1, alpha=alpha[1],
                    cbar=False)

    g1.set_ylabel('');g1.set_xlabel('');g1.set_xticks([]);g1.set_yticks([])
    g2.set_ylabel('');g2.set_xlabel('');g2.set_xticks([]);g2.set_yticks([])

    plt.show()
    
    return fig