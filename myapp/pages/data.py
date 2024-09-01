import streamlit as st
import pyodbc
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv(r"C:\Users\user\OneDrive\streamlit_machine_learning\.env")

# Function to connect to SQL Server
def get_data():
    

    # Retrieve the database credentials from environment variables
    driver = os.getenv('DB_DRIVER')
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_DATABASE')
    uid = os.getenv('DB_USER')
    pwd = os.getenv('DB_PASSWORD')

     # Establish the connection
    conn = pyodbc.connect(f'DRIVER={driver};'
                              f'SERVER={server};'
                              f'DATABASE={database};'
                              f'UID={uid};'
                              f'PWD={pwd}')
    
    query = "SELECT TOP 100 * FROM dbo.LP2_Telco_churn_first_3000"  
    data = pd.read_sql(query, conn)
    conn.close()
    return data

def app():
    st.title("Data Preview")

    st.write("### Sample Data from the Database:")
    
    try:
        data = get_data()
        st.dataframe(data.head(10))  # Display the first 10 rows of the data
        
        if st.checkbox('Show Numeric Features'):
            st.write(data.select_dtypes(include=['int', 'float']).head())
        
        if st.checkbox('Show Categorical Features'):
            st.write(data.select_dtypes(include=['object']).head())
    
    except Exception as e:
        st.error(f"Error loading data: {e}")