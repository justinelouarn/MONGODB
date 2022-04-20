#Test
library(mongolite)

#1.Connectez vous à la base food
coll <- mongo("NYfood", url = "mongodb+srv://etudiant:ur2@clusterm1.0rm7t.mongodb.net/food",options = ssl_options(allow_invalid_hostname=TRUE, weak_cert_validation=TRUE))

#3.Affichez la liste des index de la collection NYfood.
coll$index()

#4.Affichez la liste des restaurants de Manhattan dont le nom commence par A.
q = '{"borough": "Manhattan","name":{"$gte":"A", "$lt": "B"}}'
res <- as.data.frame(coll$find(q))
View(res)

