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

    # Additional analyses
    if 'ST' in filtered_data.columns:
        st.write("### Gender Distribution by State")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(x='ST', hue='PESEX', data=filtered_data, ax=ax)
        plt.title('Gender Distribution by State')
        plt.xlabel('State')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.legend(title='Gender', loc='upper right')
        st.pyplot(fig)

    corr = filtered_data.corr()
    st.write("### Correlation Matrix")
    st.write(corr)

    # Plot correlation heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    plt.title('Correlation Heatmap')
    st.pyplot(fig)

    st.write("### Income Distribution by Gender and Age Group")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='HEFAMINC', hue='PESEX', data=filtered_data, hue_order=['Male', 'Female'], col='age_group', ax=ax)
    plt.title('Income Distribution by Gender and Age Group')
    plt.xlabel('Income Range')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.legend(title='Gender', loc='upper right')
    st.pyplot(fig)

    if 'ST' in filtered_data.columns:
        st.write("### Income Distribution by State")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(x='ST', hue='HEFAMINC', data=filtered_data, ax=ax)
        plt.title('Income Distribution by State')
        plt.xlabel('State')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.legend(title='Income Range', loc='upper right')
        st.pyplot(fig)')
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
    age_to_filter = st.sidebar.slider('Select Age Range:', int(data['AGE'].min()), int(data['AGE'].max()), (18, 65))
    if 'ST' in data.columns:
        state_to_filter = st.sidebar.multiselect('Select State:', options=data['ST'].dropna().unique())
    else:
        state_to_filter = []

    # Applying filters
    filtered_data = data.copy()
    if gender_to_filter:
        filtered_data = filtered_data[filtered_data['PESEX'].isin(gender_to_filter)]
    if income_to_filter:
        filtered_data = filtered_data[filtered_data['HEFAMINC'].isin(income_to_filter)]
    if marital_status_to_filter:
        filtered_data = filtered_data[filtered_data['PRMARSTA'].isin(marital_status_to_filter)]
    filtered_data = filtered_data[(filtered_data['AGE'] >= age_to_filter[0]) & (filtered_data['AGE'] <= age_to_filter[1])]
    if 'ST' in filtered_data.columns and state_to_filter:
        filtered_data = filtered_data[filtered_data['ST'].isin(state_to_filter)]

    # Displaying data and statistics
    st.write("### Summary Statistics")
    st.write(filtered_data.describe(include='all'))

    # Plots
    st.write("### Age Distribution")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(data=filtered_data, x='AGE', kde=True, ax=ax)
    plt.title('Age Distribution')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    st.pyplot(fig)

    st.write("### Income Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='HEFAMINC', data=filtered_data, ax=ax)
    plt.title('Income Distribution')
    plt.xlabel('Income Range')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Compare distributions
    st.write("### Compare Income Distribution by Age Group")
    age_bins = [18, 30, 45, 60, 90]
    labels = ['18-29', '30-44', '45-59', '60+']
    filtered_data['age_group'] = pd.cut(filtered_data['AGE'], bins=age_bins, labels=labels, include_lowest=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='HEFAMINC', hue='age_group', data=filtered_data, ax=ax)
    plt.title('Income Distribution by Age Group')
    plt.xlabel('Income Range')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.legend(title='Age Group', loc='upper right')
    st.pyplot(fig)

    st.write("### Compare Marital Status Distribution by Income Range")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='PRMARSTA', hue='HEFAMINC', data=filtered_data, ax=ax)
    plt.title('Marital Status Distribution by Income Range')
    plt.xlabel('Marital Status')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.legend(title='Income Range', loc='upper right')
    st.pyplot(fig)

    # Additional analyses
    if 'ST' in filtered_data.columns:
        st.write("### Gender Distribution by State")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(x='ST', hue='PESEX', data=filtered_data, ax=ax)
        plt.title('Gender Distribution by State')
        plt.xlabel('State')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.legend(title='Gender', loc='upper right')
        st.pyplot(fig)

    corr = filtered_data.corr()
    st.write("### Correlation Matrix")
    st.write(corr)

    # Plot correlation heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    plt.title('Correlation Heatmap')
    st.pyplot(fig)

    st.write("### Income Distribution by Gender and Age Group")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='HEFAMINC', hue='PESEX', data=filtered_data, hue_order=['Male', 'Female'], col='age_group', ax=ax)
    plt.title('Income Distribution by Gender and Age Group')
    plt.xlabel('Income Range')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.legend(title='Gender', loc='upper right')
    st.pyplot(fig)

    if 'ST' in filtered_data.columns:
        st.write("### Income Distribution by State")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(x='ST', hue='HEFAMINC', data=filtered_data, ax=ax)
        plt.title('Income Distribution by State')
        plt.xlabel('State')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.legend(title='Income Range', loc='upper right')
        st.pyplot(fig)
