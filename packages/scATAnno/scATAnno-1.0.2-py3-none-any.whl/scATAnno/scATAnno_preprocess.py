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

def h5ad2mtx(infile_path, out_dir):
    """convert the H5AD Anndata into MTX and TSV files
    Parameters
    ----------
    infile_path: path to h5ad data
    out_dir: output directory where MTX and TSV files are stored
    Returns
    -------
    """
    anndata = sc.read_h5ad(infile_path)
    X = csr_matrix(anndata.X)
    if scipy.sparse.isspmatrix(X) ==True:
        scipy.io.mmwrite(os.path.join(out_dir, 'matrix.mtx'),X)
        anndata.obs.to_csv(os.path.join(out_dir, 'barcodes.tsv'), sep='\t')
        anndata.var.to_csv(os.path.join(out_dir, 'features.tsv'), sep='\t')
    else: print("convert not successful")
        
def load_reference_data(path):
    """read reference atlas
    Parameters
    ----------
    path: path to reference h5ad data 
    Returns reference anndata
    -------
    If h5ad file not found, search for MTX and TSV files; if none found, raise error
    """
    parent_path = os.path.dirname(os.path.normpath(path))
    if os.path.isfile(path):
        try:
            reference_data = sc.read_h5ad(path)
            reference_data.obs['dataset'] = "reference"
            return reference_data
        except OSError as error:
            print("refernce anndata not found")
            pass
    elif os.path.isfile(os.path.join(parent_path, "atac_atlas.mtx")) & os.path.isfile(os.path.join(parent_path, "atac_atlas_genes.tsv")) & os.path.isfile(os.path.join(parent_path, "atac_atlas_cellbarcodes.tsv")):
        reference_data = convert_mtx2anndata_simple(path, mtx_file = "atac_atlas.mtx",cells_file = "atac_atlas_cellbarcodes.tsv",features_file = "atac_atlas_genes.tsv")
        return reference_data
    else: raise FileNotFoundError

def import_query_data(path, mtx_file,cells_file,features_file, variable_prefix, celltype_col="celltypes", add_metrics = True):
    """convert the count matrix into an anndata.
    Parameters
    ----------
    path: data directory including mtx, barcodes and features
    mtx_file: mtx filename 
    cells_file: cell barcode filename
    features_file: feature filename
    variable_prefix: sample name prefix
    celltype_col: column name of cell types, default is "celltypes"
    add_metrics: whether adding metadata of metrics from QuickATAC
    
    Returns a AnnData object
    -------
    """
    # create anndata
    data = sc.read_mtx(os.path.join(path,mtx_file))
    data = data.T
    features = pd.read_csv(os.path.join(path, features_file), header=None, sep= '\t')
    barcodes = pd.read_csv(os.path.join(path, cells_file), header=None)

    # Split feature matrix and set peak separated by (:, -) to match reference peaks
    data.var_names = features[0]
    data.obs_names = barcodes[0]
    
    data.obs[celltype_col] = variable_prefix
    data.obs['tissue'] = variable_prefix
    data.obs['dataset'] = variable_prefix
    
    # remove spike-in cell
    data = data[data.obs.index != "spike-in"]
    # add qc filtering metrics from quickATAC if add_metrics set to true
    if add_metrics == True:
        import glob
        try:
            metrics_filepath = glob.glob(os.path.join(path, "*meta*"))[0]
            metrics = pd.read_csv(metrics_filepath, sep='\t', index_col=0)
            metrics = metrics[metrics.index != "spike-in"]
            data.obs = pd.merge(data.obs, metrics, right_index=True, left_index = True)
        except OSError as error:
            import warnings
            warnings.warn('Metrics file not found, anndata returned with no meta metrics')
            return data
    return data


def add_variable(variable_file, adata, variable_col="X_spectral_harmony"):
    """add X_spectral variable to an anndata.
    Parameters
    ----------
    variable_file: X_Spectral file path
    adata: anndata input 
    variable_col: the column name of new variable in anndata
    Returns a AnnData object
    -------
    """
    if os.path.isfile(variable_file):
        X_spectral = pd.read_csv(os.path.join(variable_file), index_col=0)
        X_spectral = X_spectral.loc[adata.obs.index]
        adata.obsm[variable_col] = X_spectral
        return adata
    else: raise ValueError("file does not exist")




