#Packages
library(mongolite)
library(leaflet)
library(dplyr)

#Connection à la base doctolib
coll <- mongo("dump_Jan2022", url = "mongodb+srv://etudiant:ur2@clusterm1.0rm7t.mongodb.net/doctolib",options = ssl_options(allow_invalid_hostname=TRUE, weak_cert_validation=TRUE))

#Centres de vaccination situés à moins de 50km de Rennes

#requete mongodb
#var ref = {"type": "Point", "coordinates": [-1.6777926, 48.117266]}
#db.dump_Jan2022.find({"location": {$near : {$geometry : ref, 
#  $maxDistance: 50000}}})

#requete R
#commentaires détails
requete = '[
{"$geoNear": {"near": {"type": "Point","coordinates": [-1.6777926, 48.117266]},
"distanceField": "distance","maxDistance": 50000}},

{"$match": {"$nor":[{"visit_motives": {"$size": 0}}]}},
{"$unwind" : "$visit_motives"},

{"$match": {"$nor":[{"visit_motives.slots": {"$size": 0}}]}},
{"$unwind" : "$visit_motives.slots"},

{"$match": {"visit_motives.slots": {"$lte": {"$date": "2022-01-29T00:00:00Z"},"$gte": {"$date": "2022-01-26T00:00:00Z"}}}},

{"$group" : {"_id": "$name","nb": {"$sum": 1},
"coord":{"$max":"$location.coordinates"}}}
]'

docto <- coll$aggregate(requete)

#avoir longitudes et latitudes
#req.coord = coll$aggregate(
#  '[
#    { "$project": { 
#        "name": 1,
#        "visit_motives.first_shot_motive":1,
#        "visit_motives.slots":1,
#        "lng": { "$arrayElemAt": ["$location.coordinates", 0]}, 
#        "lat": { "$arrayElemAt": ["$location.coordinates", 1]} 
#    }}
#]')
#View(req.coord)
#commentaires fonctionne pas


## Création des coordonnées longitude et latitude
coord <- docto$coord
lng <- c()
lat <- c()

for (i in 1:length(coord)){
  lng[i] <- coord[[i]][1]
  lat[i] <- coord[[i]][2]
}

docto$lng <- lng
docto$lat <- lat

#Affectation des couleurs à partir de seuil

#on regarde le summary et la répartition pour déterminer les classes adaptées
summary(docto$nb)
table(docto$nb)

#on choisit 3 classes : de 0 à 50, de 51 à 120, de 121 et plus
col <- c()
for (i in 1:nrow(docto)){
  if (docto$nb[i] <= 50){
    col[i] <- 'red'
  }
  else if (docto$nb[i] > 50 & docto$nb[i] <= 120){
    col[i] <- 'orange'
  }
  else if (docto$nb[i] > 120){
    col[i] <- 'green'
  }
}

#CARTE
#_id ne s'affiche pas, on le renomme en name
colnames(docto)[1] <- 'name'

leaflet(data = docto) %>% addTiles() %>%
  addCircleMarkers(~ lng, ~ lat,stroke = FALSE, fillOpacity = 0.7,
                   popup = ~paste("Le centre de vaccination ", name, " a ",as.character(nb),' créneaux ouverts.'), color =col)

