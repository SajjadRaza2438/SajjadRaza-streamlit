# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 17:55:00 2023

@author: Home PC
"""

import pandas as pd
import numpy as np
import streamlit as st
st.set_page_config(layout="wide")


st.title('Olympic History Dashboard')
st.subheader('Syed Sajjad Raza')


# Load data into a pandas dataframe
df = pd.read_csv("C:\\Users\Home PC\\AppData\Roaming\\Python\\Python39\\Scripts\\athlete_events.csv")

# Check for missing values in each column
print(df.isna().sum())

# Fill missing values in the "Age", "Height", and "Weight" columns with the mean value
df["Age"].fillna(df["Age"].mean(), inplace=True)
df["Height"].fillna(df["Height"].mean(), inplace=True)
df["Weight"].fillna(df["Weight"].mean(), inplace=True)

# Confirm that there are no more missing values in the data
print(df.isna().any())
   
df["Medal"].fillna("No Medal", inplace=True)
print(df.head())
print(df.isna().any())
print(df.isna().sum())



# Create a dropdown widget to select the country

all_countries = sorted(df['Team'].unique())
selected_country = st.selectbox('Select Your Country', all_countries)

# Filter the data based on the selected country
filtered_data = df[df["Team"] == selected_country]

# Count the number of participations for the selected country
participations = filtered_data["Team"].count()

# Count the number of gold medals for the selected country
gold_medals = filtered_data[filtered_data["Medal"] == "Gold"]["Medal"].count()

# Count the number of silver medals for the selected country
silver_medals = filtered_data[filtered_data["Medal"] == "Silver"]["Medal"].count()

# Count the number of bronze medals for the selected country
bronze_medals = filtered_data[filtered_data["Medal"] == "Bronze"]["Medal"].count()


# display the number of participations, gold medals, silver medals, and bronze medals using the `st.metrics()` function
col1, col2, col3, col4= st.columns(4)
col1.metric('Participations', participations)
col2.metric('Gold Medals', gold_medals)
col3.metric('Silver Medals', silver_medals)
col4.metric('Bronze Medals', bronze_medals)


st.set_option('deprecation.showPyplotGlobalUse', False)

with st.container():
    
    line, hbar, table = st.columns(3)
    
    
    
 
    line.header('Number of Medals over Years For Each Medal Type (G,S,B)')
    
   
    # Filter the data to only include gold, silver, and bronze medals
    medal_data = filtered_data[filtered_data["Medal"].isin(['Gold', 'Silver', 'Bronze'])]
    # Create the line chart
    sns.lineplot(x='Year', y='Medal', hue='Medal', data=medal_data)
    line.pyplot()
    

    hbar.header("Top 5 Athletes by Number of Medals Received")

    # Create a horizontal bar chart
    athlete_medal_count = filtered_data.groupby(["Name"]).Medal.count().reset_index()
    athlete_medal_count = athlete_medal_count.sort_values("Medal", ascending=False).head(5)
    sns.barplot(x='Medal', y='Name', data=athlete_medal_count)
    hbar.pyplot()
    
    table.header("Top 5 Sports by Number of Medals Received")
    sport_medal_count = filtered_data.groupby(["Sport"]).Medal.count().reset_index()
    sport_medal_count = sport_medal_count.sort_values("Medal", ascending=False).head(5)
    # st.dataframe(sport_medal_count)
    
   # Modify the width of the table column
    with table:
        st.dataframe(sport_medal_count, height=200, width=400)

    


with st.container():
    hist, pie, vbar = st.columns(3)

    hist.header("Number of Medals over Age Histogram Chart, 10 Years Bins")

    # Create a histogram chart
    filtered_data['Age'] = filtered_data['Age'].astype(int)
    sns.histplot(x='Age', data=filtered_data, bins=10)
    hist.pyplot()

    pie.header("Pie Chart Summary by Number of Medals bifurcated by Gender")


    # Plot a pie chart
    gender_medal_count = filtered_data.groupby(["Sex"]).Medal.count().reset_index()
    plt.pie(gender_medal_count["Medal"], labels=gender_medal_count["Sex"], autopct='%1.1f%%')
    pie.pyplot()


    vbar.header("Vertical Bar Chart by # of Medals Received in each Season")

    # Create a vertical bar chart
    season_medal_count = filtered_data.groupby(["Season"]).Medal.count().reset_index()
    sns.barplot(x='Season', y='Medal', data=season_medal_count)
    vbar.pyplot()











