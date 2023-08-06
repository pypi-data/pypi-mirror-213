import scanpy as sc
import pandas as pd
from scipy.sparse import csr_matrix
from scipy import sparse
import scipy.io
import os
import anndata as ad # Anndata version must > 0.8
import harmonypy
from adjustText import adjust_text
import numpy as np
import matplotlib.pyplot as plt
import time
from anndata._core.aligned_mapping import AxisArrays
from anndata.experimental import AnnCollection
import math
from scipy.spatial.distance import pdist, squareform
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

from scATAnno.SnapATAC2_spectral import *
from scATAnno.SnapATAC2_tools import *
from scATAnno.scATAnno_preprocess import *
from scATAnno.scATAnno_integration import *


######## Functions for KNN assignment ########
def KNN_classifier(reference, query, low_dim_col, n_neighbors, celltype_col):
    """
    Train KNN classifier on reference dataset, and obtain K-nearest neighbors reference cells for each query cell c
    
    Parameters
    ----------
    low_dim_col: low_dim_col
    celltype_col: reference cell type column: label

    Return
    ----------
    return matrix of query cells x index of Nc; return second matrix of query cells x distance of Nc
    """
    
    neighbors = NearestNeighbors(n_neighbors=n_neighbors).fit(reference.obsm[low_dim_col])
    res = neighbors.kneighbors(query.obsm[low_dim_col])
    dists = res[0]
    indices = res[1]
    neighbors_labels = np.vectorize(lambda i: reference.obs[celltype_col][i])(indices)
    sigma = get_sigmas(dists)
    return dists, indices, neighbors_labels, sigma


def get_sigmas(dists):
    sigma = []
    for row in dists:
        s = (sum( x**2.0 for x in row ) / float(len(row)) )**0.5
        sigma.append(s)
    return sigma


def gaussian_kernal(dists, sigma):
    # gaussian kernel function to convert distance to similarity scores
    sigma_n = np.array(sigma)[:, np.newaxis]
    K = np.exp(-dists / ( (2 / sigma_n) **2))
    return K

# Assign celltype labels without filtering by uncertainty score
def raw_assignment(K, neighbors_labels):
    prediction = []
    uncertainty = []
    for i in range(K.shape[0]):
        c_label = neighbors_labels[i,:]
        c_D = K[i,:]
        c_df = pd.DataFrame({'label': c_label,'dist': c_D})
        p = c_df.groupby('label').sum('dist')/np.sum(c_df['dist'])
        u = 1 - p
        pred_y = u.index[np.argmin(u)]
        prediction.append(pred_y)
        uncertainty.append(np.min(u).values[0])
    return prediction, uncertainty


def scATAnno_KNN_assign(reference, query, reference_label_col, low_dim_col="X_spectral_harmony", knn_neighbors=30, in_place=True):
    """
    Return query data with weighted distance-based annotation

    Parameters
    ----------
    reference: anndata for reference cells
    query: anndata of query cells
    reference_label_col: celltype label column of reference atlas
    """
    
    dists, indices, neighbors_labels, sigma = KNN_classifier(reference, query, low_dim_col = low_dim_col, n_neighbors = knn_neighbors,celltype_col = reference_label_col)
    
    K = gaussian_kernal(dists, sigma)
    
    pred_res_major = raw_assignment(K, neighbors_labels)
   
    if in_place:
        query.obsm["kernel_distance"] = K
        query.obsm["distance"] = dists
        query.obsm["indices"] = indices
        query.obsm["neighbors_labels"] = neighbors_labels
        
        pred_label_major = pred_res_major[0]
        query.obs["uncertainty_score_step1"] = pred_res_major[1]
        query.obs["pred_y"] = pred_label_major
        return query
    else: return pred_res_major

######## Functions for weighted distance-based assignment ########
def create_label_dict(celltypes):
    cat_dict = {}
    for i in range(len(celltypes)):
        cat_dict[celltypes[i]] = i
    return cat_dict


def get_centroids(mat, threshold = 25):
    # remove upper and lower percentile of values, and get median value for each dimension
    list_mat = []
    # iterate over each column/dimension of matrix
    for j in range(mat.shape[1]):
        col = mat[:, j]
        # obtain lower and upper cutoff for each dimension
        lo_cutoff = np.percentile(col, threshold)
        hi_cutoff = np.percentile(col, 100 - threshold)
        # remove values lower than lo_cutoff and higher than hi_cutoff
        col_new = col[col >= lo_cutoff]
        col_new = col_new[col_new <= hi_cutoff]
        # append new dimension to list_mat
        list_mat.append(col_new)
    # compute new centroids based on filtered values
    centroids = [ np.median(list_mat[i])  for i in range(len(list_mat))]
    return list_mat, centroids


def compute_centroid_distance(vector, c1, c2):
    # compute weights of spectral embeddings
    dist1 = abs(vector - c1)
    dist1 = np.sqrt(dist1**2)
    
    dist2 = abs(vector - c2)
    dist2 = np.sqrt(dist2**2)
    
    return dist1, dist2

def compute_centroid_weight(celltypes, df, ndims = 30, percentile_cutoff = 25, celltype_col = "major_celltype"):
    # create an empy matrix to store weighted distance (celltype-by-embedding matrix)
    S = np.zeros((celltypes.shape[0], ndims))
    # distances of reference cells to its own centroid
    D_self = []
    # distances of reference cells to the other centroid
    D_other = []
    for i in range(len(celltypes)):
        # obtain cell-by-embedding matrix of reference cells of i celltype (cells S?????)
        mat1 = df[df[celltype_col] == celltypes[i]]
        mat1 = np.array(mat1.iloc[:,0:ndims])
        # obtain cell-by-embedding matrix of reference cells of non i celltype (cells D)
        mat2 = df[df[celltype_col] != celltypes[i]]
        mat2 = np.array(mat2.iloc[:,0:ndims])

        _, c1 = get_centroids(mat1, threshold = percentile_cutoff)
        _, c2 = get_centroids(mat2, threshold = percentile_cutoff)
        
        # S1, S2: create an empty matrix [n reference cells of i celltype, ndim]
        S1 = np.zeros((mat1.shape[0], mat1.shape[1]))
        S2 = np.zeros((mat1.shape[0], mat1.shape[1])) 
        
        for j in range(mat1.shape[0]):
            # dist1: distance of a reference cell to its own centroid 1 
            # dist2: distance of a reference cell to another centroid 2
            dist1, dist2 = compute_centroid_distance(mat1[j], c1, c2) 
            # S1: distances of reference cells of i celltype to centroid 1
            S1[j] = dist1
            # S2: distances of reference cells of i celltype to centroid 2
            S2[j] = dist2
     
        assert S1.shape == S2.shape
        
        D_self.append(S1)
        D_other.append(S2)
        # for each celltype, compute the ratio of (average S2)/(average S1)
        S_  = S2.mean(axis = 0, keepdims = True)/S1.mean(axis = 0, keepdims = True)
        S[i] = S_
    # Normalized weights
    S_norm = S / np.sum(S, axis=1)[:, np.newaxis] 
    return S_norm, S, D_self, D_other

def weight_per_cell(vector, ref_mat, weight_mat):
    dist = abs(vector - ref_mat)
    w_dist = dist*weight_mat
    rowsum = np.sum(w_dist, axis=1)**2
    weighted_dist = np.sqrt(rowsum)
    #weighted_dist = np.dot(w_dist, w_dist.T)
    return weighted_dist

def compute_weighted_distance(embedding, centroid, weight):
    distance = np.array(embedding) - np.array(centroid)
    distance = np.sqrt(distance**2)
    distance = distance * weight
    return distance

def identify_center_cells(adata, variable_col,umap_threshold=15,  use_rep = 'X_spectral_harmony', ndim=30 ):
    umap_centroid_cellname = {}
    umap_centroid_index = {}
    umap_centroid_spectral = {}
    for celltype in np.unique(adata.obs[variable_col]):
        selected_celltype = adata[adata.obs[variable_col].isin([celltype])]
        # get centroid of UMAP
        umap_selected_celltype = selected_celltype.obsm['X_umap']
        # remove top and bottom 15 percentile of UMAP embeddings
        _, centroids = get_centroids(umap_selected_celltype, threshold = umap_threshold)
        # get the cell with smallest distance to the centroid
        diff = []
        for i in range(umap_selected_celltype.shape[0]):
            vector = umap_selected_celltype[i,:]
            diff.append(np.sum(abs(vector - centroids)))
        # get index of the cell
        cell_idx_closest_to_centroid = np.argmin(diff)
        # cell_name = selected_celltype.obs.index[cell_idx_closest_to_centroid,]
        cell_name = selected_celltype.obs.index[cell_idx_closest_to_centroid]
        umap_centroid_cellname[celltype] = cell_name
        umap_centroid_index[celltype] = cell_idx_closest_to_centroid 
        # get the embedding of the cell
        spectral_embedding = np.array(selected_celltype.obsm[use_rep])[cell_idx_closest_to_centroid,]
        umap_centroid_spectral[celltype] = np.array(spectral_embedding[0:ndim])
    return umap_centroid_cellname, umap_centroid_index, umap_centroid_spectral

# remove outlier cells of each reference cell type and recompute new centroid 
def remove_outliers(adata, variable_col, outlier_umap_cutoff = 90, use_rep = 'X_spectral_harmony', ndim=30):
    # 1. obtain cell closest to the UMAP centroid of each cell type
    umap_centroid_cellname, umap_centroid_index, umap_centroid_spectral = identify_center_cells(adata, use_rep=use_rep, ndim=ndim, variable_col = variable_col)
    # 2. Remove outlier cells for each celltype
    outlier_umap_cutoff = outlier_umap_cutoff
    celltypes = np.unique(adata.obs[variable_col])
    
    reference_dists = {}
    reference_clean = []
    for i in celltypes:
        selected_celltype = adata[adata.obs[variable_col].isin([i])]
        umap_selected_celltype = selected_celltype.obsm["X_umap"]
        centroid_umap = umap_selected_celltype[umap_centroid_index[i],:]

        distance = np.array(umap_selected_celltype) - np.array(centroid_umap)
        distance = np.sqrt(distance**2)

        total_dist = np.sum(distance, axis = 1)
        reference_dists[i] = total_dist

        cutoff = np.percentile(total_dist, outlier_umap_cutoff)
        ref_tmp_clean = selected_celltype[total_dist <= cutoff]
        reference_clean.append(ref_tmp_clean)
    
    reference_clean = ad.concat(reference_clean)
    
    # 3. calculate new cell closest to the UMAP centroid of each cell type
    umap_centroid_cellname, umap_centroid_index, umap_centroid_spectral = identify_center_cells(reference_clean, use_rep=use_rep, ndim=ndim, variable_col =variable_col)
    return reference_clean, umap_centroid_cellname, umap_centroid_index, umap_centroid_spectral

def compute_embedding_weights(adata, variable_col, use_rep = "X_spectral_harmony",  ndim = 30):
    # obtain weights for spectral embedding using reference atlas
    if ndim is None:
        ndim = adata.obsm[use_rep].shape[1]
    else: ndim = ndim
    # Obtain reference cells
    spectral = pd.DataFrame(adata.obsm[use_rep]).iloc[:, 0:ndim]
    spectral.columns = ["Spectral_{}".format(i) for i in range(ndim)]
    spectral.index = adata.obs.index
    df = pd.DataFrame(spectral)
    df = df.assign(major_celltype  = adata.obs[variable_col])
    celltypes = np.unique(df['major_celltype'])
    label_dict = create_label_dict(celltypes)
    
    S_norm_centroid, S_centroid, D_self_centroid, D_other_centroid = compute_centroid_weight(celltypes, df = df.copy(), percentile_cutoff = 15, celltype_col = "major_celltype")
    weight_df = pd.DataFrame(S_norm_centroid, columns = ["Spec " + str(i) for i in range(ndim)], index = celltypes)
    return weight_df

def _get_reference_distribution(adata, weight_df, umap_centroid_spectral, variable_col, ndim, use_rep = "X_spectral_harmony"):
    reference_total_dists = {}
    celltypes = np.unique(adata.obs[variable_col])
    for i in celltypes:
        ref_tmp = adata[adata.obs[variable_col].isin([i])]
        weight = np.array(weight_df.loc[i,:])
        embedding = pd.DataFrame(ref_tmp.obsm[use_rep]).iloc[:,0:ndim]
        centroid = umap_centroid_spectral[i] 
        distance = np.array(embedding) - np.array(centroid)
        distance = np.sqrt(distance**2)
        distance = distance * weight
        total_dist = np.sum(distance, axis = 1)
        reference_total_dists[i] = total_dist
    return reference_total_dists

def _distance_filter(query, weight_df,umap_centroid_spectral,reference_total_dists, use_rep = "X_spectral_harmony", percent_threshold = 95, prediction_col='pred_y', ndim = 30):
    """
    Return reference atlas removed outliers, weights of spectral embedding, and secondPass annotation of query data

    Parameters
    ----------
    prediction_col: query celltype column to perform secondpass filtering and annotation
    percent_threshold: query distance cutoff for celltye assignment
    """
    percent_threshold = percent_threshold
    # compute corrected predictions using weighted distance
    corrected_predictions = []
    corrected_uncertainty = []

    for i in range(len(query.obs[prediction_col])):
        # obtain prediction of query cells
        prediction = query.obs[prediction_col][i]
        #if prediction != "unknown":
        weight = np.array(weight_df.loc[prediction,:])
        # obtain centroid of the predicted celltype
        centroid = umap_centroid_spectral[prediction]
        # obtain query embeddings of a given centroid
        query_embedding = np.array(query.obsm[use_rep])[i,0:ndim]
        # compute query-ref centroid distance
        distance_query = np.array(query_embedding) - np.array(centroid)
        distance_query = np.sum(np.sqrt(distance_query**2) * weight)

        cutoff = np.percentile(reference_total_dists[prediction], percent_threshold)
        if distance_query >= cutoff:
            corrected_uncertainty.append(1.0)
        else:
            corrected_uncertainty.append(0.0)
      
    query.obs["uncertainty_score_step2"] = corrected_uncertainty
    return query

def distance_filter(reference, query, reference_label_col, outlier_umap_cutoff=90,use_rep = "X_spectral_harmony",  prediction_col='pred_y',  ndim = 30, percent_threshold = 95, draw_dist = False):
    """
    Return reference atlas removed outliers, weights of spectral embedding, and secondPass annotation of query data

    Parameters
    ----------
    reference_label_col: reference celltype column to generate embedding weights
    outlier_umap_cutoff: reference umap cutoff to remove outliers
    prediction_col: query predicted celltype column to perform annotation
    percent_threshold: query distance cutoff for celltye assignment
    """
    # 1. remove outlier cells in reference data based on umap
    reference_clean, umap_centroid_cellname, umap_centroid_index, umap_centroid_spectral = remove_outliers(reference, outlier_umap_cutoff = outlier_umap_cutoff,use_rep=use_rep,variable_col=reference_label_col,ndim = ndim )
    # 2. compute embedding weights for each celltype using clean reference data
    weight_df = compute_embedding_weights(reference_clean, use_rep=use_rep,variable_col=reference_label_col,ndim=ndim)
    # 3. compute reference celltype distance distribution
    reference_total_dists = _get_reference_distribution(reference_clean, weight_df, umap_centroid_spectral, ndim=ndim, use_rep=use_rep,variable_col=reference_label_col)
    # 4. assign query celltypes based on reference distance distribution
    query = _distance_filter(query, weight_df,umap_centroid_spectral,reference_total_dists,use_rep=use_rep, prediction_col=prediction_col,  ndim=ndim, percent_threshold = percent_threshold)
    if draw_dist==True:
        return reference_clean, weight_df, query, reference_total_dists,umap_centroid_spectral
    else: 
        return reference_clean, weight_df, query

def curate_celltype_names(l, atlas):
    """
    Return a list with curated cell type based on the reference atlas
    """
    if atlas == "PBMC":
        l_new = [ 'Naive CD4 T' if i == 'Naive Treg' else i for i in l]
        l_new = [ 'NK' if i == 'Mature NK' or (i=='Immature NK') else i for i in l_new]

    elif atlas == "HealthyAdult":
        curated_major = []
        for i in l:
            if i == "B Lymphocyte":
                curated_major.append("Immune Cells")
            elif i == "T Lymphocyte":
                curated_major.append("Immune Cells")
            elif i == 'Myeloid / Macrophage':
                curated_major.append("Immune Cells")
            else: curated_major.append(i)
        l_new = curated_major
        
    elif atlas == "TIL":
        l_new = l
        #todo: merge NK1 and NK2
    else:
        l_new = l 
    return l_new

def assign_final_cell_type(query, threshold, atlas, predicted_variable = "pred_y", u1_variable = "uncertainty_score_step1", u2_variable = "uncertainty_score_step2"):
    """
    Return query data with final uncertainty score and predicted cell type at cell level

    Parameters
    ----------
    threshold: threshold for uncertainty score and detect unknown cells
    predicted_variable: assignment from KNN
    u1_variable: uncertainty score fron KNN first step
    u2_variable: uncertainty score fron distance second step
    """
    u_list = [] # final uncertainty score
    y2_list = [] # distance corrected celltype
    y1_list = [] # KNN-based uncertainty celltype
    for i in query.obs.index:
        y = query.obs.loc[i, predicted_variable]
        u1 = query.obs.loc[i, u1_variable]
        
        if u1 <= threshold:
            y1_list.append(y)
        else:
            y1_list.append("unknown")
        
        u2 = query.obs.loc[i, u2_variable]
        u = np.max([u1,u2])
        u_list.append(u)
        if u <= threshold:
            y2_list.append(y)
        else:
            y2_list.append("unknown")
          
    
    query.obs["Uncertainty_Score"] = u_list
    query.obs["1.knn-based_celltype"] = curate_celltype_names(y1_list, atlas)
    query.obs["2.corrected_celltype"] = curate_celltype_names(y2_list, atlas)
    
    return query

def scATAnno_distance_assign(reference, query, reference_label_col, distance_threshold, atlas, uncertainty_threshold, use_rep = "X_spectral_harmony",  prediction_col='pred_y'):
    """
    Return query data with weighted distance-based annotation

    Parameters
    ----------
    reference: anndata for reference cells
    query: anndata of query cells
    reference_label_col: celltype label column of reference atlas
    atlas: selection of reference atlas
    distance_threshold: threshold for weighted distance filtering 
    uncertainty_threshold: final uncertainty score threshold
    prediction_col: predicted celltype column from KNN raw assignment for query data
    """
    reference_clean, weight_df, query_res1  = distance_filter(reference=reference, query=query, reference_label_col = reference_label_col, percent_threshold = distance_threshold, use_rep = use_rep, prediction_col=prediction_col)
    query_res2 = assign_final_cell_type(query=query_res1, threshold=uncertainty_threshold, atlas=atlas, predicted_variable = prediction_col, u1_variable = "uncertainty_score_step1", u2_variable = "uncertainty_score_step2")
    
    return query_res2

########## Functions for cluster level annotation ##########

def cluster_annotation_anndata(adata, prediction_col = None, cluster_col = None):
    if cluster_col is None:
        cluster_col = "Clusters"
    else: cluster_col = cluster_col
    
    if prediction_col is None:
        prediction_col = "corrected_pred_y_major"
    else: prediction_col = prediction_col
    
    if cluster_col in adata.obs.columns:
        cluster_anno_unstack = adata.obs.groupby(cluster_col)[prediction_col].value_counts().unstack()
    else: raise KeyError("Column {} Not Found in dataframe".format(cluster_col))
    
    cluster_group_anno = {}
    for i in cluster_anno_unstack.index:
        cluster_group_anno[i] = cluster_anno_unstack.columns[np.argmax(cluster_anno_unstack.loc[i,:])]
    
    cluster_annotations = []
    for cell_idx in range(adata.obs.shape[0]):
        key = adata.obs.iloc[cell_idx, :][cluster_col]
        anno = cluster_group_anno[key]
        cluster_annotations.append(anno)
    adata.obs['cluster_annotation'] = cluster_annotations
    return adata


def scATAnno_cluster_assign(query, use_rep, cluster_col=None, UMAP=True, leiden_resolution=3):
    """
    Return query data with cluster-level annotation

    Parameters
    ----------
    query: anndata of query cells
    cluster_col: if None, automatically cluster by leiden algorithm; otherwise, leiden cluster and then input cluster column name
    UMAP: if True, redo UMAP for query data; else, do not change UMAP
    """
    query_only_newUMAP = query.copy()
    if UMAP:
        sc.pp.neighbors(query_only_newUMAP, use_rep=use_rep)
        sc.tl.umap(query_only_newUMAP)
    if cluster_col is None:
        sc.tl.leiden(query_only_newUMAP,  key_added = "leiden", resolution = leiden_resolution)
        query_only_newUMAP = cluster_annotation_anndata(query_only_newUMAP,  cluster_col = "leiden", prediction_col = "2.corrected_celltype")
    else:
        query_only_newUMAP = cluster_annotation_anndata(query_only_newUMAP,  cluster_col = cluster_col, prediction_col = "2.corrected_celltype")

    return query_only_newUMAP


########## One Function wrapping up all steps ##########
def scATAnno_annotate(reference, query, reference_label_col, atlas, distance_threshold, uncertainty_threshold, 
           cluster_col = None, UMAP = True, leiden_resolution = 3,use_rep="X_spectral_harmony",knn_neighbors=30,
          prediction_col="pred_y" ):
    """
    Return query data with annotation steps

    Parameters
    ----------
    reference: anndata of reference atlas
    query: anndata of query cells
    reference_label_col: celltype label column of reference atlas
    atlas: selection of reference atlas
    distance_threshold: threshold for weighted distance filtering 
    uncertainty_threshold: final uncertainty score threshold
    cluster_col: if None, automatically cluster by leiden algorithm; otherwise, leiden cluster and then input cluster column name
    UMAP: if True, redo UMAP for query data; else, do not change UMAP
    prediction_col: predicted celltype column from KNN raw assignment for query data
    """
    query_KNN = scATAnno_KNN_assign(reference, query, reference_label_col=reference_label_col, low_dim_col=use_rep, knn_neighbors=knn_neighbors, in_place=True)
    
    query_distance = scATAnno_distance_assign(reference, query_KNN, reference_label_col= reference_label_col, distance_threshold=distance_threshold, atlas=atlas, uncertainty_threshold=uncertainty_threshold, use_rep = use_rep,  prediction_col=prediction_col)

    # reference_clean, weight_df, query  = distance_filter(reference, query, reference_label_col = reference_label_col, prediction_col=prediction_col, use_rep = use_rep, percent_threshold = distance_threshold)
    # query = assign_final_cell_type(query, threshold=uncertainty_threshold, atlas = atlas, predicted_variable = prediction_col, u1_variable = "uncertainty_score_step1", u2_variable = "uncertainty_score_step2")
    
    query_only_newUMAP = scATAnno_cluster_assign(query_distance, use_rep=use_rep, cluster_col=cluster_col, UMAP=UMAP, leiden_resolution=leiden_resolution)

    
    return query_only_newUMAP


