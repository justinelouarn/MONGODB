
#########################################################
#                                                       #
#           IMPORTATION DES PACKAGES                    #
#                                                       #
#########################################################

from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx


from bokeh.io import output_file, show
from bokeh.models import BoxZoomTool, Circle, HoverTool,MultiLine,Plot, Range1d, ResetTool, Column, Div,Row
from bokeh.palettes import PuRd8
from bokeh.plotting import from_networkx, figure
from bokeh.transform import linear_cmap

#########################################################
#                                                       #
#           IMPORTATION DES DONNEES                     #
#                                                       #
#########################################################

# Importation de la base
db_uri = "mongodb+srv://etudiant:ur2@clusterm1.0rm7t.mongodb.net/"
client = MongoClient(db_uri)
db = client["publications"]
coll = db["hal_irisa_2021"]


#########################################################
#                                                       #
#                   PARTIE REQUETE                      #
#                                                       #
#########################################################

# Requête : 
##Les auteurs 
### Classés du plus au moins prolifique
#### Garder les 20 premiers
##### Récuperer la liste des publications par auteur : operateur $push
 

Requete = db.hal_irisa_2021.aggregate([
                        {"$unwind": "$authors"}, # découpage par auteur
                        {"$group": {"_id": {"name": "$authors.name",
                                            "firstname": "$authors.firstname"}, # groupement par nom+prenom de l'auteur
                                    "liste_titres": {"$push": "$title"},
                                     "nb_publi": {"$sum": 1}} # comptage des lignes
                        },
                        {"$sort": {"nb_publi": -1}}, # ordre décroissant
                        {"$limit": 20},# les 20 premieres lignes
                        
                        
                        {"$group": {"_id": {"Prenom": "$_id.name", # 2ème group by pour avoir une sortie plus adaptée
                            "Nom": "$_id.firstname",
                            "Liste_titres" : "$liste_titres",
                            "Nb_publi": "$nb_publi"}}} 
                      ])

#for ligne in  Requete :
#    print(ligne)


#########################################################
#                                                       #
#      CREATION DATAFRAME : AUTEUR + NB DE PUBLI        #
#                                                       #
#########################################################


# Création liste avec informations auteur + nombre de publications associées.
auteur_nb_publi = [auteur["_id"] for auteur in Requete]
#print(len(auteur_nb_publi))

    

# Création du dataframe à partir de la liste ci-dessus.

df = []
for auteur in auteur_nb_publi:  
    df.append(auteur) 
  
df = pd.DataFrame(df)  # transformation dataframe exploitable.
print(df)

#########################################################
#                                                       #
#      CREATION LISTES PUBLICATIONS ET RELATIONS        #
#                                                       #
#########################################################


nb_publi = []  # nombre de publications par auteur
nb_publi_co = [] # nombre de publications communes à 2 auteurs.
noeud_auteur_2 = []
noeud_auteur_1 = []



#publi_auteur_lefevre = list(df.Liste_titres[df.Prenom == "Lefèvre"])[0]
# Bien spécifier [0] sinon on n'accede pas à la liste des titres



# Parcourir tous les auteurs et récuperer la liste de leurs titres de publications.



###########################################################################################
# 1ere etape : récupérer par paire d'auteurs : l'ensemble des titres                      #
###########################################################################################


for auteur_1 in df.Prenom :
    
    publi_auteur_1 = list(df.Liste_titres[df.Prenom == auteur_1])[0]

    for auteur_2 in df.Prenom :
        if auteur_1 == auteur_2: # Ne pas comparer un auteur avec lui-même
            continue
        # Récuperer la liste deS titres de publications de l'auteur 2.
        publi_auteur_2 = list(df.Liste_titres[df.Prenom == auteur_2])[0]
        
        publi_1_2 = publi_auteur_1 + publi_auteur_2 # Regrouper les 2 listes de titres de l'auteur 1 et 2.
 
        
 
###########################################################################################
# 2eme etape : récupérer par paire d'auteurs : l'ensemble des titres COMMUNS              #
###########################################################################################

        titre_unique =[]
        cpt = 0
        
        
        for elem in publi_1_2: # On parcourt tous les titres des 2 auteurs.
            if elem not in titre_unique: # Ajout dans liste si pas encore présent.
                titre_unique.append(elem)
                compte = publi_1_2.count(elem) # on compte le nombre de fois que cet élément apparait dans publi_1_2.
                if compte > 1:# S'il apparait + d'une fois = les 2 auteurs sont en commun : alors on ajoute +1 au compteur cpt.
                    cpt=cpt+1
        commun = int(cpt)
        

        noeud_auteur_1.append(auteur_1)
        noeud_auteur_2.append(auteur_2)
        nb_publi_co.append(commun)
        
        
        nb_publi.append(int(df.Nb_publi[df.Prenom == auteur_1]))
        



# dataframe necessaire pour la réalisation du graphe.
graphe = pd.DataFrame({"source": noeud_auteur_1, "target": noeud_auteur_2, "weight": nb_publi_co, "node_size": nb_publi})


#########################################################
#                                                       #
#      SELECTION AUTEURS AVEC AU MOINS 1 LIEN           #
#                                                       #
#########################################################


print(graphe)




filtre=graphe['weight'] >= 1

graphe = graphe[filtre]

print(len(graphe.source.unique()))
## il  nous manque 6 de nos auteurs..

# qui sont ils ?  

liste_auteurs =set(list( graphe.source) + list(graphe.target))
print(liste_auteurs)
             
for i in df.Prenom : 
    
     if i not in liste_auteurs :
         print(i)
    


#Jézéquel
#Rubino
#Berder
#Martin
#Busnel
#Legeai
#["Jézéquel","Rubino","Berder","Martin","Busnel","Legeai"]






# Transformation du dataframe en reseau
P = nx.from_pandas_edgelist(graphe)

#########################################################
#                                                       #
#               PREPARATION BOKEH                       #
#                                                       #
#########################################################


auteur_unique = graphe.copy() # Faire une copie 
auteur_unique.drop_duplicates(subset ="source", keep = 'first', inplace=True)


# Création dictionnaire association auteur et son nombre de publications.


dico_auteur_publi = {}
j=0 # objectif : associer les valeurs  des noeuds aux auteurs
for auteur in auteur_unique.source:
    dico_auteur_publi[auteur] = auteur_unique.node_size.values[j]
    j+=1


# Création dictionnaire association lien et sa taille = au nombre de publication en commun entre 2 auteurs.
dico_edges = {}
j=0
for edge in P.edges():
    dico_edges[edge] = graphe.weight.values[j]
    j+=1
    
# ajouter le dico_auteur_publi créé comme attribut du noeud.
nx.set_node_attributes(P, name='adjusted_node_size', values=dico_auteur_publi)

# ajouter le dico_edges créé comme attribut du lien.
nx.set_edge_attributes(P, name='weight', values=dico_edges)





#########################################################
#                                                       #
#                     OUTILS SURVOL                     #
#                                                       #
#########################################################


HOVER_TOOLTIPS = [ ("Prenom ", "@index"), ("Publications totales ", "@adjusted_node_size")]


#########################################################
#                                                       #
#                CREATION GRAPHIQUE                     #
#                                                       #
#########################################################




# Création du network
nx_graph = from_networkx(P, nx.circular_layout, scale=10, center=(0, 0)) 


plot = figure(tooltips = HOVER_TOOLTIPS,
              tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
              x_range=Range1d(-15, 15), y_range=Range1d(-15, 15),title='Réseau des 20 auteurs les plus prolifiques avec au moins une co-publication')

#########################################################
#                                                       #
#               AFFECTATION POIDS                       #
#                                                       #
#########################################################




# Récupération valeur minimale
mini = min(nx_graph.node_renderer.data_source.data['adjusted_node_size'])
#print(mini)
# Récupération valeur maximale
maxi = max(nx_graph.node_renderer.data_source.data['adjusted_node_size'])
#print(maxi)
# Affectation taille avec parametres mini et maxi
nx_graph.node_renderer.glyph = Circle(size='adjusted_node_size', fill_color=linear_cmap('adjusted_node_size', PuRd8, mini, maxi))



#########################################################
#                                                       #
#               AFFECTATION TAILLE                      #
#                                                       #
#########################################################



nx_graph.edge_renderer.glyph = MultiLine(line_alpha=0.6, line_width='weight') 
plot.renderers.append(nx_graph)




#########################################################
#                                                       #
#                       CODE HTML                       #
#                                                       #
#########################################################

div = Div(text="""
<h1> Réseau de publications scientifiques </h1>
<p>Ce graphique représente les liens de co-publication des 20 auteurs les plus prolifiques de publications scientifiques de l'IRISA </p>
<p>A l'aide de ce graphique on se rend compte que ce n'est pas le scientifique qui a écrit le plus d'articles (Lefèvre) qui est celui qui a le fait le plus de collaborations.</p>
""")

#########################################################
#                                                       #
#               ONGLET + AFFICHAGE WEB                  #
#                                                       #
#########################################################

layout = Row(Column(div, plot))
output_file("Publications.html")
show(layout)