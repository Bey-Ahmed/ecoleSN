# -*- coding: utf-8 -*-

"""
	Représentation des résultats du bac de 2012 à 2016
	pour chaque région du Sénégal 
	(par rapport à tout le pays)

	---> Beylerbey

"""

import geopandas as gpd
import imageio
import matplotlib.pyplot as plt
import pandas as pd
import sys
from getfile import getFile


"""
	Récupération du fichier contenant les coordonnées 
	pour le dessin de la carte du Sénégal qui sont
	ensuite placées dans un tableau
"""
if getFile('..', 'SNregions.json') == 1 :
	sys.exit()
senegal = gpd.read_file(getFile('..', 'SNregions.json'))


"""
	Régions du Sénégal
"""
regionsSN = ('DAKAR', 'DIOURBEL', 'FATICK', 'KAFFRINE', 'KAOLACK', 'KEDOUGOU', 'KOLDA', 'LOUGA', 'MATAM', 'SAINT LOUIS', 'SEDHIOU', 'TAMBACOUNDA', 'THIES', 'ZIGUINCHOR')


"""
	Nombres de bacheliers entre 2012 et 2016
"""
if getFile('.', 'BAC_results_per_year.csv') == 1 :
		exit()
total_admis = pd.read_csv(getFile('.', 'BAC_results_per_year.csv'), index_col=0)


# Fixation de la taille de l'espace du rendu
plt.rcParams['figure.figsize'] = (20, 10)


"""
	Ajout du % de réussite par région de 2012 à 2016
"""
images = []
for year in range(2012, 2017, 1) :
	# Récupération des résultats pour une année (year)
	fileName = 'BAC_results_'+str(year)+'.csv'
	if getFile('..', fileName) == 1 :
		exit()
	data = pd.read_csv(getFile('..', fileName), index_col=0)

	# Calcul du % de réussite de chaque région par rapport au pays
	admis = [0]
	for i in range(len(data.index)) :
		admis.append(data.loc[regionsSN[i]][0] * 100 / total_admis.loc[year][0])
	admis.append(50)

	# Ajout des résultats, à la région correspondante, au dictionnaire "senegal"
	senegal['Bacheliers (%)'] = tuple(admis)

	# Dessin de la carte en fonction des % de réussite
	mapSN = senegal.plot(column='Bacheliers (%)', scheme='Equal_Interval', k=7, cmap='YlGn', edgecolor='grey', legend=True)
	mapSN.set_title('% de réussite au bac au Sénégal par région ('+str(year)+')')
	leg = mapSN.get_legend()
	leg.set_title('% des bacheliers')
	mapSN.set_axis_off()

	## Placement des noms des régions sur la carte
	if getFile('..', 'regionsName.json') == 1 :
		sys.exit()
	regionsName = gpd.read_file(getFile('..', 'regionsName.json'))
	for idx, row in regionsName.iterrows() :
		coordinates = row['geometry'].coords.xy
		x, y = coordinates[0][0], coordinates[1][0]
		mapSN.annotate(row['name'], xy=(x, y), xytext=(x, y), family='serif', fontweight='bold', horizontalalignment='center')
	
	## Sauvegarde dans les fichiers .png respectifs
	fileName = 'BAC_results_'+str(year)+'.png'
	plt.savefig(fileName, bbox_inches='tight')
	images.append(imageio.imread(fileName))

# Génération du gif à partir des images stockées dans la variable images
kargs = {'duration' : 1} # Duréee de défilement des images
imageio.mimsave('BAC_results_per_year.gif', images, **kargs)