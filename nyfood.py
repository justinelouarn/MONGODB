#importation des packages
from pymongo import MongoClient
import matplotlib.pyplot as plt

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

liste_nb=[]
liste_qrt=[]
for agreg in cursor_agreg:
    liste_nb.append(agreg["nb_restos"])
    liste_qrt.append(agreg["_id"])
print(liste_nb)
print(liste_qrt)


# Création du graphe
plt.figure(figsize = (10, 5))
plt.bar(liste_qrt, liste_nb, color ='blue', width = 0.4)
plt.xlabel("Quartier")
plt.ylabel("Nombre")
plt.title("Nombre de restaurants par quartier")
plt.show()

