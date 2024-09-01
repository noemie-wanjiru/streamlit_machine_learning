import streamlit as st
import pandas as pd
from datetime import datetime

# Function to load prediction history from a CSV file
def load_history():
    try:
       
        
        # Adjust column names based on your stored data structure
        history = pd.read_csv('prediction_history.csv',names=["Timestamp", 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService', 
            'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 
            'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 
            'Contract', 'PaperlessBilling', 'PaymentMethod', 'tenure','MonthlyCharges', 
             'TotalCharges', "Prediction", "Probabilities"])
        return history
    except FileNotFoundError:
        return pd.DataFrame(columns=["Timestamp", 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService', 
            'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 
            'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 
            'Contract', 'PaperlessBilling', 'PaymentMethod', 'tenure','MonthlyCharges', 
             'TotalCharges', "Prediction", "Probabilities"])

def app():
    st.title("Prediction History")
    
    # Load the history
    history = load_history()
    
    if not history.empty:
        # Display the history dataframe
        st.write("### Past Predictions")
        st.dataframe(history)
        
        # Optionally provide filters
        filter_by_date = st.date_input("Filter by Date", value=None)
        if filter_by_date:
            history["Timestamp"] = pd.to_datetime(history["Timestamp"])
            filtered_history = history[history["Timestamp"].dt.date == filter_by_date]
            st.write("### Filtered Predictions")
            st.dataframe(filtered_history)
            
        # Optionally allow the user to clear history
        if st.button("Clear History"):
            with open('prediction_history.csv', 'w') as f:
                f.write("")  # Clearing the file
            st.success("Prediction history cleared.")
    else:
        st.write("No prediction history available.")
