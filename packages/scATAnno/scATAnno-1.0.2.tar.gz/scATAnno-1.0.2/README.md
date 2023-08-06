# scATAnno

### An Automated Cell Type Annotation for Single-cell ATAC Sequencing Data
<img src='https://github.com/aj088/scATAnno-main/blob/main/doc/_static/img/2.workflow_details-MainFigure1.png'>

For more detailed information, please refer to the [document](https://scatanno-main.readthedocs.io/en/latest/).

# Installation
Install scATAnno through github:

    $ git clone https://github.com/aj088/scATAnno-main.git
    $ cd scATAnno-main
    $ pip install .


# Usage
scATAnno has two important parts of functions. The first part is the integration function __`scATAnno_integrate()`__; the second part if cell type assignment functions __`scATAnno_KNN_assign()`__, __`scATAnno_distance_assign()`__, __`scATAnno_cluster_assign()`__, which can be applied sequentially to automatically annotation cells, as shown in the example below:

```
# reference and query are two AnnData matrices 
# Integration step

integrated_adata = scATAnno_integrate(reference, query, reference_label_col="celltypes")
reference = integrated_adata[integrated_adata.obs["dataset"] == "Atlas"]
query = integrated_adata[integrated_adata.obs["dataset"] != "Atlas"]

# Celltype assignment step
# Perform KNN assignment
query_KNN = scATAnno_KNN_assign(reference, query, reference_label_col="celltypes")

# Perform weighted-distance based assignment
query_distance = scATAnno_distance_assign(reference, query_KNN, reference_label_col="celltypes", distance_threshold=95, atlas="PBMC", uncertainty_threshold=0.5)

# Perform cluster-level assignment
query_annotated = scATAnno_cluster_assign(query_distance)

```

# Cite
Yijia Jiang, Zhirui Hu, Junchen Jiang, Alexander Zhu, Yi Zhang, Allen Lynch, Yingtian Xie, Rong Li, Ningxuan Zhou, Cliff A. Meyer, Palome Cejas, Myles Brown, Henry W. Long, Xintao Qiu. scATAnno: Automated Cell Type Annotation for single-cell ATAC sequencing Data. bioRxiv 2023.06.01.543296.


