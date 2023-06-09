#Input the relevant libraries
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from PIL import Image

df = pd.DataFrame()
year = ''

def filterBy(df, campus):
    filtered_df = df[df['Campus'] == campus]  
    return filtered_df

def filterByYear(df, year):
    filtered_df = df[df['Year Graduated'] == year]  
    new_df = pd.DataFrame(filtered_df)
    new_df = new_df.copy().reset_index(drop=True)
    return new_df
    
def loadcsvfile():
    csvfile = 'graduate-tracer.csv'
    df = pd.read_csv(csvfile, dtype='str', header=0, sep = ",", encoding='latin') 
    return df

def createPlots(df, columnName):
    st.write('Graduates Distribution by ' + columnName)
    scounts=df[columnName].value_counts()
    labels = list(scounts.index)
    sizes = list(scounts.values)
    custom_colors = ['tomato', 'cornflowerblue', 'gold', 'orchid', 'green']
    fig = plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.pie(sizes, labels = labels, textprops={'fontsize': 10}, startangle=140, \
            autopct='%1.0f%%', colors=sns.color_palette('Set2'))
    plt.subplot(1, 2, 2)
    p = sns.barplot(x = scounts.index, y = scounts.values, palette= 'viridis')
    plt.setp(p.get_xticklabels(), rotation=90)
    st.pyplot(fig)

    # get value counts and percentages of unique values in column 
    value_counts = df[columnName].value_counts(normalize=True)
    value_counts = value_counts.mul(100).round(2).astype(str) + '%'
    value_counts.name = 'Percentage'

    # combine counts and percentages into a dataframe
    result = pd.concat([df[columnName].value_counts(), value_counts], axis=1)
    result.columns = ['Counts', 'Percentage']
    st.write(pd.DataFrame(result))
    
    return

def createTable(df, columnName):  
    st.write('Graduate Distribution by ' + columnName)
    # get value counts and percentages of unique values in column 
    value_counts = df[columnName].value_counts(normalize=True)
    value_counts = value_counts.mul(100).round(2).astype(str) + '%'
    value_counts.name = 'Percentage'

    # combine counts and percentages into a dataframe
    result = pd.concat([df[columnName].value_counts(), value_counts], axis=1)
    result.columns = ['Counts', 'Percentage']
    st.write(pd.DataFrame(result))
    
    return

def twowayPlot(df, var1, var2):
    fig = plt.figure(figsize =(10, 3))
    p = sns.countplot(x=var1, data = df, hue=var2, palette='bright')
    _ = plt.setp(p.get_xticklabels(), rotation=90) 
    st.pyplot(fig)

# Define the Streamlit app
def app():
    st.title("Welcome to the 2023 WVSU Graduate Tracer Report")      
    st.subheader("(c) WVSU Management Information System")
                 
    st.write("This dashboard is managed by: Dr. Nancy S. Surmieda \nDirector, Office of Student Affairs, osa@wvsu.edu.ph")
                 
    st.write("The employability of university graduates can vary depending on a variety of factors, such as their field of study, their level of academic achievement, their relevant work experience, their soft skills, and the current state of the job market.")

    st.write("The current dataset is taken from the WVSU Graduate Tracer Study as of May 5, 2023.")
    st.subheader("Graduate Employability Report")
    df = loadcsvfile()

    year = '2016'
    options=df['Year Graduated'].unique()
    
    year = st.selectbox('Select the year', options)
    if year=='2016':   
        df = filterByYear(df, year)
        st.write('Selected year is ' + year)
        createPlots(df, 'Campus')
    else:
        df = filterByYear(df, year)
        st.write('Selected year is ' + year)
        createPlots(df, 'Campus')
    
    
    st.write('Filter graduates by campus')
    #The main campus is selected by default
    campus = 'Main Campus'
    options=df['Campus'].unique()
    campus = st.selectbox('Select the campus', options)
    if campus=='Main Campus':
        df = filterBy(df, campus)
    else:
        df = filterBy(df, campus)
        
    if st.button('Distribution By Sex'):
        df = filterBy(df, campus)
        createPlots(df, 'Sex')

    
    if st.button('Distribution By Civil Status'):
        df = filterBy(df, campus)  
        createPlots(df, 'Civil Status')

    if st.button('Distribution By College'):
        df = filterBy(df, campus)  
        createPlots(df, 'College')

    if st.button('Distribution By Province'):
        df = filterBy(df, campus)  
        createTable(df, 'Province of Origin')
        
    if st.button('Distribution By Location of Residence'):
        df = filterBy(df, campus)  
        createTable(df, 'Location of Residence')
        
    if st.button('Distribution By Employment Status'):
        df = filterBy(df, campus)  
        createTable(df, 'Employment Status')
    

#run the app
if __name__ == "__main__":
    app()
