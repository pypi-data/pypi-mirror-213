"""
progression_qc est un compilateur/validateur pour la production de d'exercices pour Progression. progression_qc reçoit sur l'entrée standard ou en paramètre un fichier YAML contenant la description d'une question et reproduit sur la sortie standard le résultat traité et validé.
"""

import os

print(os.environ)

__version__ = os.environ["VERSION"]
__author__ = "Patrick Lafrance"
