# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iV216hk3_Cq4w3SdGEgDJfFJM6ZK4mB2

# Interactive Data Visualization using Python and Matplotlib
# Data Visualization
## Assignment 2
## Dublin Business School
### Dataset: https://www.kaggle.com/rush4ratio/video-game-sales-with-ratings
"""

from google.colab import files
uploaded= files.upload()

import altair as alt
import pandas as pd
import numpy as np
import seaborn as sns

import folium
import io
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

df=pd.read_csv(io.BytesIO(uploaded['Video_Games_Sales.csv']))

alt.data_transformers.enable('default',max_rows=None)

df.head()

df.Year_of_Release=df.Year_of_Release.astype('int64')

interval = alt.selection_interval()

points = alt.Chart(df).mark_circle().encode(
  x= 'Platform',
  y= 'User_Count',
  color=alt.condition(interval, 'Genre', alt.value('gray'))
).properties(
  selection=interval
)

histogram = alt.Chart(df).mark_bar().encode(
  x='count()',
  y='Genre',
  color='Genre'
).transform_filter(interval)

points & histogram

input_dropdown = alt.binding_select(options=['PS', 'PS2', 'PS3', 'PS4', 'PSP', 'X360', 'XB', 'XOne', 'Wii', 'WiiU', 'WS', '2600', '3DO', '3DS', 'DC', 'DS', 'GB', 'GBA', 'GC',
                                             'GEN', 'GG', 'N64', 'NES', 'NG','PC', 'PCFX', 'PSV', 'SAT', 'SCD', 'SNES', 'TG16'])
selection = alt.selection_single(fields=['Platform'], bind=input_dropdown, name=' ')
color = alt.condition(selection,
                    alt.Color('Platform:N', legend = None),
                    alt.value('gray'))

alt.Chart(df).mark_bar().encode(
    x="Genre",
    y="Global_Sales",
    color=color
).properties(
  width = 1000
).add_selection(
    selection
).interactive()

selector = alt.selection_single(empty='all', fields=['Platform'])

base = alt.Chart(df).properties(
    width=250,
    height=250
).add_selection(selector)

points = base.mark_point(filled=True, size=200).encode(
    x=('User_Score'),
    y='User_Count',
    color=alt.condition(selector, 'id:O', alt.value('gray'), legend=None),
).interactive()

timeseries = base.mark_line().encode(
    x='Critic_Score',
    y='Critic_Count',
    color=alt.Color('id:O', legend=None)
).transform_filter(
    selector
)

points | timeseries

brush = alt.selection(type='interval', encodings=['x'])

# Define the base chart, with the common parts of the
# background and highlights
base = alt.Chart().mark_line().encode(
    x=alt.X(alt.repeat('column'), type='quantitative', bin=alt.Bin(maxbins=20)),
    y='Global_Sales'
).properties(
    width=160,
    height=130
)

# blue background with selection
background = base.add_selection(brush)

# yellow highlights on the transformed data
highlight = base.encode(
    color=alt.value('red')
).transform_filter(brush)

# layer the two charts & repeat
alt.layer(
    background,
    highlight,
    data=df
).transform_calculate(
    "time",
    "hours(datum.date)"
).repeat(column=["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"])

brush = alt.selection(type='interval', resolve='global')

base = alt.Chart(df).mark_square().encode(
    y='Global_Sales',
    color=alt.condition(brush, 'Genre', alt.ColorValue('gray')),
).add_selection(
    brush
).properties(
    width=250,
    height=250
).interactive()

base.encode(x='NA_Sales') | base.encode(x='EU_Sales') | base.encode(x='JP_Sales') | base.encode(x='Other_Sales')

np.random.seed(42)
df = pd.DataFrame(np.cumsum(np.random.randn(100, 6), 0).round(1),
                    columns=['Electronic Arts', 'EA Sports', 'Ubisoft', 'Nintendo', 'Rockstar', 'Bungie'], index=pd.RangeIndex(100, name='x'))

df = df.reset_index().melt('x', var_name='Developer', value_name='Global_Sales')
# Create a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['x'], empty='none')

# The basic line
line = alt.Chart(df).mark_line(interpolate='basis').encode(
    x='Year_of_Release:T',
    y='Global_Sales:Q',
    color='Developer:N'
)

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = alt.Chart(df).mark_point().encode(
    x='Year_of_Release:T',
    opacity=alt.value(1980),
).add_selection(
    nearest
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# Draw text labels near the points, and highlight based on selection
text = line.mark_text(align='left', dx=100, dy=0).encode(
    text=alt.condition(nearest, 'Global_Sales:Q', alt.value(' '))
)

# Draw a rule at the location of the selection
rules = alt.Chart(df).mark_rule(color='gray').encode(
    x='Year_of_Release:T',
).transform_filter(
    nearest
)

# Put the five layers into a chart and bind the data
alt.layer(
    line, selectors, points, rules, text
).properties(
    width=600, height=300
)