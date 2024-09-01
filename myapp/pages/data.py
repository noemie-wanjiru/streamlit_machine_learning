import streamlit as st
import pyodbc
import pandas as pd
from dotenv import load_dotenv
import os



# Function to connect to SQL Server
def get_data():
    


    conn = pyodbc.connect(r'DRIVER={SQL Server};'
                          r'SERVER=dap-projects-database.database.windows.net;'
                          r'DATABASE=dapDB;'
                          r'UID=LP2_project;'
                          r'PWD=Stat$AndD@t@Rul3')
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
