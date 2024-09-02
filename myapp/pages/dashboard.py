import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pyodbc
from PIL import Image
from dotenv import load_dotenv
import os


# Function to connect to SQL Server and retrieve data
def get_data():

    conn = pyodbc.connect(r'DRIVER={SQL Server};'
                          r'SERVER=dap-projects-database.database.windows.net;'
                          r'DATABASE=dapDB;'
                          r'UID=LP2_project;'
                          r'PWD=Stat$AndD@t@Rul3')

    
    query = "SELECT * FROM dbo.LP2_Telco_churn_first_3000"  # Adjust the query to fit your data
    data = pd.read_sql(query, conn)
    conn.close()
    return data

def app():
        # Load your image 
    image =Image.open("images\kpi.jpeg")

    st.image(image, use_column_width=True)
    
    st.title("Dashboard")
  
    
    # Tabs for EDA and KPI Dashboards
    tab1, tab2 = st.tabs(["EDA Dashboard", "KPI Dashboard"])
    
    # Load data from SQL
    try:
        data = get_data()
        
        # EDA Dashboard
        with tab1:
            st.subheader("Exploratory Data Analysis")
            
            # Distribution of numerical columns
            st.write("### Numeric Feature Distributions")
            numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
            selected_column = st.selectbox("Select a Numeric Column", numeric_columns)
            if selected_column:
                fig = px.histogram(data, x=selected_column, nbins=50)
                st.plotly_chart(fig)
            
            # Correlation heatmap
            if st.checkbox('Show Correlation Heatmap'):
                st.write("### Correlation Heatmap")
                correlation = data.corr(numeric_only=True)
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax)
                st.pyplot(fig)
        
        # KPI Dashboard
        with tab2:
            st.subheader("Key Performance Indicators (KPIs)")
            

            # KPI Calculations
            total_customers = len(data)
            churn_rate = data['Churn'].value_counts(normalize=True).get(True, 0) * 100
            avg_monthly_charges = data['MonthlyCharges'].mean()
            avg_total_charges = data['TotalCharges'].mean()

            # KPI Display
            st.header('Key Performance Indicators')

            st.metric(label='Total Number of Customers', value=total_customers)
            st.metric(label='Churn Rate (%)', value=f'{churn_rate:.2f}%')
            st.metric(label='Average Monthly Charges', value=f'${avg_monthly_charges:.2f}')
            st.metric(label='Average Total Charges', value=f'${avg_total_charges:.2f}')

            # Additional Analysis
            st.header('Customer Tenure Distribution')
            st.bar_chart(data['tenure'].value_counts().sort_index())

            st.header('Service Subscription Counts')

            # Count of different Internet Services
            internet_service_counts = data['InternetService'].value_counts()
            st.subheader('Internet Service Types')
            st.bar_chart(internet_service_counts)

            # Count of different Payment Methods
            payment_method_counts = data['PaymentMethod'].value_counts()
            st.subheader('Payment Methods')
            st.bar_chart(payment_method_counts)

            # Count of Churn by Gender
            churn_by_gender = data.groupby('gender')['Churn'].value_counts().unstack().fillna(0)
            st.subheader('Churn by Gender')
            st.bar_chart(churn_by_gender)
             
    except Exception as e:
        st.error(f"Error loading data: {e}")
