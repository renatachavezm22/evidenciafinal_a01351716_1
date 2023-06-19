import streamlit as st
#import numpy as np
import pandas as pd
#import plotly as px
#import plotly.figure_factury as ff
#from brokeh.plotting import figure
import matplotlib.pyplot as plt
from datetime import datetime


st.header(':blue[Police Incident Reports from 2018 to 2020 in San Francisco] :police_car: :us:')

df = pd.read_csv('Police_Department_Incident_Reports__2018_to_Present.csv')
st.dataframe(df)

st.markdown('The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location and resolution.')

mapa = pd.DataFrame()
mapa['Date']= df['Incident Date']
mapa['Day']= df['Incident Day of Week']
mapa['Police District']= df['Police District']
mapa['Neighborhood']= df['Analysis Neighborhood']
mapa['Incident Category']= df['Incident Subcategory']
mapa['Resolution'] = df['Resolution']
mapa['lat'] = df['Latitude']
mapa['lon'] = df['Longitude']
mapa = mapa.dropna()
st.map(mapa.astype({'lat': 'float32', 'lon': 'float32'}))

subset_data2=mapa
police_district_input= st.sidebar.multiselect(
    'Police District',
    mapa.groupby('Police District').count().reset_index()['Police District'].tolist())
if len(police_district_input)>0:
    subset_data2=mapa[mapa['Police District'].isin(police_district_input)]
    

subset_data1=subset_data2
neighborhood_input= st.sidebar.multiselect(
    'Neighborhood',
    mapa.groupby('Neighborhood').count().reset_index()['Neighborhood'].tolist())
if len(neighborhood_input)>0:
    subset_data1=subset_data2[subset_data2['Neighborhood'].isin(neighborhood_input)]


subset_data=subset_data1
incident_input= st.sidebar.multiselect(
    'Incident Category',
    mapa.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())
if len(incident_input)>0:
    subset_data=subset_data1[subset_data1['Incident Category'].isin(incident_input)]

st.sidebar.write("Renata Emilia Chávez Martínez")
st.sidebar.write("A01351716")

subset_data

total_incidents = len(subset_data)
st.subheader('Total Incidents📚')
st.info(total_incidents)

st.markdown('It is important to mention that any police district can respond to any incident, the neighborhood in which it happened is not related to the police district. ⚠️🏙️')
st.subheader('Crime locations in San Francisco 🗺️')
st.map(subset_data)
st.subheader('Crimes per day of the week 📅')
st.bar_chart(subset_data['Day'].value_counts())
st.subheader('Crimes occurred per day 📅')
st.bar_chart(subset_data['Date'].value_counts())
st.subheader('Types of crimes committed 🚨')
st.bar_chart(subset_data['Incident Category'].value_counts())


agree=st.button('Click to see incident subcategories')
if agree:
    st.markdown('Subtypes of crimes committed 🚓📚')
    st.bar_chart(subset_data['Incident Subcategory'].value_counts())

st.subheader('Resolution Status 📝')
fig1, ax1= plt.subplots()
labels=subset_data['Resolution'].unique()
ax1.pie(subset_data['Resolution'].value_counts(), labels=labels, autopct='%1.1f%%',startangle=20)
st.pyplot(fig1)

resolution_percentage = subset_data.groupby('Incident Category')['Resolution'].value_counts(normalize=True).mul(100).rename('Percentage').reset_index()

st.subheader('Resolution Percentage📝 by Category')
fig2, ax2 = plt.subplots()
for category in resolution_percentage['Incident Category'].unique():
    data = resolution_percentage[resolution_percentage['Incident Category'] == category]
    ax2.bar(data['Resolution'], data['Percentage'], label=category)
ax2.set_xlabel('Resolution')
ax2.set_ylabel('Percentage')
ax2.legend()
st.pyplot(fig2)

top_10_districts = subset_data['Police District'].value_counts().nlargest(10)

st.subheader('Top 10 Police Districts🚓')
fig3, ax3 = plt.subplots()
ax3.barh(top_10_districts.index, top_10_districts.values)
ax3.set_xlabel('Number of Incidents')
ax3.set_ylabel('Police District')
st.pyplot(fig3)

incidents_by_day = subset_data['Day'].value_counts()

st.subheader('Incidents by Day of the Week📅')
fig4, ax4 = plt.subplots()
ax4.pie(incidents_by_day, labels=incidents_by_day.index, autopct='%1.1f%%', startangle=90)
ax4.axis('equal')
st.pyplot(fig4)