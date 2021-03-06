# questo file serve per generare varie mappe da usare nella presentazione
# permette di avere una idea di come si distribuiscono i consumi sul territorio 

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

import numpy as np
from datetime import time, timedelta, datetime, date 
import contextily as cx
import matplotlib.pyplot as plt
import matplotlib as mpl 
from trentodatalib import meteo, consumi, inquinamento
from trentodatalib import funzioni as fz
from trentodatalib import rawdatabase as rawdata


grid = rawdata.gridraw

# plotto una mappa attraverso la funzione genera_mappa_consumi che sta nella libreria funzioni
#La mappa rappresenta i consumi lordi di tutto il mese ed evidenzia le zone a più alto consumo nella zona di trento
def plot_mappa_consumi_lordi():
	gdf_consumi_lordi = fz.genera_mappa_consumi(rawdata.df_consumiraw, rawdata.df_lineeraw, grid) 
	MAX = gdf_consumi_lordi['consumo_per_cella'].max()
	MIN = gdf_consumi_lordi['consumo_per_cella'].min()
	norm= plt.Normalize( MIN, MAX )
	fig, ax_consumi_lordi = plt.subplots(1, 2, figsize=(14,7))
	for ii in range(2):
		gdf_consumi_lordi.plot('consumo_per_cella', cmap='YlOrRd', alpha=0.5, ax = ax_consumi_lordi[ii] ) 
		cx.add_basemap(ax_consumi_lordi[ii], crs=grid.crs.to_string() )
		plt.colorbar(plt.cm.ScalarMappable( norm=ax_consumi_lordi[ii]._children[0].norm , cmap='YlOrRd'), ax= ax_consumi_lordi[ii])
		#plt.colorbar(plt.cm.ScalarMappable( norm=ax_consumi_lordi[ii].norm , cmap='YlOrRd'), ax=ax_consumi_lordi )
	#zoom sull'area di trento
	ax_consumi_lordi[1].set_xlim(11.05, 11.20)
	ax_consumi_lordi[1].set_ylim(46.0, 46.15)
	plt.show()
	return
	#plt.savefig("mappaConsumi1.pdf", bbox_inches='tight' , dpi=300)

# Variazioni di consumo fra 
# giorno e la notte e se quest'ultime correlano con le zone industriali del trentino

def plot_mappa_diff_giorno_notte():

	df_mappa_giorno = fz.genera_mappa_consumi( consumi.df_consumidiurni, consumi.df_linee , grid )
	df_mappa_notte = fz.genera_mappa_consumi( consumi.df_consuminotturni, consumi.df_linee, grid )
	#normalizzo i consumi per numero di ore nella fascia oraria giorno/notte
	df_mappa_giorno['consumo_per_cella']/=11
	df_mappa_notte['consumo_per_cella']/=13
	df_mappa_diff = df_mappa_giorno.copy()
	df_mappa_diff['consumo_per_cella'] = +df_mappa_giorno['consumo_per_cella'] - df_mappa_notte['consumo_per_cella']

	fig, axes = plt.subplots(1,1, figsize=(12,5) ) 
	MAX = np.max(np.abs(df_mappa_diff['consumo_per_cella'] )  ) 
	norm= plt.Normalize( -MAX, MAX ) 
	#bwr: blue white red (in ordine crescente)
	df_mappa_diff.plot('consumo_per_cella', cmap='bwr', alpha=0.5, ax = axes, norm=norm) 
	cx.add_basemap(axes, crs=grid.crs.to_string() )
	axes.set_xlim(10.8, 11.5) 
	axes.set_ylim(45.84, 46.2)
	#plt.colorbar(plt.cm.ScalarMappable( norm=ax_consumi_lordi._children[0].norm , cmap='bwr'), ax=axes[0] )
	plt.colorbar(plt.cm.ScalarMappable( norm=axes._children[0].norm , cmap='bwr'), ax=axes )
	plt.show()
	return

def plot_mappa_diff_wknd():
	# faccio una mappa per vedere la differenza fra i consumi dei giorni infrasettimanali e i week-end

	df_mappa_settimana = fz.genera_mappa_consumi( consumi.df_consumisettimana, consumi.df_linee , grid)
	df_mappa_weekend = fz.genera_mappa_consumi( consumi.df_consumiweekend, consumi.df_linee, grid)
	#normalizzo
	Nset = len(consumi.df_consumisettimana.index)
	Ntot = len(consumi.df_consumi.index)
	df_mappa_settimana['consumo_per_cella']/=Nset*144
	df_mappa_weekend['consumo_per_cella']/=(Ntot-Nset)*144
	# ci sono 144 righe ogni giorno (ogni riga è un quarto d'ora)
	df_mappa_diff2 = df_mappa_settimana.copy()
	df_mappa_diff2['consumo_per_cella'] = df_mappa_settimana['consumo_per_cella']-df_mappa_weekend['consumo_per_cella']
	MAX = np.max(np.abs(df_mappa_diff2['consumo_per_cella'] )  ) 
	norm= plt.Normalize( -MAX, MAX )
	axs_diff2 = df_mappa_diff2.plot('consumo_per_cella', cmap='bwr', alpha=0.5, norm=norm,figsize=(12,5)) 
	cx.add_basemap(axs_diff2, crs=grid.crs.to_string() )

	plt.colorbar(plt.cm.ScalarMappable( norm=axs_diff2._children[0].norm , cmap='bwr'), ax=axs_diff2 )
	axs_diff2.set_xlim(10.8, 11.5) 
	axs_diff2.set_ylim(45.84, 46.2)
	return
#plt.savefig("mappasettimanaweekend.pdf", bbox_inches='tight' , dpi=300)
#plt.show()



def plot_mappa_stazioni():
	
	fig, axmappastazioni = plt.subplots(1, 2, figsize=(14,7))

	for ii in range(2):
		meteo.df_mappa_stazioni.plot(color='blue', ax=axmappastazioni[ii]) 
		cx.add_basemap(axmappastazioni[ii], crs=meteo.df_mappa_stazioni.crs.to_string() ) 
	#grid.plot(ax=axmappastazioni, color='aliceblue', alpha=0.4) 


	axmappastazioni[1].set_xlim(11.0, 11.3)
	axmappastazioni[1].set_ylim(45.9, 46.2)
	axmappastazioni[1].annotate('Trento Laste', (11.13565, 46.08), fontsize=12)
	axmappastazioni[1].annotate('Roncafort', (11.10131, 46.10), fontsize=12)
	plt.show()
	return



def plot_suddivisione_regioni(luogo='provincia'):

	#alpha, trasparenza dei plot
	aph = 0.2
	if luogo not in ['provincia', 'comune']:
		print("Inserire 'regione' o 'comune' come argomento alla funzione.")


	df_staz=meteo.df_mappa_stazioni
	df_reg = meteo.gdfLineCells
	df_staz.to_crs(epsg=4326, inplace=True)
	df_reg.to_crs(epsg=4326, inplace=True)
	#mappo le stazioni in diversi colori secondo una colormap di matplotlib
	stazioni = pd.unique(df_reg['nearestStation'])
	cmap = mpl.cm.get_cmap('hsv', len(stazioni))

	colori = list(cmap(np.arange(0, cmap.N)))
	colorihex = [mpl.colors.to_hex(colori[ii]) for ii in range(len(colori))]
	np.random.shuffle(colorihex)
	dict_colori_stazioni = dict(zip(stazioni, colorihex))
	df_reg['colore'] = df_reg['nearestStation'].replace(dict_colori_stazioni)
	
	
	if luogo == 'provincia':
		ax1 = df_reg.plot(color=df_reg['colore'], alpha=aph, figsize = (14, 7))
		df_staz.plot(ax=ax1, color='blue')


	#per plot del comune voglio solo le due stazioni di cui abbiamo tenuto i dati
	if luogo=='comune':
		df1 = df_reg[df_reg['nearestStation']=='T0129']
		df2 = df_reg[df_reg['nearestStation']=='T0135']
		df1['colore'] =  '#ff0000' #rosso in hex
		df2['colore'] = '#0000ff' #blu in hex

		dftoplot = pd.concat([df1, df2])
		ax1 = dftoplot.plot(color=dftoplot['colore'], alpha=aph, figsize = (14,7))
		df_staz[(df_staz['station']=='T0129') | (df_staz['station']=='T0135')].plot(ax=ax1, color='blue')
		ax1.set_xlim(11.0, 11.3)
		ax1.set_ylim(45.9, 46.2)
		ax1.annotate('Trento Laste', (11.056, 46.06), fontsize=12)
		ax1.annotate('Roncafort', (11.085, 46.101), fontsize=12)
		comuneTN = rawdata.gdf_comuniTN[rawdata.gdf_comuniTN['COMUNE']=='Trento'].to_crs(epsg=4326)
		comuneTN.plot(ax=ax1, edgecolor='black', facecolor='none', label='comune di Trento')
		#print(comuneTN.head())

	cx.add_basemap(ax1, crs=df_reg.crs.to_string() ) 
	plt.show()
	
	return

