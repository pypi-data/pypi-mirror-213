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
from PIL import Image

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

def plot2features(msi_obj, feats , cmap, scale_auto=False,
                max_num_1=41000, min_num_1=21000, 
                max_num_2=50000, min_num_2=25000):
    
    df1 = msi_obj.to_img_mtx(mz=feats[0],smooth=False)
    df2 = msi_obj.to_img_mtx(mz=feats[1],smooth=False)

    if scale_auto == True:
        min_num_1 = np.quantile(df1, 0.01)
        max_num_1 = np.quantile(df1, 0.99)
        min_num_2 = np.quantile(df2, 0.01)
        max_num_2 = np.quantile(df2, 0.99)
    df1_new = df1.clip(min_num_1,max_num_1, axis=1)
    df2_new = df2.clip(min_num_2,max_num_2, axis=1)
    
    df1_norm = (df1_new - df1_new.min().min()) / (df1_new.max().max() - df1_new.min().min())
    df2_norm = (df2_new - df2_new.min().min()) / (df2_new.max().max() - df2_new.min().min())

    # Convert to RGB colors
    img1 = cmap[0](df1_norm.to_numpy())
    img2 = cmap[1](df2_norm.to_numpy())
    img_combined = np.clip(img1 + img2, 0, 1)

    # Convert to 8-bit RGB for visualization
    img_combined_uint8 = (img_combined * 255).astype(np.uint8)
    img_pil = Image.fromarray(img_combined_uint8)

    fig, ax  = plt.subplots(1, 1, dpi = 400)
    plt.imshow(img_pil)
    plt.axis('off')
    plt.tight_layout()
    return fig

def plot2features_subset(msi_obj, feats, cmap, scale_auto=False,
                max_num_1=41000, min_num_1=21000, 
                max_num_2=50000, min_num_2=25000,
                         subset=[95,185,35,175]):
    
    df1 = msi_obj.to_img_mtx(mz=feats[0],smooth=False).iloc[subset[0]:subset[1], subset[2]:subset[3]]
    df2 = msi_obj.to_img_mtx(mz=feats[1],smooth=False).iloc[subset[0]:subset[1], subset[2]:subset[3]]

    if scale_auto == True:
        min_num_1 = np.quantile(df1, 0.01)
        max_num_1 = np.quantile(df1, 0.99)
        min_num_2 = np.quantile(df2, 0.01)
        max_num_2 = np.quantile(df2, 0.99)
    df1_new = df1.clip(min_num_1,max_num_1, axis=1)
    df2_new = df2.clip(min_num_2,max_num_2, axis=1)
    
    df1_norm = (df1_new - df1_new.min().min()) / (df1_new.max().max() - df1_new.min().min())
    df2_norm = (df2_new - df2_new.min().min()) / (df2_new.max().max() - df2_new.min().min())

    # Convert to RGB colors
    img1 = cmap[0](df1_norm.to_numpy())
    img2 = cmap[1](df2_norm.to_numpy())
    img_combined = np.clip(img1 + img2, 0, 1)

    # Convert to 8-bit RGB for visualization
    img_combined_uint8 = (img_combined * 255).astype(np.uint8)
    img_pil = Image.fromarray(img_combined_uint8)

    fig, ax  = plt.subplots(1, 1, dpi = 400)
    plt.imshow(img_pil)
    plt.axis('off')
    plt.tight_layout()
    return fig