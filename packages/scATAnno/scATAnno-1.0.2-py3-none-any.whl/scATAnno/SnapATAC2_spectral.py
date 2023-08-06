#import snapatac2 as snap
import scanpy as sc
import pandas as pd
from scipy.sparse import csr_matrix
import scipy.io
import os
import anndata as ad
import harmonypy
from adjustText import adjust_text
import numpy as np
import matplotlib.pyplot as plt
import time
import os.path
#####
from snapatac2._snapatac2 import jm_regress
#####
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity, rbf_kernel
import gc
from typing import Optional, Union
from anndata.experimental import AnnCollection
from ntpath import join
from typing import Union, Sequence, Literal, Optional, Dict
import collections.abc as cabc
import scipy.sparse as ss
from anndata import AnnData
from anndata.experimental import AnnCollection
import math

def read_as_binarized(adata: ad.AnnData) -> ss.spmatrix:
    grp = adata.file["X"]
    mtx = ss.csr_matrix(adata.shape, dtype=np.float64)
    mtx.indices = grp["indices"][...]
    mtx.indptr = grp["indptr"][...]
    mtx.data = np.ones(mtx.indices.shape, dtype=np.float64)
    return mtx

def binarized_chunk_X(
    adata: ad.AnnData,
    select: Union[int, Sequence[int], np.ndarray] = 1000,
    replace: bool = False,
) -> ss.spmatrix:
    """
    Return a chunk of the data matrix :attr:`X` with random or specified indices.

    Parameters
    ----------
    select
        Depending on the type:
        :class:`int`
            A random chunk with `select` rows will be returned.
        :term:`sequence` (e.g. a list, tuple or numpy array) of :class:`int`
            A chunk with these indices will be returned.
    replace
        If `select` is an integer then `True` means random sampling of
        indices with replacement, `False` without replacement.
    """
    if isinstance(select, int):
        select = select if select < adata.n_obs else adata.n_obs
        choice = np.random.choice(adata.n_obs, select, replace)
    elif isinstance(select, (np.ndarray, cabc.Sequence)):
        choice = np.asarray(select)
    else:
        raise ValueError("select should be int or array")

    reverse = None
    if adata.isbacked:
        # h5py can only slice with a sorted list of unique index values
        # so random batch with indices [2, 2, 5, 3, 8, 10, 8] will fail
        # this fixes the problem
        indices, reverse = np.unique(choice, return_inverse=True)
        selection = adata.X[indices.tolist()]
    else:
        selection = adata.X[choice]

    binarize_inplace(selection)
    return selection if reverse is None else selection[reverse]

def inplace_init_view_as_actual(data):
    """
    Replace view of backed AnnData with actual data
    """
    if data.isbacked and data.is_view:
        filename = str(data.filename)
        data.write()
        data.file.close()
        new_data = ad.read(filename, backed="r+")
        new_data.file.close()
        data._init_as_actual(
            obs=new_data.obs,
            var=new_data.var,
            uns=new_data.uns,
            obsm=new_data.obsm,
            varm=new_data.varm,
            varp=new_data.varp,
            obsp=new_data.obsp,
            raw=new_data.raw,
            layers=new_data.layers,
            shape=new_data.shape,
            filename=new_data.filename,
            filemode="r+",
        )

def binarize_inplace(X):
    """Binarize sparse matrix in-place"""
    X.data = np.ones(X.indices.shape, dtype=np.float64)

    
def select_features(
    adata: Union[ad.AnnData, AnnCollection],
    variable_feature: bool = True,
    whitelist: Optional[str] = None,
    blacklist: Optional[str] = None,
    inplace: bool = True,
) -> Optional[np.ndarray]:
    """
    Perform feature selection.

    Parameters
    ----------
    adata
        AnnData object
    variable_feature
        Whether to perform feature selection using most variable features
    whitelist
        A user provided bed file containing genome-wide whitelist regions.
        Features that are overlapped with these regions will be retained.
    blacklist 
        A user provided bed file containing genome-wide blacklist regions.
        Features that are overlapped with these regions will be removed.
    inplace
        Perform computation inplace or return result.
    
    Returns
    -------
    Boolean index mask that does filtering. True means that the cell is kept.
    False means the cell is removed.
    """
    if isinstance(adata, ad.AnnData):
        count = np.ravel(adata.X[...].sum(axis = 0))
    else:
        count = np.zeros(adata.shape[1])
        for batch, _ in adata.iterate_axis(5000):
            count += np.ravel(batch.X[...].sum(axis = 0))

    selected_features = count != 0

    if whitelist is not None:
        selected_features &= internal.intersect_bed(list(adata.var_names), whitelist)
    if blacklist is not None:
        selected_features &= not internal.intersect_bed(list(adata.var_names), blacklist)

    if variable_feature:
        mean = count[selected_features].mean()
        std = math.sqrt(count[selected_features].var())
        selected_features &= np.absolute((count - mean) / std) < 1.65

    if inplace:
        adata.var["selected"] = selected_features
    else:
        return selected_features

def spectral(
    data: ad.AnnData,
    n_comps: Optional[int] = None,
    features: Optional[Union[str, np.ndarray]] = "selected",
    random_state: int = 0,
    sample_size: Optional[Union[int, float]] = None,
    chunk_size: Optional[int] = None,
    distance_metric: str = "jaccard",
    inplace: bool = True,
) -> Optional[np.ndarray]:

    if isinstance(features, str):
        if features in data.var:
            features = data.var[features]
        else:
            raise NameError("Please call `select_features` first or explicitly set `features = None`")

    np.random.seed(random_state)
    if n_comps is None:
        min_dim = min(data.n_vars, data.n_obs)
        if 50 >= min_dim:
            n_comps = min_dim - 1
        else:
            n_comps = 50
    if chunk_size is None: chunk_size = 20000

    (n_sample, _) = data.shape
    ##### checked 
    if sample_size is None:
        sample_size = n_sample
    elif isinstance(sample_size, int):
        if sample_size <= 1:
            raise ValueError("when sample_size is an integer, it should be > 1")
        if sample_size > n_sample:
            sample_size = n_sample
    else:
        if sample_size <= 0.0 or sample_size > 1.0:
            raise ValueError("when sample_size is a float, it should be > 0 and <= 1")
        else:
            sample_size = int(sample_size * n_sample) 

    if sample_size >= n_sample: # sample size is entire sample
        if isinstance(data, AnnCollection):
            X, _ = next(data.iterate_axis(n_sample))
            X = X.X[...]
            if distance_metric == "jaccard":
                X.data = np.ones(X.indices.shape, dtype=np.float64)
        elif isinstance(data, ad.AnnData):
            if data.isbacked and data.is_view:
                    inplace_init_view_as_actual(data)
            X = data.X[...]
            if distance_metric == "jaccard":
                X.data = np.ones(X.indices.shape, dtype=np.float64)
        else:
            raise ValueError("input should be AnnData or AnnCollection")

        if features is not None: X = X[:, features]

        model = Spectral(n_dim=n_comps, distance=distance_metric)
        model.fit(X)
        result = model.transform() # save reference results 
    
    else: # if there is subsample
        if isinstance(data, AnnCollection):
            # Fix sample indices to 0:22200
            # need to fix axis 
            S, sample_indices = next(data.iterate_axis(sample_size, shuffle=True))
            S = S.X[...]
            if distance_metric == "jaccard":
                S.data = np.ones(S.indices.shape, dtype=np.float64)
            chunk_iterator = map(lambda b: b[0].X[...], data.iterate_axis(chunk_size))
        elif isinstance(data, ad.AnnData):
            if distance_metric == "jaccard":
                S = binarized_chunk_X(data, select=sample_size, replace=False) # resample density distribution?
            else:
                S = ad.chunk_X(data, select=sample_size, replace=False)
            chunk_iterator = map(lambda b: b[0], data.chunked_X(chunk_size))
        else:
            raise ValueError("input should be AnnData or AnnCollection")

        if features is not None: S = S[:, features]

        model = Spectral(n_dim=n_comps, distance=distance_metric) # construct and save model
        model.fit(S)   # fix reference; save model as object

        from tqdm import tqdm # show progression bar
        import math
        print("Perform Nystrom extension")
        for batch in tqdm(chunk_iterator, total = math.ceil(n_sample / chunk_size)): # n_sample = 22200; chunk_size = 20000
            if distance_metric == "jaccard":
                batch.data = np.ones(batch.indices.shape, dtype=np.float64)
            if features is not None: batch = batch[:, features]
            model.extend(batch) # input query as batch 
        result = model.transform() # result[0] evals; result[1] evecs # save results
    
    if inplace:
        data.uns['spectral_eigenvalue'] = result[0]
        data.obsm['X_spectral'] = result[1]
    else:
        return result

# def spectral_custom(
#     model,
#     data: ad.AnnData,
#     n_comps: Optional[int] = None,
#     features: Optional[Union[str, np.ndarray]] = "selected",
#     random_state: int = 0,
#     sample_size: Optional[Union[int, float]] = None,
#     chunk_size: Optional[int] = None,
#     distance_metric: str = "jaccard",
#     inplace: bool = True,
# ) -> Optional[np.ndarray]:

#     if isinstance(features, str):
#         if features in data.var:
#             features = data.var[features]
#         else:
#             raise NameError("Please call `select_features` first or explicitly set `features = None`")

#     np.random.seed(random_state)
#     if n_comps is None:
#         min_dim = min(data.n_vars, data.n_obs)
#         if 50 >= min_dim:
#             n_comps = min_dim - 1
#         else:
#             n_comps = 50
#     if chunk_size is None: chunk_size = 20000

#     (n_sample, _) = data.shape
#     ##### checked 
#     if sample_size is None:
#         sample_size = n_sample
#     elif isinstance(sample_size, int):
#         if sample_size <= 1:
#             raise ValueError("when sample_size is an integer, it should be > 1")
#         if sample_size > n_sample:
#             sample_size = n_sample
#     else:
#         if sample_size <= 0.0 or sample_size > 1.0:
#             raise ValueError("when sample_size is a float, it should be > 0 and <= 1")
#         else:
#             sample_size = int(sample_size * n_sample) ##### checked 
#     #if sample_size >= n_sample: # sample size is entire sample
#     if sample_size < n_sample: 
#         print("test")

#     else: # if there is subsample
#         if isinstance(data, AnnCollection):
#             print("anncollection")
            
#         elif isinstance(data, ad.AnnData):
#             print("input is anndata")
#             X = data.X[...]

#         from tqdm import tqdm # show progression bar
#         import math
#         print("Perform Nystrom extension")
#         if distance_metric == "jaccard":
#             X.data = np.ones(X.indices.shape, dtype=np.float64)
#         #if features is not None: data = data[:, features]
#         model.extend(X)
#         result = model.transform() # result[0] evals; result[1] evecs # save results
#     if inplace:
#         data.uns['spectral_eigenvalue'] = result[0]
#         data.obsm['X_spectral'] = result[1]
#     else:
#         return result




class Spectral:
    def __init__(self, n_dim=30, distance="jaccard"):

        #self.dim = mat.get_shape()[1]
        self.n_dim = n_dim
        self.distance = distance
        if (self.distance == "jaccard"):
            self.compute_similarity = jaccard_similarity
        elif (self.distance == "cosine"):
            self.compute_similarity = cosine_similarity
        else:
            self.compute_similarity = rbf_kernel

    def fit(self, mat):
        self.sample = mat
        self.dim = mat.shape[1]
        self.coverage = mat.sum(axis=1) / self.dim
        print("Compute similarity matrix")
        A = self.compute_similarity(mat)

        if (self.distance == "jaccard"):
            print("Normalization")
            self.normalizer = JaccardNormalizer(A, self.coverage)
            self.normalizer.normalize(A, self.coverage, self.coverage)
            np.fill_diagonal(A, 0)
            # Remove outlier
            self.normalizer.outlier = np.quantile(np.asarray(A), 0.999)
            np.clip(A, a_min=0, a_max=self.normalizer.outlier, out=A)
        else:
            np.fill_diagonal(A, 0)
            A = np.matrix(A)

        # M <- D^-1/2 * A * D^-1/2   # normalized adjacency natrix
        # np.save('/Users/jiang/Dropbox (Partners HealthCare)/Software/ATAC_Annotation_V1/ATAC_Annotation_Package/output/pbmc_10k_multiome_V2/decompos_A_first.npy', A)
        # print("shape of A: {}".format(A.shape))
        D = np.sqrt(A.sum(axis=1))
        np.divide(A, D, out=A)
        np.divide(A, D.T, out=A)
        # https://docs.scipy.org/doc/scipy/tutorial/arpack.html
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.eigsh.html
        print("Perform decomposition")
        evals, evecs = sp.sparse.linalg.eigsh(A, self.n_dim + 1, which='LM')
        # np.save('/Users/jiang/Dropbox (Partners HealthCare)/Software/ATAC_Annotation_V1/ATAC_Annotation_Package/output/pbmc_10k_multiome_V2/decompos_evals.npy', evals)
        # np.save('/Users/jiang/Dropbox (Partners HealthCare)/Software/ATAC_Annotation_V1/ATAC_Annotation_Package/output/pbmc_10k_multiome_V2/decompos_evecs.npy', evecs)
        #print("save decomposition results")

        ix = evals.argsort()[::-1]
        self.evals = np.real(evals[ix])
        self.evecs = np.real(evecs[:, ix])

        B = np.divide(self.evecs, D)
        np.divide(B, self.evals.reshape((1, -1)), out=B)
        # np.save('/Users/jiang/Dropbox (Partners HealthCare)/Software/ATAC_Annotation_V1/ATAC_Annotation_Package/output/pbmc_10k_multiome_V2/decompos_B.npy',B)
        # get decomposition eigenvectors

        self.B = B
        self.Q = []
        #np.save('data.npy', evecs)
        self.test = [] # to remove

        return self

    def extend(self, data):
        A = self.compute_similarity(self.sample, data)
        if (self.distance == "jaccard"):
            self.normalizer.normalize(
                A, self.coverage, data.sum(axis=1) / self.dim,
                clip_min=0, clip_max=self.normalizer.outlier
            )
        self.Q.append(A.T @ self.B)
        self.test.append(A) # to remove
                 


    def transform(self, orthogonalize = True):
        
        # np.save('/Users/jiang/Dropbox (Partners HealthCare)/Software/ATAC_Annotation_V1/ATAC_Annotation_Package/output/pbmc_10k_multiome_V2/extend_Q.npy', self.Q)
        # np.save('/Users/jiang/Dropbox (Partners HealthCare)/Software/ATAC_Annotation_V1/ATAC_Annotation_Package/output/pbmc_10k_multiome_V2/extend_evals.npy', self.evals)

        if len(self.Q) > 0:
            Q = np.concatenate(self.Q, axis=0)
            D_ = np.sqrt(np.multiply(Q, self.evals.reshape(1, -1)) @ Q.sum(axis=0).T)
            np.divide(Q, D_.reshape((-1, 1)), out=Q)
            # print("investigate transformation")
            # np.save('/Users/jiang/Dropbox (Partners HealthCare)/Software/ATAC_Annotation_V1/ATAC_Annotation_Package/output/pbmc_10k_multiome_V2/transform_Q_first.npy', Q) 
            # print("shape of Q: {}".format(Q.shape))

            if orthogonalize:
                # orthogonalization
                sigma, V = np.linalg.eig(Q.T @ Q)
                sigma = np.sqrt(sigma)
                B = np.multiply(V.T, self.evals.reshape((1,-1))) @ V
                np.multiply(B, sigma.reshape((-1, 1)), out=B)
                np.multiply(B, sigma.reshape((1, -1)), out=B)
                evals_new, evecs_new = np.linalg.eig(B)

                # reorder
                ix = evals_new.argsort()[::-1]
                self.evals = evals_new[ix]
                evecs_new = evecs_new[:, ix]

                np.divide(evecs_new, sigma.reshape((-1, 1)), out=evecs_new)
                self.evecs = Q @ V @ evecs_new
            else:
                self.evecs = Q
        return (self.evals[1:], self.evecs[:, 1:])

def jaccard_similarity(m1, m2=None):
    """
    Compute pair-wise jaccard index
    Parameters
    ----------
    mat1
        n1 x m
    mat2
        n2 x m
    
    Returns
    -------
        Jaccard similarity matrix
    """
    # print(m1.shape)
    # if m2 is not None: print(m2.shape)
    s1 = m1.sum(axis=1)
    if m2 is None:
        d = m1.dot(m1.T).todense()
        gc.collect() #A new object starts its life in the first generation of the garbage collector
        t = np.negative(d) # Numerical negative, element-wise.
        t += s1 
        t += s1.T
        d /= t
    else:
        s2 = m2.sum(axis=1)
        d = m1.dot(m2.T).todense()
        gc.collect()
        d /= -d + s1 + s2.T
    gc.collect()
    return d

class JaccardNormalizer:
    def __init__(self, jm, c):
        (slope, intersect) = jm_regress(jm, c)
        self.slope = slope
        self.intersect = intersect
        self.outlier = None
   # Pi = Ci/m and Pj=Cj/m be the probability of observing a signal in cell xiand xj where m is thelength of the vector.
    def normalize(self, jm, c1, c2, clip_min=None, clip_max=None):
        # jm / (self.slope / (1 / c1 + 1 / c2.T - 1) + self.intersect)
        temp = 1 / c1 + 1 / c2.T
        temp -= 1
        np.reciprocal(temp, out=temp)
        np.multiply(temp, self.slope, out=temp)
        temp += self.intersect
        jm /= temp
        if clip_min is not None or clip_max is not None:
            np.clip(jm, a_min=clip_min, a_max=clip_max, out=jm)
        gc.collect()
