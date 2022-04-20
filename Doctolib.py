#importation des packages
from pymongo import MongoClient
import matplotlib.pyplot as plt

#importation de la base
db_uri = "mongodb+srv://etudiant:ur2@clusterm1.0rm7t.mongodb.net/"
client = MongoClient(db_uri)
db = client["doctolib"]
coll = db["dump_Jan2022"]