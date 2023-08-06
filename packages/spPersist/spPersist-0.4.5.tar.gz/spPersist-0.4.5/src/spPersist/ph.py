from . import DTM_filtrations as dtm
from . import persistence_statistics as ps

import gudhi
import numpy as np
import matplotlib.pyplot as plt

def compute_Rips_complex(X,DTM=False,max_dimension=2,p=1,m=0.1,is_plot=False):
  '''
  compute_Rips_complex takes a point cloud X and DTM indicating whether DTM filtrations
  are used in the computation, and returns the computed simplicial complex of X. 
  If is_plot is true, it also plots its persistence diagram.

  The extra parameter max_dimension can be specified for Rips complex and DTM
  filtrations; and for the case of DTM filtrations, the additional parameters 
  p and m can be specified.
  '''

  # create a complex
  if DTM:
    st = dtm.DTMFiltration(X, m, p, max_dimension)
  else:
    st = gudhi.RipsComplex(points=X).create_simplex_tree(max_dimension)

  # compute the persistence
  diagram = st.persistence()                                       

  # plot the persistence diagram
  if is_plot:
    gudhi.plot_persistence_diagram(diagram)
    if DTM:
      title = 'Persistence diagram of the DTM-filtration with parameter p ='+str(p)
    else:
      title = 'Persistence diagram of the Rips complex'
    plt.title(title);

  return st


def compute_Alpha_complex(X,DTM=False,max_dimension=3,p=1,m=0.05,is_plot=False):
  '''
  compute_Alpha_complex takes a point cloud X and DTM indicating whether DTM filtrations
  are used in the computation, and returns the computed simplicial complex of X. 
  If is_plot is true, it also plots its persistence diagram.

  The extra parameter max_dimension, p and m can be specified for DTM filtrations.
  '''

  # create a complex
  if DTM:
    st = dtm.AlphaDTMFiltration(X, m, p, max_dimension)
  else:
    st = gudhi.AlphaComplex(points=X).create_simplex_tree()

  # compute the persistence
  diagram = st.persistence()                                       

  # plot the persistence diagram
  if is_plot:
    gudhi.plot_persistence_diagram(diagram)
    if DTM:
      title = 'Persistence diagram of the Alpha-DTM-filtration with parameter p ='+str(p)
    else:
      title = 'Persistence diagram of the Alpha complex'
    plt.title(title);

  return st


def bottleneck_distance(st1, st2, dim):
  '''
  bottleneck_distance takes SimplexTree st1 and st2 and computes
  the bottleneck distance of their persistence diagram in dimension dim.
  '''
  
  diag1 = st1.persistence_intervals_in_dimension(dim)
  diag2 = st2.persistence_intervals_in_dimension(dim)

  distance = gudhi.bottleneck_distance(diag1, diag2)

  message = "Bottleneck distance approximation = " + '%.2f' % gudhi.bottleneck_distance(diag1, diag2, 0.1)
  print(message)

  message = "Bottleneck distance value = " + '%.2f' % distance
  print(message)

  return distance


def plot_confidence_region(X, ptype: str, level=0.90):
  '''
  confidence_region takes a point cloud X and ptype
  indicating either a Rips complex or a Square-root
  Alpha complex used for computing the persistence,
  and plot the persistence diagram of X with confidence 
  region as red band. 

  The topological features in the region is considered
  'topological noise' and the features above the red 
  band is considered 'topological signal'.

  The desired confidence level can be specified using
  the parameter level.
  '''

  hatc = ps.hausd_interval(data=X, level=level)
  if ptype == 'Rips':
    st = compute_Rips_complex(X)
    diagram = st.persistence()
  elif ptype == 'Alpha':
    st = compute_Alpha_complex(X)
    st_list = st.get_filtration()
    for splx in st_list:
      st.assign_filtration(splx[0],filtration= np.sqrt(splx[1])) 
    diagram = st.persistence()
  else:
    raise ValueError('ptype is not either Rips or Alpha.')
  
  gudhi.plot_persistence_diagram(diagram,band=2*hatc);


def connected_components(st):
  '''
  connected_components takes a SimplexTree st and
  return the number of connected components of st.
  '''

  return st.betti_numbers()[0]


def one_dimensional_holes(st):
  '''
  one_dimensional_holes takes a SimplexTree st and
  return the number of one dimensional holes of st.
  '''

  return st.betti_numbers()[1]


def two_dimensional_holes(st):
  '''
  one_dimensional_holes takes a SimplexTree st and
  return the number of one dimensional holes of st.
  '''

  return st.betti_numbers()[2]


def holes(st, dim: int):
  '''
  holes takes a SimplexTree st and return 
  the number of holes of st in dimension dim.
  '''

  return st.betti_numbers()[dim]