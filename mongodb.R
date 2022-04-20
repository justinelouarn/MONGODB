#Packages
library(mongolite)
library(ggplot2)
library(ggmap)
library(leaflet)

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
        "visit_motives.first_shot_motive":1,
        "visit_motives.slots":1,
        "lng": { "$arrayElemAt": ["$location.coordinates", 0]}, 
        "lat": { "$arrayElemAt": ["$location.coordinates", 1]} 
    }}
]')
View(req.coord)

data = as.data.frame(req.coord[((req.coord$lng<=(-1.17127)) & (req.coord$lng>=(-2.04726))) & (req.coord$lat>=47.718)& (req.coord$lat<=48.5495),])
View(data) #affiche les centres de vaccination situés à moins de 50km de Rennes

data$visit_motives

#CARTE

#carte de Rennes
#rennes <- c(left = -3, bottom = 47, right = -1, top = 49)
#fond <- get_stamenmap(rennes, zoom = 7,"toner-lite")
#ggmap(fond)+geom_point(data=data, aes(x=lng,y=lat),color="red")

leaflet(data = data) %>% addTiles() %>%
  addCircleMarkers(~ lng, ~ lat,stroke = FALSE, fillOpacity = 0.7,
                   popup = ~name)

