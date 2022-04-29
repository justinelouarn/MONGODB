
from pymongo import MongoClient
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show, output_file
from bokeh.transform import dodge
from bokeh.layouts import column, row
from bokeh.models import Div, HoverTool
from math import pi
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
from bokeh.models.widgets import Tabs, Panel

#importation de la base
db_uri = "mongodb+srv://etudiant:ur2@clusterm1.0rm7t.mongodb.net/"
client = MongoClient(db_uri)
db = client["food"]
coll = db["NYfood"]
print(coll)

# Nombre de restau par quartiers 
Requete = coll.aggregate([
                        {"$unwind": "$grades"},
                        {"$group": {"_id": {"note":"$grades.grade"},
                                  "nb": {"$sum": 1}}}
                      ])



liste_requete=[]
for i in Requete:
    liste_requete.append(i)
print(liste_requete)



df1 = pd.DataFrame(liste_requete)
df1 = pd.DataFrame(df1['_id'].values.tolist(), index=df1.index)




df2 = pd.DataFrame(liste_requete)

df = pd.concat([df1, df2], axis=1)
df.pop('_id')

source = ColumnDataSource(data=df)





x = {
    'A' : int(df.nb[df.note=="A"]),
    'B' : int(df.nb[df.note=="B"]),
    'C' : int(df.nb[df.note=="C"]),
    'P' : int(df.nb[df.note=="P"]),
    'Z' : int(df.nb[df.note=="Z"]),
    'Not Yet Graded' : int(df.nb[df.note=="Not Yet Graded"]),
}

data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'notes'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Category20c[len(x)]

p = figure(height=350, title="Repartition des notes des restaurants de New-York", toolbar_location=None,
           tools="hover", tooltips="@notes: @value", x_range=(-0.5, 1.0))

p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='notes', source=data)

p.axis.axis_label = None
p.axis.visible = False
p.grid.grid_line_color = None

div1 = Div(text="""<h2> Répartition des notes attribuées aux restaurants de New York </h2>
<p> La note la plus attribuée pour les restaurants de New York est la note A avec 74 652 attributions.
Elle représente plus de 3/4 des attributions. Puis, les notes les plus attribués après A sont dans l'ordre B, C, P et Z.
Seulement 1 337 restaurants n'ont pas eu de notes</p>""")

layout1 = row(div1, column(p))


#### HISTOGRAMME nombre de restau par quartier

requete2 = coll.aggregate([
  {"$group": {"_id": "$borough",
              "nb_restos": {"$sum": 1}}
  }
])

# affichage

liste_nb=[]
liste_qrt=[]
for agreg in requete2:
    liste_nb.append(agreg["nb_restos"])
    liste_qrt.append(agreg["_id"])

p2 = figure(x_range= liste_qrt,title="Nombre de restaurants par quartier",x_axis_label = "Quartiers", y_axis_label = "Nombre de restaurants")
p2.vbar(x=liste_qrt,top=liste_nb, color='purple', width=0.5, alpha=0.5)

div2 = Div(text="""<h2> Histogramme du nombre de restaurants par quartier de New York </h2>
 <p><a href="index.html">Sommaire</a></p>
<p> Le quartier de New York qui compte le plus de restaurants est Manhattan avec plus de 1000 restaurants. Celui qui compte le moins est Staten Island
</p>""")
layout2 = row(div2, column(p2))


####### LES ONGLETS
tab = Panel(child=layout1, title="PIE CHART")
tab2 = Panel(child=layout2, title="HISTOGRAMME")

Tabs1 = Tabs(tabs=[tab, tab2])
output_file("nyfood_2.html")
show(Tabs1)





















