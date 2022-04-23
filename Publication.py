# Importation des packages
from pymongo import MongoClient
import matplotlib.pyplot as plt

# Importation de la base
db_uri = "mongodb+srv://etudiant:ur2@clusterm1.0rm7t.mongodb.net/"
client = MongoClient(db_uri)
db = client["publications"]
coll = db["hal_irisa_2021"]

# Requête : 
##Les 20 auteurs 
### Avec plus de 20 publications
#### Classés du plus au moins prolifique
 

Requete = db.hal_irisa_2021.aggregate([
                        {"$unwind": "$authors"}, # découpage par auteur
                        {"$group": {"_id": {"name": "$authors.name",
                                            "firstname": "$authors.firstname"}, # groupement par nom+prenom de l'auteur
                                     "nb_publi": {"$sum": 1}} # comptage des lignes
                        },
                        {"$sort": {"nb_publi": -1}}, # ordre décroissant
                        {"$limit": 20} # les 20 premieres lignes
                      ])

resu = []
for i in Requete:
    resu.append(i)

#print(resu)
## {'name': 'Lefèvre', 'firstname': 'Sébastien'}, 'nb_publi': 24}
### Sébastien Lefèvre a 24 publications