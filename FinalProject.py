"""
TJ Smith
CS230
Final Project
Skyscrapers2021
https://share.streamlit.io/tsmith224/streamlit/main/FinalProject.py
"""
from pandas import DataFrame, read_csv
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk
import numpy as np

#Histogram Function
def histogram(df,materials,color,choice,display='Height(Feet)'):
    dfmaterial = df[df['MATERIAL']==materials] #Creates new dataframe based on the users input of materials (concrete, steel, etc.)
    st.write(dfmaterial)
    plt.hist(dfmaterial[f'{choice}'],bins=5,color=color,edgecolor='Black')
    plt.title(f'Frequencies of skyscrapers made from {materials}')
    plt.ylabel('Number of Skyscrapers')
    plt.xticks(rotation=60)
    plt.xlabel(f'{choice}')
    return plt

#Map Function
def year_map(df,year):
    dfyear = df[df['COMPLETION']<=year]#New dataframe based on users input for year
    st.write(dfyear)
    name = []
    lat = []
    lon = []
    height = []
    for index,row in dfyear.iterrows():
        name.append(row['NAME'])
        lat.append(row['latitude'])
        lon.append(row['longitude'])
        height.append(row['Feet'])

    location = list(zip(name,lat,lon,height))

    df_map = pd.DataFrame(location, columns=["Name", "lat", "lon",'Feet'])

    view = pdk.ViewState(latitude=df_map['lat'].mean(), longitude=df_map['lon'].mean(), zoom=10, pitch=50)

    layer1 = pdk.Layer('ColumnLayer', data=df_map,get_position='[lon, lat]',auto_Highlight=True,get_elevation='Feet',get_radius=100,
                       get_color=[255,0,0],pickable=True,extruded=True,elevationScale=1,coverage=.2
                       )

    tool_tip = {"html" : "This is the {Name}. It has a height of {Feet}. "}

    map = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',initial_view_state=view,layers=[layer1],tooltip= tool_tip)

    st.pydeck_chart(map)

#Main Function
def main():

    #Title and reading data
    st.title("Welcome to TJ's CS230 Final Project!")
    datafile = "Skyscrapers2021.csv"
    df = pd.read_csv(datafile)

    #Using drop to modify dataframe
    data_hist = df.drop(['NAME', 'CITY','Full Address','latitude','longitude','COMPLETION','FUNCTION','Meters'],axis=1)
    data_map = df.drop(['Full Address','Meters','FLOORS','MATERIAL','FUNCTION'],axis=1)

    #Getting list of all materials
    material = []
    for x in data_hist['MATERIAL']:
        if x not in material:
            material.append(x)
    materials = st.selectbox('Choose which materials you would like to display:', material)

    #Checkbox to choose Feet or Floors
    st.sidebar.header('Choose which column value you would like to display. ')
    feet = st.sidebar.checkbox("Height(Feet)", True)
    floors = st.sidebar.checkbox("FLOORS", False)

    #Color Picker
    colors = st.sidebar.color_picker('Choose a color to display on the histogram')
    if feet:
        choice = 'Feet'
    if floors:
        choice = 'FLOORS'
    st.pyplot(histogram(data_hist,materials,colors,choice,'FLOORS'))

    #Slider for map years
    st.subheader('Map of the Skyscrapers across the world')
    year = st.slider('Choose which years you would like to display',min_value=1931,max_value=2021)
    year_map(data_map,year)

main()

