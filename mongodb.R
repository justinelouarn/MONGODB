#Test
library(mongolite)

#Connection à la base doctolib
coll <- mongo("dump_Jan2022", url = "mongodb+srv://etudiant:ur2@clusterm1.0rm7t.mongodb.net/doctolib",options = ssl_options(allow_invalid_hostname=TRUE, weak_cert_validation=TRUE))

#Liste des index de la collection
coll$index()

#Centres de vaccination situés à moins de 50km de Rennes

#requete mongodb
#var ref = {"type": "Point", "coordinates": [-1.6777926, 48.117266]}
#db.dump_Jan2022.find({"location": {$near : {$geometry : ref, 
#  $maxDistance: 50000}}})

#requete sur r
req.coord = coll$aggregate(
  '[
    { "$project": { 
        "name": 1, 
        "lng": { "$arrayElemAt": ["$location.coordinates", 0]}, 
        "lat": { "$arrayElemAt": ["$location.coordinates", 1]} 
    }}
]')
View(req.coord)

data = as.data.frame(req.coord[((req.coord$lng<=(-1.17127)) & (req.coord$lng>=(-2.04726))) & (req.coord$lat>=47.718)& (req.coord$lat<=48.5495),])
View(data) #affiche les centres de vaccination situés à moins de 50km de Rennes

#CARTE