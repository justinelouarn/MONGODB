#importation des packages
from pymongo import MongoClient

#importation de la base
db_uri = "mongodb+srv://etudiant:ur2@clusterm1.0rm7t.mongodb.net/"
client = MongoClient(db_uri)
db = client["food"]
coll = db["NYfood"]

# Nombre de restau par quartiers 
cursor_agreg = coll.aggregate([
  {"$group": {"_id": "$borough",
              "nb_restos": {"$sum": 1}}
  }
])

# affichage
# for agreg in cursor_agreg:
#     print(agreg["nb_restos"], "restaurants dans le quartier", agreg["_id"])

liste_nb = []
liste_quartier = []
for obj in cursor_agreg :
    liste_nb.append(obj["nb_restos"])
    liste_quartier.append(obj["_id"])

print(liste_nb)
print(liste_quartier)
