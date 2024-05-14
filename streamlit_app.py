import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Define mappings for your specific variables
sex_mapping = {1: 'Male', 2: 'Female'}
income_mapping = {11: "40,000 To 49,999", 15: "100,000 To 149,999", 6: "15,000 To 19,999", 16: "150,000 or More",
                  2: "5,000 To 7,499", 1: "Less Than $5,000", 13: "60,000 To 74,999", 5: "12,500 To 14,999",
                  14: "75,000 To 99,999", 3: "7,500 To 9,999", 8: "25,000 To 29,999", 9: "30,000 To 34,999",
                  7: "20,000 To 24,999", 10: "35,000 To 39,999", 12: "50,000 To 59,999", 4: "10,000 To 12,499"}
marital_status_mapping = {7: "Never married", 5: "Divorced", 2: "Married, Armed Forces Spouse Present",
                          1: "Married, Civilian Spouse Present", -1: "In Universe, Met No Conditions To Assign",
                          4: "Widowed", 3: "Married, Spouse Absent (exc. Separated)", 6: "Separated"}
state_mapping = {1: 'Alabama', 2: 'Alaska', 4: 'Arizona', 5: 'Arkansas', 6: 'California', 8: 'Colorado', 9: 'Connecticut',
                 10: 'Delaware', 11: 'District of Columbia', 12: 'Florida', 13: 'Georgia', 15: 'Hawaii', 16: 'Idaho',
                 17: 'Illinois', 18: 'Indiana', 19: 'Iowa', 20: 'Kansas', 21: 'Kentucky', 22: 'Louisiana', 23: 'Maine',
                 24: 'Maryland', 25: 'Massachusetts', 26: 'Michigan', 27: 'Minnesota', 28: 'Mississippi', 29: 'Missouri',
                 30: 'Montana', 31: 'Nebraska', 32: 'Nevada', 33: 'New Hampshire', 34: 'New Jersey', 35: 'New Mexico',
                 36: 'New York', 37: 'North Carolina', 38: 'North Dakota', 39: 'Ohio', 40: 'Oklahoma', 41: 'Oregon',
                 42: 'Pennsylvania', 44: 'Rhode Island', 45: 'South Carolina', 46: 'South Dakota', 47: 'Tennessee',
                 48: 'Texas', 49: 'Utah', 50: 'Vermont', 51: 'Virginia', 53: 'Washington', 54: 'West Virginia',
                 55: 'Wisconsin', 56: 'Wyoming'}

# Function to load data from a local file
def load_data():
    df = pd.read_csv('USdatSt.csv')
    df.dropna(inplace=True)  # Ensuring no missing values
    df['PESEX'] = df['PESEX'].map(sex_mapping)
    df['HEFAMINC'] = df['HEFAMINC'].map(income_mapping)
    df['PRMARSTA'] = df['PRMARSTA'].map(marital_status_mapping)
    if 'ST' in df.columns:
        df['ST'] = df['ST'].map(state_mapping)
    return df

# Check if data is already loaded, if not load it
if 'data' not in st.session_state:
    st.session_state.data = load_data()
data = st.session_state.data

# Streamlit interface
st.title('CPS Data Analysis Dashboard')

if not data.empty:
    # Sidebar for user inputs and filters
    st.sidebar.header("Filter Data")
    gender_to_filter = st.sidebar.multiselect('Select Gender:', options=data['PESEX'].dropna().unique())
    income_to_filter = st.sidebar.multiselect('Select Income Range:', options=data['HEFAMINC'].dropna().unique())
    marital_status_to_filter = st.sidebar.multiselect('Select Marital Status:', options=data['PRMARSTA'].dropna().unique())
    if 'ST' in data.columns:
        state_to_filter = st.sidebar.multiselect('Select State:', options=data['ST'].dropna().unique())
    else:
        state_to_filter = []

    # Applying filters
    if gender_to_filter:
        data = data[data['PESEX'].isin(gender_to_filter)]
    if income_to_filter:
        data = data[data['HEFAMINC'].isin(income_to_filter)]
    if marital_status_to_filter:
        data = data[data['PRMARSTA'].isin(marital_status_to_filter)]
    if 'ST' in data.columns and state_to_filter:
        data = data[data['ST'].isin(state_to_filter)]

    # Displaying data and statistics

    # Plots
    st.write("### Gender Distribution")
    fig, ax = plt.subplots(figsize=(8, 6))
    data['PESEX'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['skyblue', 'lightcoral'], ax=ax)
    plt.title('Gender Distribution')
    plt.ylabel('')
    st.pyplot(fig)

    st.write("### Income Range Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data['HEFAMINC'], bins=len(data['HEFAMINC'].unique()), color='lightgreen', ax=ax, kde=True)
    plt.title('Income Range Distribution')
    plt.xlabel('Income Range')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.write("### Marital Status Breakdown")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(y='PRMARSTA', data=data, palette='husl', ax=ax)
    plt.title('Marital Status Breakdown')
    plt.xlabel('Frequency')
    plt.ylabel('Marital Status')
    st.pyplot(fig)

    # Compare distributions
    st.write("### Income Range by Gender")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.violinplot(x='HEFAMINC', y='PESEX', data=data, split=True, inner="quart", palette='pastel', ax=ax)
    plt.title('Income Range by Gender')
    plt.xlabel('Income Range')
    plt.ylabel('Gender')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.write("### Marital Status by Gender")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pd.crosstab(data['PESEX'], data['PRMARSTA']), annot=True, fmt='d', cmap='YlGnBu', ax=ax)
    plt.title('Marital Status by Gender')
    plt.xlabel('Marital Status')
    plt.ylabel('Gender')
    st.pyplot(fig)

    # Additional analyses
    st.write("### Income Range by Marital Status")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='HEFAMINC', y='PRMARSTA', data=data, palette='Set3', ax=ax)
    plt.title('Income Range by Marital Status')
    plt.xlabel('Income Range')
    plt.ylabel('Marital Status')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Heatmap analysis
    st.write("### Heatmap of Gender and Marital Status")
    heatmap_data = pd.crosstab(data['PESEX'], data['PRMARSTA'])
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
    plt.title('Heatmap of Gender and Marital Status')
    plt.xlabel('Marital Status')
    plt.ylabel('Gender')
    st.pyplot(fig)

    # Descriptive statistics
    st.write("### Summary Statistics")
    st.write(data.describe(include='all'))
