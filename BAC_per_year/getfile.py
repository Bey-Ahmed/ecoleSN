"""
	Fonction de récupération d'un fichier

"""

import os

def getFile(path, fileName) :
	for root, dirs, files in os.walk(path) :
		for name in files :
			if name == fileName :
				filePath = os.path.abspath(os.path.join(root, name))

	# Vérification de l'existance du fichier
	try :
		filePath
	except NameError :
		print(fileName, 'inexistant!')
		return 1

	return filePath
