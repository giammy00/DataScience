# in questo file voglio di fatto generare i database in pandas, partendo dai file forniti 
# in maniera da avere dei database originali che non vengono modificati 
# in più lascio di seguito tutti gli import fatti nel corso del progetto per coodità personale 
import pandas as pd
import geopandas as gpd
from datetime import time, timedelta, datetime, date 
import contextily as cx
import numpy as np
import json
import numpy as np
from pathlib  import Path
import matplotlib.pyplot as plt
import matplotlib as mpl
from shapely.geometry import Polygon, Point
from fiona.crs import from_epsg
import fiona
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression

# metto gli import che servono per questo file: 
from trentodatalib import funzioni as fz
from pathlib import Path
from trentodatalib import trentopaths as tpath
import pandas as pd
import json
from shapely.geometry import Point

# estraggo il database riguardante i consumi e il database riguardante le linee 
current_path = Path(__file__).parent.resolve()
df_lineeraw =  pd.read_csv(current_path / tpath.raw_data_path / tpath.filenames['SET-lines'])
nomi = ['LINESET', 'time', 'consumi']
df_nov   =  pd.read_csv(current_path / tpath.raw_data_path / tpath.filenames['NOV-DATA' ], names = nomi)
df_dec   =  pd.read_csv(current_path / tpath.raw_data_path / tpath.filenames['DEC-DATA' ], names = nomi)
#unisco dati 
df_consumiraw = pd.concat([df_nov, df_dec])
#converto colonna time nel formato di pandas
##df_consumiraw['time'] = pd.to_datetime(df_consumiraw['time'], format='%Y-%m-%d %H:%M')
##df_consumiraw.rename(columns={'time':'datetime'}, inplace=True) 



# estraggo il database riguardante l'inquinamento 
current_path = Path(__file__).parent.resolve()
with open(current_path/ tpath.raw_data_path / tpath.filenames['meteo'] ) as file:
    dati_meteo_json = json.load(file)

meteo_rawdata = pd.DataFrame(dati_meteo_json['features'])
#convertiamo la colonna geometry nel formato di shapely
meteo_rawdata['geomPoint.geom'] = meteo_rawdata['geomPoint.geom'].apply(lambda x:Point(x['coordinates']) )
meteo_rawdata.rename(columns={'geomPoint.geom':'geometry'} , inplace=True) 
meteo_rawdata = meteo_rawdata.melt( id_vars=meteo_rawdata.columns.values[:10]) 
#aggiusto la colonna degli orari
meteo_rawdata[['variable', 'rawtime']] = meteo_rawdata['variable'].str.split('.', expand=True) 
meteo_rawdata['datetime'] = pd.to_datetime( meteo_rawdata['date']+meteo_rawdata['rawtime'], format='%Y-%m-%d%H%M' ) 
#e butto quelle vecchie
meteo_rawdata.drop(columns=['rawtime','date'], inplace=True)


#Estraggo i dati inquinamento 
df_inquinamentoraw= pd.read_csv(current_path/ tpath.ext_data_path / tpath.filenames['inquinamento'] , encoding='latin-1')

# Estraggo anche la griglia 
with open(current_path / tpath.raw_data_path / tpath.filenames['grid']) as f:
	grid_json=json.load(f)

gridraw = gpd.GeoDataFrame(grid_json['features'])

#converto la colonna geometry nel formato Polygon di shapely
gridraw['geometry'] = gridraw['geometry'].apply(lambda x:Polygon(x['coordinates'][0]))

#### Questa parte imposta il crs del geoDataFrame ######
# Import specific function 'from_epsg' from fiona module

# Set the GeoDataFrame's coordinate system to WGS84
gridraw.crs = from_epsg(code = 4326)

gridraw['id'] = gridraw['properties'].apply(lambda x: x['cellId'])
gridraw.drop(columns=['type', 'properties'], inplace=True) 



# Estraggo i dati dei comuni, questi serviranno solo per un eventuale plot 
'''
dati_comuni = gpd.read_file(current_path/ tpath.ext_data_path / files['comuni'] )
dati_province = gpd.read_file(current_path/ tpath.ext_data_path / files['province'] )

gdf_comuniTNraw = dati_comuni[ dati_comuni['COD_PROV'] == 22 ].reset_index(drop=True)
gdf_comuniTNraw.crs
'''