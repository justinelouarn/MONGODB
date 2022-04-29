

from pymongo import MongoClient
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show, output_file
from bokeh.transform import dodge
from bokeh.layouts import column
from bokeh.models import Div, HoverTool
from math import pi
from bokeh.palettes import Category20c
from bokeh.transform import cumsum

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

show(p)



























