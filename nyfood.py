#importation des packages
from pymongo import MongoClient

#importation de la base
db_uri = "mongodb+srv://etudiant:ur2@clusterm1.0rm7t.mongodb.net/"
client = MongoClient(db_uri)
db = client["food"]
coll = db["NYfood"]


# aggrégation
cursor_agreg = coll.aggregate([
  {"$group": {"_id": "$borough",
              "nb_restos": {"$sum": 1}}
  }
])

# affichage
for agreg in cursor_agreg:
    print(agreg["nb_restos"], "restaurants dans le quartier", agreg["_id"])



