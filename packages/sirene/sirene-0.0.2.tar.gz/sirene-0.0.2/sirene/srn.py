import pandas as pd

from importlib import resources
import io

def read(sector='agropecuaria',gas='CO2'):
  #File Path
  file_path = '/content/drive/MyDrive/projetos/Bacen/variaveis_ambientais/dicionario/dados_GHG_MCTI/sexta_edicao/estim_6a_ed_1990-2020_'
  #number of subsector
  if sector == "agropecuaria":
    n = 78
  elif sector == "energia":
    n = 32
  elif sector == "ippu":
    n = 28
  elif sector == "lulucf":
    n = 8
  elif sector == "residuos":
    n = 10
  elif sector == "total-brasil-1":
    n = 7
  else:
    n = None

  #select sheet
  #'CO2e_GWP_SAR'
  #'CO2e_GWP_AR5'
  #'CO2e_GTP_AR5'
  #'CO2'
  #'CH4'
  #'N2O'
  with resources.open_binary('sirene.MCTI.sexta_edicao', 'estim_6a_ed_1990-2020_'+sector+'.xlsx') as f:
    data = f.read()
    bytes_io = io.BytesIO(data)
  df = pd.read_excel(bytes_io, sheet_name=gas)
  df = df.loc[4:4+n,:]
  #set columns names
  new_columns = df.iloc[0]
  df = df[1:]
  df.columns = new_columns
  df.set_index(df.columns[0], inplace=True)
  df.rename_axis("NFR_code", inplace=True)
  return df


