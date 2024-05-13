import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image

df = pd.read_csv("https://raw.githubusercontent.com/littlecelestedemon/pokemon_stats/main/pokemonDB_dataset.csv")

# set the categories for the radar graph
categories = ['HP','Attack','Defense','Speed', 'Special Defense', 'Special Attack']

# create the figure with plotly
fig = go.Figure()

colors = {"Normal": [255, 255, 255], "Fire": [201, 20, 35], "Water": [69, 94, 255],
          "Electric": [242, 214, 75], "Grass": [63, 232, 80], "Ice": [45, 249, 252],
          "Fighting": [135, 66, 26], "Poison": [73, 25, 112], "Ground": [92, 55, 11],
          "Flying": [3, 75, 153], "Psychic": [189, 34, 163], "Bug": [166, 209, 96],
          "Rock": [176, 143, 113], "Dragon": [66, 38, 97], "Ghost": [36, 13, 84],
          "Dark": [23, 11, 11], "Steel": [94, 94, 94], "Fairy": [238, 167, 250]}

# get both mon's name
val = input("Enter a Pokemon's name: ")
index = df.isin([val]).any(axis=1).idxmax()
while index == 0 and val.lower() != "abomasnow":
  print("Sorry, that's not a valid Pokemon name! Try: Charizard, Pikachu, Eevee, Mega Absol, etc.")
  val = input("Enter a Pokemon's name: ")
  index = df.isin([val]).any(axis=1).idxmax()

val_second = input("Enter another Pokemon's name: ")
index_second = df.isin([val_second]).any(axis=1).idxmax()
while index_second == 0 and val_second.lower() != "abomasnow":
  print("Sorry, that's not a valid Pokemon name! Try: Charizard, Pikachu, Eevee, Mega Absol, etc.")
  val_second = input("Enter a Pokemon's name: ")
  index_second = df.isin([val_second]).any(axis=1).idxmax()

# find the mon's row
mon = df.iloc[index]
mon_second = df.iloc[index_second]

# find its color
type_list = mon.loc["Type"]
type_one = type_list.split(",")[0]
color_1 = colors.get(type_one)
R = color_1[0]
G = color_1[1]
B = color_1[2]

# if there are two types, split them into two values
if "," in type_list:
  type_two = type_list.split(", ")[1]
  color_2 = colors.get(type_two)
  R = (color_1[0]+color_2[0]) // 2
  G = (color_1[1]+color_2[1]) // 2
  B = (color_1[2]+color_2[2]) // 2


# find its color
type_list_second = mon_second.loc["Type"]
type_one_second = type_list_second.split(",")[0]
color_1_second = colors.get(type_one_second)
R_second = color_1_second[0]
G_second = color_1_second[1]
B_second = color_1_second[2]

# if there are two types, split them into two values
if "," in type_list_second:
  type_two_second = type_list_second.split(", ")[1]
  color_2_second = colors.get(type_two_second)
  R_second = (color_1_second[0]+color_2_second[0]) // 2
  G_second = (color_1_second[1]+color_2_second[1]) // 2
  B_second = (color_1_second[2]+color_2_second[2]) // 2

# two different colors needed so we cannot repeat
color = str(R)+","+str(G)+","+str(B)
color_second = str(R_second)+","+str(G_second)+","+str(B_second)

# all of this is just to determine which pokemon's stats go first or second
# if all of a mon's stats are lower but they're inputted first, you cannot access their stats as easily
# generally better to have the mon with the highest stat as the one in the back aka drawn first
mon_stats = [mon.loc['HP Base'], mon.loc['Attack Base'], mon.loc['Defense Base'],
         mon.loc['Speed Base'], mon.loc['Special Defense Base'], mon.loc['Special Attack Base']]
mon_stats.sort(reverse=True)

mon_stats_second = [mon_second.loc['HP Base'], mon_second.loc['Attack Base'], mon_second.loc['Defense Base'],
         mon_second.loc['Speed Base'], mon_second.loc['Special Defense Base'], mon_second.loc['Special Attack Base']]
mon_stats_second.sort(reverse=True)

if mon_stats[0] > mon_stats_second[0]:
  fig.add_trace(go.Scatterpolar(
      r=[mon.loc['HP Base'], mon.loc['Attack Base'], mon.loc['Defense Base'],
         mon.loc['Speed Base'], mon.loc['Special Defense Base'], mon.loc['Special Attack Base']],
      theta=categories,
      fill='toself',
      name=val,
      fillcolor="rgba("+color+",0.5)",
      marker_color="rgb("+color+")"))

  fig.add_trace(go.Scatterpolar(
      r=[mon_second.loc['HP Base'], mon_second.loc['Attack Base'], mon_second.loc['Defense Base'],
         mon_second.loc['Speed Base'], mon_second.loc['Special Defense Base'], mon_second.loc['Special Attack Base']],
      theta=categories,
      fill='toself',
      name=val_second,
      fillcolor="rgba("+color_second+",0.5)",
      marker_color="rgb("+color_second+")"))
else:
  fig.add_trace(go.Scatterpolar(
      r=[mon_second.loc['HP Base'], mon_second.loc['Attack Base'], mon_second.loc['Defense Base'],
         mon_second.loc['Speed Base'], mon_second.loc['Special Defense Base'], mon_second.loc['Special Attack Base']],
      theta=categories,
      fill='toself',
      name=val_second,
      fillcolor="rgba("+color_second+",0.5)",
      marker_color="rgb("+color_second+")"))

  fig.add_trace(go.Scatterpolar(
      r=[mon.loc['HP Base'], mon.loc['Attack Base'], mon.loc['Defense Base'],
         mon.loc['Speed Base'], mon.loc['Special Defense Base'], mon.loc['Special Attack Base']],
      theta=categories,
      fill='toself',
      name=val,
      fillcolor="rgba("+color+",0.5)",
      marker_color="rgb("+color+")"))

# range will be 0 to the highest value
fig.update_layout(
      polar=dict(radialaxis=dict(
          visible=True,
          range=[0,250]
      )),
      showlegend=True)

# image loading and adding to the figure
# if the image can't be found, just skip
try:
  logo = Image.open("/content/drive/MyDrive/Images/" + val + "_new.png")
  logo_second = Image.open("/content/drive/MyDrive/Images/" + val_second + "_new.png")
  fig.add_layout_image(
    dict(
        source=logo,
        xref="paper", yref="paper",
        x=.15, y=.78,
        sizex=0.35, sizey=0.35,
        xanchor="right", yanchor="bottom"
        )
    )
  fig.add_layout_image(
      dict(
          source=logo_second,
          xref="paper", yref="paper",
          x=.95, y=.78,
          sizex=0.35, sizey=0.35,
          xanchor="right", yanchor="bottom"
      )
  )
except:
  print("No image(s), continuing without it.")

# adds the additional info on the mon + other annotations
fig.add_annotation(text="Name: " + val,
                  xref="paper", yref="paper",
                  x=0, y=.73, showarrow=False)
fig.add_annotation(text="Species: " + mon.loc["Species"],
                  xref="paper", yref="paper",
                  x=0, y=.68, showarrow=False)

# second mon
fig.add_annotation(text="Name: " + val_second,
                  xref="paper", yref="paper",
                  x=1, y=.73, showarrow=False)
fig.add_annotation(text="Species: " + mon_second.loc["Species"],
                  xref="paper", yref="paper",
                  x=1, y=.68, showarrow=False)

# show type or types, depending on if the mon has one or two
mon_type = mon.loc['Type']
if "," in mon_type:
  fig.add_annotation(text="Types: " + mon.loc["Type"],
                     xref="paper", yref="paper",
                     x=0, y=.6, showarrow=False)
else:
  fig.add_annotation(text="Type: " + mon.loc["Type"],
                     xref="paper", yref="paper",
                     x=0, y=.6, showarrow=False)

# height + weight
fig.add_annotation(text="Height: " + mon.loc["Height"],
                   xref="paper", yref="paper",
                   x=0, y=.55, showarrow=False)

fig.add_annotation(text="Weight: " + mon.loc["Weight"],
                   xref="paper", yref="paper",
                   x=0, y=.5, showarrow=False)

# 2nd pokemon shenanigans
mon_type = mon_second.loc['Type']
if "," in mon_type:
  fig.add_annotation(text="Types: " + mon_second.loc["Type"],
                     xref="paper", yref="paper",
                     x=1, y=.6, showarrow=False)
else:
  fig.add_annotation(text="Type: " + mon_second.loc["Type"],
                     xref="paper", yref="paper",
                     x=1, y=.6, showarrow=False)

# height + weight
fig.add_annotation(text="Height: " + mon_second.loc["Height"],
                   xref="paper", yref="paper",
                   x=1, y=.55, showarrow=False)

fig.add_annotation(text="Weight: " + mon_second.loc["Weight"],
                   xref="paper", yref="paper",
                   x=1, y=.5, showarrow=False)

# egg group shenanigans
egg_groups = mon.loc["Egg Groups"]
egg_groups = egg_groups.split(", ")
if len(egg_groups) == 1:
  fig.add_annotation(text="Egg Group: " + egg_groups[0],
                   xref="paper", yref="paper",
                   x=0, y=.45, showarrow=False)
else:
  fig.add_annotation(text="Egg Groups: " + mon.loc["Egg Groups"],
                   xref="paper", yref="paper",
                   x=0, y=.45, showarrow=False)

# second mon egg groups
egg_groups = mon_second.loc["Egg Groups"]
egg_groups = egg_groups.split(", ")
if len(egg_groups) == 1:
  fig.add_annotation(text="Egg Group: " + egg_groups[0],
                   xref="paper", yref="paper",
                   x=1, y=.45, showarrow=False)
else:
  fig.add_annotation(text="Egg Groups: " + mon_second.loc["Egg Groups"],
                   xref="paper", yref="paper",
                   x=1, y=.45, showarrow=False)

# ability shenanigans
abilities = mon.loc["Abilities"]
abilities = abilities.split(", ")

for i in range(len(abilities)):
  if i == 0:
    fig.add_annotation(text="Abiltiies: " + abilities[0],
                       xref="paper", yref="paper",
                       x=0, y=.4, showarrow=False)
  elif i == 1:
    fig.add_annotation(text=abilities[1],
                       xref="paper", yref="paper",
                       x=0,y=.35, showarrow=False)
  elif i == 2:
    fig.add_annotation(text=abilities[2],
                       xref="paper", yref="paper",
                       x=0,y=.275, showarrow=False)


# second mon ability shenanigans
abilities = mon_second.loc["Abilities"]
abilities = abilities.split(", ")

for i in range(len(abilities)):
  if i == 0:
    fig.add_annotation(text="Abiltiies: " + abilities[0],
                       xref="paper", yref="paper",
                       x=1, y=.4, showarrow=False)
  elif i == 1:
    fig.add_annotation(text=abilities[1],
                       xref="paper", yref="paper",
                       x=1,y=.35, showarrow=False)
  elif i == 2:
    fig.add_annotation(text=abilities[2],
                       xref="paper", yref="paper",
                       x=1,y=.275, showarrow=False)


# update the title, update legend, show
fig.update_layout(title_text = "Base Stats of " + val + " and " + val_second, title_x=0.5)

fig.update_layout(legend_bgcolor='rgb(194, 194, 194)')
fig.update_layout(legend_bordercolor='rgb(180, 180, 180)')
fig.update_layout(legend_borderwidth=2)

fig.update_layout(paper_bgcolor='rgb(219, 243, 255)')
fig.update_layout(plot_bgcolor='rgb(180, 209, 184)')

fig.update_layout(polar = dict(bgcolor = "rgb(156, 184, 160)"))

fig.show()

# this figure is adjusted to the biggest maximum stat
# this is because we're comparing a pokemon to itself
# the relative difference between two pokemon matters not
# only the difference between the max, min, and base stats of a single mon
# therefore, adjusting the max to whatever stat is highest is valid for this visualization
