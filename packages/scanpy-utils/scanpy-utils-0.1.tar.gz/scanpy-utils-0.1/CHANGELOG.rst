
Changelog
=========

0.1 (2021-06-24) Initial release
--------------------------------

* ``get_markers`` function to extract markers from adata and add ``pct.1``, ``pct.2`` fields
* ``write_mtx`` function to dump adata in cellranger mtx format
* ``clean_metadata`` function to merge and remove duplicates from ``adata.var`` after merging

Plotting:

* ``feature_plot`` function to plot hexbin feature plot on UMAP
* ``plot_composition`` function to plot composition of clusters based on other metadata
* ``expr_colormap`` function with custom colormap for expression
