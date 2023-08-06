import scanpy as sc
import pandas as pd
import numpy as np
import os
import anndata as ad
from adjustText import adjust_text
from pathlib import Path
import glob
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style='white')



def gen_mpl_labels(adata, groupby, exclude=(), ax=None, adjust_kwargs=None, text_kwargs=None):
    if adjust_kwargs is None:
        adjust_kwargs = {"text_from_points": False}
    if text_kwargs is None:
        text_kwargs = {}

    medians = {}

    for g, g_idx in adata.obs.groupby(groupby).groups.items():
        if g in exclude:
            continue
        medians[g] = np.median(adata[g_idx].obsm["X_umap"], axis=0)

    if ax is None:
        texts = [
            plt.text(x=x, y=y, s=k, **text_kwargs) for k, (x, y) in medians.items()
        ]
    else:
        texts = [ax.text(x=x, y=y, s=k, **text_kwargs) for k, (x, y) in medians.items()]
    
    adjust_text(texts, **adjust_kwargs)

def gen_mpl_labels_df(df, groupby, x_coord = "UMAP_1", y_coord = "UMAP_2",exclude=(), ax=None, adjust_kwargs=None, text_kwargs=None):
    if adjust_kwargs is None:
        adjust_kwargs = {"text_from_points": False}
    if text_kwargs is None:
        text_kwargs = {}

    medians = {}

    for g, g_idx in df.groupby(groupby).groups.items():
        if g in exclude:
            continue
        medians[g] = np.median(df.loc[g_idx, [x_coord, y_coord]], axis=0)

    if ax is None:
        texts = [
            plt.text(x=x, y=y, s=k, **text_kwargs) for k, (x, y) in medians.items()
        ]
    else:
        texts = [ax.text(x=x, y=y, s=k, **text_kwargs) for k, (x, y) in medians.items()]

    adjust_text(texts, **adjust_kwargs)

def scATAnno_plotting_umap_df(df, hue, out_dir, filename, figsize = (6,6), dtype = "categorical",  show = True, palette = "tab20"):
    """
    Return umap plot.

    Parameters
    ----------
    df: panda dataframe that has umap coordinates UMAP_1 and UMAP_2
    hue: anndata variable 
    out_dir: output directory
    filename: output filename
    dtype: datatype of hue parameter: None, categorical or numerical 
    """
    
    # dtype: must be categorical or numeric
    if dtype == "categorical":
        if "unknown" in list(df[hue]):
            hue_order = np.unique(df[hue])[0:len(np.unique(df[hue]))-1]
            hue_order = np.insert(hue_order, 0, "unknown")
        else:
            hue_order = np.unique(df[hue])
        
        palette = palette 
        if len(np.unique(df[hue])) > len(sns.color_palette("tab20")):
            palette = None
        
        if palette is None:
            with plt.rc_context({"figure.figsize": figsize, "figure.dpi": 300, "figure.frameon": True}):
                g=sns.scatterplot(x="UMAP_1", y="UMAP_2", 
                              hue=hue, data=df, legend="full", alpha=0.8, hue_order = hue_order)
                g.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
                fig = g.get_figure()
                sns.set_theme(style='white')
                fig.tight_layout()
                gen_mpl_labels_df(
            df,
            hue, 
            exclude=("None",),  # This was before we had the `nan` behaviour
            adjust_kwargs=dict(arrowprops=dict(arrowstyle='-', color='black')),
            text_kwargs=dict(fontsize=14),)
                plt.savefig(os.path.join(out_dir,filename),bbox_inches="tight")
                if show == True:
                    plt.show()
            plt.close()
            
        else: 
            with plt.rc_context({"figure.figsize": figsize, "figure.dpi": 300, "figure.frameon": True}):
                g=sns.scatterplot(x="UMAP_1", y="UMAP_2", palette = palette,
                              hue=hue, data=df, legend="full", alpha=0.8, hue_order = hue_order)
                g.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
                fig = g.get_figure()
                sns.set_theme(style='white')
                fig.tight_layout()
                gen_mpl_labels_df(df,hue, exclude=("None",),  # This was before we had the `nan` behaviour
                adjust_kwargs=dict(arrowprops=dict(arrowstyle='-', color='black')),
                text_kwargs=dict(fontsize=14),)
                plt.savefig(os.path.join(out_dir,filename),bbox_inches="tight")
                if show == True:
                    plt.show()
            plt.close()
            
    elif dtype == "numerical":
        with plt.rc_context({"figure.figsize": figsize, "figure.dpi": 300, "figure.frameon": True}):
            plt.scatter(df["UMAP_1"], df["UMAP_2"], alpha = .8, c = df[hue])
            plt.title("Uncertainty score UMAP")
            plt.xlabel("UMAP_1")
            plt.ylabel("UMAP_2")
            cbar = plt.colorbar()
            plt.savefig(os.path.join(out_dir,filename),bbox_inches="tight")
            if show == True:
                plt.show()
            plt.close()
    else: raise ValueError("dtype must be eigher categorical or numerical")

def scATAnno_plotting_umap(adata, hue, palette_dictionary = None, palette = None, out_dir=None, filename=None, dtype = None, title = None, show = False, figsize=(6,6), _ax =None, size=None, hue_order=None):
    """
    Return umap plot.

    Parameters
    ----------
    adata: anndata that has umap information
    hue: anndata variable 
    out_dir: output directory
    filename: output filename
    dtype: datatype of hue parameter: None, categorical or numerical 
    """
    
    if dtype is None:
        if (palette is None) and (palette_dictionary is None):
            palette = "tab20" 
            if len(np.unique(adata.obs[hue])) > len(sns.color_palette("tab20")):
                palette = None
            if (out_dir is None) and (filename is None):
                sc.pl.umap(adata, color=hue, show=True, title=title, palette=palette, ax=_ax, size=size)
                return
            sc.settings.autosave = True
            sc.settings.figdir = os.path.join(out_dir) # change
            with plt.rc_context({"figure.figsize": figsize, "figure.dpi": 300, "figure.frameon": True}):
                sc.pl.umap(adata, color=hue, show = show, ax=_ax, title=title, palette=palette, size=size,  save = "_{}".format(filename))
                plt.title(title, fontweight='bold')
                plt.close()
                sc.settings.autosave = False
        
        if palette is not None:
            palette = palette
            if (out_dir is None) and (filename is None):
                sc.pl.umap(adata, color=hue, show=True, title=title, palette=palette, ax=_ax, size=size)
                return            
            sc.settings.autosave = True
            sc.settings.figdir = os.path.join(out_dir)
            with plt.rc_context({"figure.figsize": figsize, "figure.dpi": 300, "figure.frameon": True}):
                sc.pl.umap(adata, color=hue, show = show, ax=_ax, title=title, palette=palette, size=size,  save = "_{}".format(filename))
                plt.title(title, fontweight='bold')
                plt.close()
                sc.settings.autosave = False
                
        if  palette_dictionary is not None:
            if (out_dir is None) and (filename is None):
                sc.pl.umap(adata, color=hue, show=True, title=title, palette=palette_dictionary, ax=_ax, size=size)
                return
            adata.obs[hue] = adata.obs[hue].astype({hue:'category',})
            if hue_order is None:
                adata.obs[hue].cat.reorder_categories(np.unique(adata.obs[hue]), inplace=True)
            else: adata.obs[hue].cat.reorder_categories(hue_order, inplace=True)
                
            sc.settings.autosave = True
            sc.settings.figdir = os.path.join(out_dir) # change
            with plt.rc_context({"figure.figsize": figsize, "figure.dpi": 300, "figure.frameon": True}):
                sc.pl.umap(adata, color=hue, show = show, ax=_ax, title=title, palette=palette_dictionary, size=size,  save = "_{}".format(filename))
                plt.title(title, fontweight='bold')
                plt.close()
                sc.settings.autosave = False
            return
       
    elif dtype == "categorical":
        adata.obs[hue] = adata.obs[hue].astype({hue:'category',})
        if hue_order is None:
            adata.obs[hue].cat.reorder_categories(np.unique(adata.obs[hue]), inplace=True)
        else: adata.obs[hue].cat.reorder_categories(hue_order, inplace=True)
            
        if (palette is None) and (palette_dictionary is None):
            palette = "tab20" 
            if len(np.unique(adata.obs[hue])) > len(sns.color_palette("tab20")):
                palette = None
            with plt.rc_context({"figure.figsize": figsize, "figure.dpi": 300, "figure.frameon": True}):
                ax = sc.pl.umap(adata, color=hue, show=show, legend_loc=None, title=title, palette=palette, size=size)
                gen_mpl_labels(
                    adata,
                    hue,
                    exclude=("None",),  # This was before we had the `nan` behaviour
                    ax=ax,
                    adjust_kwargs=dict(arrowprops=dict(arrowstyle='-', color='black')),
                    text_kwargs=dict(fontsize=14, weight="bold"),)
                fig = ax.get_figure()
                fig.tight_layout()
                plt.title(title, fontweight='bold')
                if (out_dir is None) and (filename is None):
                    plt.show()
                    return
                plt.savefig(os.path.join(out_dir,filename))
                plt.close()
                return 
        if palette is not None:
            palette = palette
            with plt.rc_context({"figure.figsize": figsize, "figure.dpi": 300, "figure.frameon": True}):
                ax = sc.pl.umap(adata, color=hue, show=show, legend_loc=None, title=title, palette=palette, size=size)
                gen_mpl_labels(
                    adata,
                    hue,
                    exclude=("None",),  # This was before we had the `nan` behaviour
                    ax=ax,
                    adjust_kwargs=dict(arrowprops=dict(arrowstyle='-', color='black')),
                    text_kwargs=dict(fontsize=14, weight="bold"),)
                fig = ax.get_figure()
                fig.tight_layout()
                plt.title(title, fontweight='bold')
                if (out_dir is None) and (filename is None):
                    plt.show()
                    return
                plt.savefig(os.path.join(out_dir,filename))
                plt.close()
                return 
        if  palette_dictionary is not None:
            with plt.rc_context({"figure.figsize": figsize, "figure.dpi": 300, "figure.frameon": True}):
                ax = sc.pl.umap(adata, color=hue, show=show, legend_loc=None, title=title, palette=palette_dictionary, size=size)
                gen_mpl_labels(
                    adata,
                    hue,
                    exclude=("None",),  # This was before we had the `nan` behaviour
                    ax=ax,
                    adjust_kwargs=dict(arrowprops=dict(arrowstyle='-', color='black')),
                    text_kwargs=dict(fontsize=14, weight="bold"),)
                fig = ax.get_figure()
                fig.tight_layout()
                plt.title(title, fontweight='bold')
                if (out_dir is None) and (filename is None):
                    plt.show()
                    return
                plt.savefig(os.path.join(out_dir,filename))
                plt.close()
                return 

    elif dtype == "numerical":
        with plt.rc_context({"figure.figsize": figsize, "figure.dpi": 300, "figure.frameon": True}):
            ax = sc.pl.umap(adata, color=hue, show=show, legend_loc=None, title=title, size=size, ax = _ax)
            fig = ax.get_figure()
            fig.tight_layout()
            plt.title(title, fontweight='bold')
            if (out_dir is None) and (filename is None):
                plt.show()
                return
            plt.savefig(os.path.join(out_dir,filename))
            plt.close()
            return 
    else: raise ValueError("dtype of variable must be specified as None, categorical or numerical")

        
def defaultPlotting(figsize=(6,6), fontsize = 20, titlesize=20, labelsize=20, dpi=300,xtick_size=20, ytick_size=25): 
    # https://stackoverflow.com/questions/60878196/seaborn-rc-parameters-for-set-context-and-set-style
    sns.set(rc={'figure.figsize':figsize, "font.size":fontsize,"axes.titlesize":titlesize,"axes.labelsize":labelsize,"figure.dpi": dpi, "xtick.labelsize": xtick_size, "ytick.labelsize": ytick_size,},style="white")
    
def defaultPlotting_umap():
    plt.rcParams['figure.figsize'] = (6,6)
    plt.rcParams['axes.titleweight'] = "bold"
    plt.rcParams['axes.titlesize'] = 20
    plt.rcParams['axes.labelsize'] = 20
    plt.rcParams['xtick.labelsize'] = 20
    plt.rcParams['xtick.labelsize'] = 20


def get_palettes(name = "default102"):
    """
    Return palette

    Parameters
    ----------
    name: Must be 'default102' or 'default28'
    """
    
    if name == "default102":
        # from http://godsnotwheregodsnot.blogspot.de/2012/09/color-distribution-methodology.html
        godsnot_102 = [
                        # "#000000",  # remove the black, as often, we have black colored annotation
                        "#FFFF00",
                        "#1CE6FF",
                        "#FF34FF",
                        "#FF4A46",
                        "#008941",
                        "#006FA6",
                        "#A30059",
                        "#FFDBE5",
                        "#7A4900",
                        "#0000A6",
                        "#63FFAC",
                        "#B79762",
                        "#004D43",
                        "#8FB0FF",
                        "#997D87",
                        "#5A0007",
                        "#809693",
                        "#6A3A4C",
                        "#1B4400",
                        "#4FC601",
                        "#3B5DFF",
                        "#4A3B53",
                        "#FF2F80",
                        "#61615A",
                        "#BA0900",
                        "#6B7900",
                        "#00C2A0",
                        "#FFAA92",
                        "#FF90C9",
                        "#B903AA",
                        "#D16100",
                        "#DDEFFF",
                        "#000035",
                        "#7B4F4B",
                        "#A1C299",
                        "#300018",
                        "#0AA6D8",
                        "#013349",
                        "#00846F",
                        "#372101",
                        "#FFB500",
                        "#C2FFED",
                        "#A079BF",
                        "#CC0744",
                        "#C0B9B2",
                        "#C2FF99",
                        "#001E09",
                        "#00489C",
                        "#6F0062",
                        "#0CBD66",
                        "#EEC3FF",
                        "#456D75",
                        "#B77B68",
                        "#7A87A1",
                        "#788D66",
                        "#885578",
                        "#FAD09F",
                        "#FF8A9A",
                        "#D157A0",
                        "#BEC459",
                        "#456648",
                        "#0086ED",
                        "#886F4C",
                        "#34362D",
                        "#B4A8BD",
                        "#00A6AA",
                        "#452C2C",
                        "#636375",
                        "#A3C8C9",
                        "#FF913F",
                        "#938A81",
                        "#575329",
                        "#00FECF",
                        "#B05B6F",
                        "#8CD0FF",
                        "#3B9700",
                        "#04F757",
                        "#C8A1A1",
                        "#1E6E00",
                        "#7900D7",
                        "#A77500",
                        "#6367A9",
                        "#A05837",
                        "#6B002C",
                        "#772600",
                        "#D790FF",
                        "#9B9700",
                        "#549E79",
                        "#FFF69F",
                        "#201625",
                        "#72418F",
                        "#BC23FF",
                        "#99ADC0",
                        "#3A2465",
                        "#922329",
                        "#5B4534",
                        "#FDE8DC",
                        "#404E55",
                        "#0089A3",
                        "#CB7E98",
                        "#A4E804",
                        "#324E72",
                        ]

        default_102 = godsnot_102
        return default_102
    
    if name == "default28":
        zeileis_28 = [
                    "#023fa5",
                    "#7d87b9",
                    "#bec1d4",
                    "#d6bcc0",
                    "#bb7784",
                    "#8e063b",
                    "#4a6fe3",
                    "#8595e1",
                    "#b5bbe3",
                    "#e6afb9",
                    "#e07b91",
                    "#d33f6a",
                    "#11c638",
                    "#8dd593",
                    "#c6dec7",
                    "#ead3c6",
                    "#f0b98d",
                    "#ef9708",
                    "#0fcfc0",
                    "#9cded6",
                    "#d5eae7",
                    "#f3e1eb",
                    "#f6c4e1",
                    "#f79cd4",
                    # these last ones were added:
                    '#7f7f7f',
                    "#c7c7c7",
                    "#1CE6FF",
                    "#336600",
                    ]
        default_28 = zeileis_28
        return default_28
    else: raise ValueError("Parameter must be specified as 'default28' or 'default102'")

