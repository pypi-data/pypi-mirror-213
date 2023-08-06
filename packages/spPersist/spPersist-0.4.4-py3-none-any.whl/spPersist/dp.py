import os, shutil, requests
import tarfile, zipfile
from zipfile import ZipFile

import scanpy as sc
import pandas as pd
import anndata



def Visium_FFPE_Mouse_Brain():
  '''
  Returns annotated data object of the Adult Mouse Brain (FFPE) dataset from 
  Visium, 10x Genomics.
  '''

  gex = 'Visium_FFPE_Mouse_Brain_filtered_feature_bc_matrix.h5'
  url_gex = 'https://cf.10xgenomics.com/samples/spatial-exp/1.3.0/Visium_FFPE_Mouse_Brain/Visium_FFPE_Mouse_Brain_filtered_feature_bc_matrix.h5'
  url_pos = 'https://cf.10xgenomics.com/samples/spatial-exp/1.3.0/Visium_FFPE_Mouse_Brain/Visium_FFPE_Mouse_Brain_spatial.tar.gz'
  open(gex, 'wb').write(requests.get(url_gex).content)
  open('spatial.tar','wb').write(requests.get(url_pos).content)

  tar = tarfile.open('spatial.tar')
  posfile = tar.getmembers()[1] # 1 is the index of the coordinate file.
  tar.extract(posfile)
  return visium(gex, posfile.name)


def V1_Adult_Mouse_Brain():
  '''
  Returns annotated data object of the Mouse Brain Section (Coronal) dataset
  from Visium, 10x Genomics.
  '''

  gex = 'V1_Adult_Mouse_Brain_filtered_feature_bc_matrix.h5'
  url_gex = 'https://cf.10xgenomics.com/samples/spatial-exp/1.0.0/V1_Adult_Mouse_Brain/V1_Adult_Mouse_Brain_filtered_feature_bc_matrix.h5'
  url_pos = 'https://cf.10xgenomics.com/samples/spatial-exp/1.0.0/V1_Adult_Mouse_Brain/V1_Adult_Mouse_Brain_spatial.tar.gz'
  open(gex, 'wb').write(requests.get(url_gex).content)
  open('spatial.tar','wb').write(requests.get(url_pos).content)

  tar = tarfile.open('spatial.tar')
  posfile = tar.getmembers()[3] # 3 is the index of the coordinate file.
  tar.extract(posfile)
  return visium(gex, posfile.name)


def Vizgen_V1_S2R1():
  '''
  Returns annotated data object of Slice 2 Replicate 1
  of the MERFISH Mouse Brain Receptor Map datasets from
  Vizgen.
  '''
  return Vizgen_V1(2,1)


def Vizgen_V1_S1R3():
  '''
  Returns annotated data object of Slice 1 Replicate 3
  of the MERFISH Mouse Brain Receptor Map datasets from
  Vizgen.
  '''
  return Vizgen_V1(1,3)


def Vizgen_V1(slice_num: int, replicate_num: int):
  '''
  Returns annotated data object of the dataset of 
  slice number slice_num and replicate number replicate_num  
  of the MERFISH Mouse Brain Receptor Map datasets from Vizgen.
  '''

  if slice_num > 3 or replicate_num >3:
    raise ValueError('Slice '+str(slice_num)+' Replicate '+str(replicate_num)+' does not exist.')

  from google.colab import auth 
  auth.authenticate_user()

  # Paths to Data
  base_path = 'gs://public-datasets-vizgen-merfish/datasets/mouse_brain_map/BrainReceptorShowcase/'

  dataset_name = 'Slice' + str(slice_num) + '/Replicate' + str(replicate_num) + '/'
  dataset_suffix = '_S' + str(slice_num) + 'R' + str(replicate_num)

  ad = merfish(base_path + dataset_name + 'cell_by_gene' + dataset_suffix + '.csv',
             base_path + dataset_name + 'cell_metadata' + dataset_suffix + '.csv')
  return ad


def visium(gex: str, pos: str):
  '''
  visium takes cell by gene count file name gex and tissue position lists pos, 
  and return an annotated data object with spatial coordinates in obsm.
  Note that gex and pos should be formatted as Spance Ranger outputs.
  '''
  ad = sc.read_10x_h5(gex)
  coords = pd.read_csv(pos,index_col=0)
  coords.columns = ["in_tissue", "array_row", "array_col", "pxl_col_in_fullres", "pxl_row_in_fullres"]
  ad.obs = pd.merge(ad.obs, coords, how="left", left_index=True, right_index=True)
  ad.obsm['spatial'] = ad.obs[["pxl_row_in_fullres", "pxl_col_in_fullres"]].values
  ad.obs.drop(columns=["pxl_row_in_fullres", "pxl_col_in_fullres"], inplace=True)
  return ad

def merfish(gex: str, pos: str):
  '''
  merfish takes cell by gene count file name gex and
  metadata file pos that contains spatial coordinates, 
  and return an annotated data object with spatial coordinates in obsm.
  Note that gex and pos should be formatted as Vizgen outputs.
  '''
  adata = anndata.AnnData(pd.read_csv(gex, header=0, index_col=0))
  

  coords = pd.read_csv(pos, header=0, index_col=0)
  coords.columns = ["fov", "volume", "center_x", "center_y", "min_x", "max_x", "min_y", "max_y"]

  adata.obs = pd.merge(adata.obs, coords, how="left", left_index=True, right_index=True)
  adata.obsm['spatial'] = adata.obs[["center_x", "center_y"]].values
  adata.obs.drop(columns=["center_x", "center_y"], inplace=True)
  return adata


def id_to_url(id_num: str):
  '''
  id_to_url takes a GEO accession or Zenodo doi id_num
  and returns the url path of the repository.
  '''

  if 'GSE' in id_num:
    path = 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE'+id_num[3:6]+'nnn/'+id_num+'/suppl/'
  elif 'zenodo' in id_num:
    record_id = id_num.split('.')[-1]
    r = requests.get(f"https://zenodo.org/api/records/{record_id}") 
    urls = [f['links']['self'] for f in r.json()['files']]
    path = os.path.commonprefix(urls)
    if os.path.isfile(path):
      path = os.path.dirname(path)
  else:
    raise ValueError(id_num + ' is neither GEO accession or Zenodo doi.')

  return path


def zenodo_to_h5(doi: str, filename: str, ttype: str):
  '''
  zenodo_to_h5 takes a zenodo doi number doi that 
  contains a tar or zip file named filename and ttype specifying
  if the technology type is Visium or MERFISH, and
  exports a zip file of annotated objects from 
  the Visium or MERFISH samples in the dataset as h5 files.
  '''

  path = id_to_url(doi)
  url_to_h5(path,filename=filename,ttype=ttype)


def accession_to_h5(gse: str, filename: str, ttype: str):
  '''
  accession_to_h5 takes a GEO accession number gse that 
  contains a tar or zip file named filename and ttype specifying
  if the technology type is Visium or MERFISH, and
  exports a zip file of annotated objects from 
  the Visium or MERFISH samples in the dataset as h5 files.
  '''

  path = id_to_url(gse)
  url_to_h5(path, filename=filename, ttype=ttype)


def url_to_h5(path: str, filename: str, ttype: str):
  '''
  url_to_h5 takes a url path that contains a 
  tar or zip file named filename and ttype specifying
  if the technology type is Visium or MERFISH, and
  exports a zip file of annotated objects from 
  the Visium or MERFISH samples in the dataset as h5 files.

  Note that the files in filename should contain samples of 
  gene expression counts and the corresponding spatial coordinates
  and the sample id should be prefix of these files separated by the
  underscore character.
  '''

  url = os.path.join(path,filename)
  if filename not in os.listdir():
    open(filename, 'wb').write(requests.get(url).content)

  if tarfile.is_tarfile(filename):
    repository = tarfile.open(filename) 
    filenames = repository.getnames()
  elif zipfile.is_tarfile(filename):
    repository = ZipFile(filename)
    filenames = repository.namelist()
  else:
    raise ValueError('filename is not tar or zip file.')

  if ttype == 'Visium':
    samplelist = list(filter(lambda s: s.endswith('.h5'), filenames))
  elif ttype == 'MERFISH':
    samplelist = list(filter(lambda s: 'cell_by_gene' in s, filenames))
  else:
    raise ValueError('ttype is not either Visium or MERFISH.')

  sampleids = [s.split('_')[0] for s in samplelist]
  
  # helper function for extracting a sample
  def extractsample(members, sampleid):
    for member in members:
      if member.isfile():
        fname = member.name
      else:
        fname = member

      if sampleid in fname:
        yield member

  # helper function for emptying a given directory
  def emptydir(folder):
    for filename in os.listdir(folder):
      file_path = os.path.join(folder, filename)
      try:
          if os.path.isfile(file_path) or os.path.islink(file_path):
              os.unlink(file_path)
          elif os.path.isdir(file_path):
              shutil.rmtree(file_path)
      except Exception as e:
          print('Failed to delete %s. Reason: %s' % (file_path, e))


  data_path = './data/'
  h5_path = './h5/'

  if not os.path.exists(data_path):
    os.mkdir(data_path)
  if not os.path.exists(h5_path):
    os.mkdir(h5_path)

  emptydir(h5_path)

  for sampleid in sampleids:
    emptydir(data_path)
    
    # extract files for a given sample id to the data foler
    repository.extractall(path=data_path,
                   members=extractsample(repository, sampleid))

    for filename in os.listdir(data_path):
      if ttype == 'Visium':
        if 'filtered' in filename:
          gex = data_path + filename
        if 'positions' in filename:
          pos = data_path + filename
      elif ttype == 'MERFISH':
        if 'cell_by_gene' in filename:
          gex = data_path + filename
        if 'cell_metadata' in filename:
          pos = data_path + filename
      else:
        raise ValueError('ttype is not either Visium or MERFISH.')
    
    if gex is None or pos is None:
      raise NameError('The repository does not contain Visium or Vizgen formatted files.')
    
    if 'filtered' in gex:
      adata = visium(gex, pos)
    else:
      adata = merfish(gex, pos)

    savefilename = sampleid + '.h5'
    adata.write_h5ad(h5_path+savefilename)
  
  # zip h5 files
  shutil.make_archive('h5', 'zip', h5_path)