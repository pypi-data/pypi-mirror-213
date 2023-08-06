from . import ph

def homological_classification(st):
  '''
  homological_classification takes a SimplexTree st,
  and return a dictionary of homologies of st where
  the keys indicate connected components or n-dimensional
  holes and the values indicate the number of connected
  components or the number of holes of a given dimension.
  '''

  hc = {}
  bn = st.betti_numbers()
  for i in range(len(bn)):
    if i == 0:
      hc['connected components'] = bn[i]
    else:
      hc[str(i)+'-dimensional holes'] = bn[i]

  return hc