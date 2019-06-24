# -*- coding: utf-8 -*-

"""
	Représentation des nombres de candidats au bac de 2012 à 2016
	suivant les différentes régions du Sénégal

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
	Nombres de candidats au bac entre 2012 et 2016
"""
if getFile('.', 'BAC_candidates_per_year.csv') == 1 :
		exit()
nbCandidats = pd.read_csv(getFile('.', 'BAC_candidates_per_year.csv'), index_col=0)


# Fixation de la taille de l'espace du rendu
plt.rcParams['figure.figsize'] = (20, 10)


"""
	% d'admis dans chaque région du Sénégal entre 2012 et 2016
"""
images = []
for year in range(2012, 2017, 1) :
	# Récupération des résultats pour une année (year)
	fileName = 'BAC_results_'+str(year)+'.csv'
	if getFile('..', fileName) == 1 :
		exit()
	data = pd.read_csv(getFile('..', fileName), index_col=0)

	# Calcul du % de réussite de chaque région
	admis = [0]
	for i in range(len(data.index)) :
		admis.append(data.loc[regionsSN[i]][1] * 100 / nbCandidats.loc[year][0])
	admis.append(50) # Résultats < 50 => 50 max pour la représentation

	# Ajout des résultats, à la région correspondante, au dictionnaire "senegal"
	senegal['Nb Candidats (%)'] = tuple(admis)

	# Dessin de la carte en fonction des % de réussite
	mapSN = senegal.plot(column='Nb Candidats (%)', scheme='Equal_Interval', k=7, cmap='YlGn', edgecolor='grey', legend=True)
	mapSN.set_title('%% de candidats au bac au Sénégal par région ('+str(year)+')')
	leg = mapSN.get_legend()
	leg.set_title('%% de candidats')
	mapSN.set_axis_off()

	# Placement des noms des régions sur la carte
	if getFile('..', 'regionsName.json') == 1 :
		sys.exit()
	regionsName = gpd.read_file(getFile('..', 'regionsName.json'))
	for idx, row in regionsName.iterrows() :
		coordinates = row['geometry'].coords.xy
		x, y = coordinates[0][0], coordinates[1][0]
		mapSN.annotate(row['name'], xy=(x, y), xytext=(x, y), family='serif', fontweight='bold', horizontalalignment='center')

	## Sauvegarde dans les fichiers .png respectifs
	fileName = 'BAC_candidates_'+str(year)+'.png'
	plt.savefig(fileName, bbox_inches='tight')
	images.append(imageio.imread(fileName))
# Génération du gif à partir des images stockées dans la variable images
kargs = {'duration' : 1} # Duréee de défilement des images
imageio.mimsave('BAC_candidates.gif', images, **kargs)
