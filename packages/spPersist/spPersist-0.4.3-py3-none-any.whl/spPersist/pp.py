import cell2location
import scanpy as sc

def quality_control_metrics(adata):
  '''
  quality_control_metrics takes an annotated data object adata
  produced in the data processing module and performs 
  quality control calculation as recommended in Scanpy
  preprocessing tutorials.
  '''

  sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True)


def quality_control(adata):
  '''
  quality_control takes an annotated data object adata,
  prompts the user to enter quality control parameters,
  and filters the expression matrix.
  '''

  print('Filtering cells...\nPress Enter to skip the parameter.')
  params = ['min_counts', 'min_genes', 'max_counts','max_genes']
  ps = []
  for s in params:
    p = input('Enter '+ s + ':')
    print(s + ': ' + p)
    try:
      int(p)
    except:
      p = None
    else:
      p = int(p)
    ps.append(p)

  sc.pp.filter_cells(adata, min_counts=ps[0], inplace=True)
  sc.pp.filter_cells(adata, min_genes=ps[1], inplace=True)
  sc.pp.filter_cells(adata, max_counts=ps[2], inplace=True)
  sc.pp.filter_cells(adata, max_genes=ps[3], inplace=True)

  print('Filtering genes...\nPress Enter to skip the parameter.')
  params = ['min_counts', 'min_cells', 'max_counts','max_cells']
  ps = []
  for s in params:
    p = input('Enter '+ s + ':')
    print(s + ': ' + p)
    try:
      int(p)
    except:
      p = None
    else:
      p = int(p)
    ps.append(p)

  sc.pp.filter_genes(adata, min_counts=ps[0], inplace=True)
  sc.pp.filter_genes(adata, min_cells=ps[1], inplace=True)
  sc.pp.filter_genes(adata, max_counts=ps[2], inplace=True)
  sc.pp.filter_genes(adata, max_cells=ps[3], inplace=True)


def deconvolute(ad, ref):
  '''
  deconvolute takes an annotated data object ad produced
  in the data processing module and a single-cell reference 
  data ref as a pandas dataframe, and performs deconvolution 
  methods as demonstrated in the cell2location tutorial with 
  human lymph node. It returns the spatially resolved 
  annotated data.
  '''

  adata = ad.copy()

  # create and train the model
  mod = cell2location.models.Cell2location(
      adata, cell_state_df=ref, 
      # the expected average cell abundance: tissue-dependent 
      # hyper-prior which can be estimated from paired histology:
      N_cells_per_location=30,
      # hyperparameter controlling normalisation of
      # within-experiment variation in RNA detection:
      detection_alpha=20
  ) 
  mod.view_anndata_setup()

  mod.train(max_epochs=30000, 
            # train using full data (batch_size=None)
            batch_size=None, 
            # use all data points in training because 
            # we need to estimate cell abundance at all locations
            train_size=1,
            use_gpu=True,
          )

  # In this section, we export the estimated cell abundance (summary of the posterior distribution).
  adata = mod.export_posterior(
      adata, sample_kwargs={'num_samples': 1000, 'batch_size': mod.adata.n_obs, 'use_gpu': True}
  )

  return adata

