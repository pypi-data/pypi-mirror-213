# Spatial transcriptomics with Persistent Homology

This is a package for classifying Spatial transcriptomics data according to its 
spatial topology. The specific mathematical foundation for the classification is
the theory of Persistent Homology and persistence diagram. The package 
contains a data processing module, called dp, allowing users to load either the
standard datasets from Visium and MERFISH, or published datasets into desired
annotated data format for the analysis performed in this package. The format is
compatible with the package Squidpy.

The package also includes a pre-processing module, a 
persistent homology module and a homological classification module, respectively
named pp, ph and hc.

The pre-processing module contains quality control metrics, deconvolution
methods and cell type identifications.

The persistent homology module contains functions for computing simplicial 
complexes of point clouds (See data structures in the gudhi package.) and their
topological measures. It also includes plotting features of the persistence 
diagram.

The homological classification module computes the number of holes and connected
components as a dictionary.