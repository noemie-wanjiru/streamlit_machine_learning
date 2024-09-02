import streamlit as st
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

# Load the model and encoder 
@st.cache_resource

def load_preprocessing_pipeline():
    return joblib.load("models/preprocessing_pipeline.joblib")

def load_model():
    model = joblib.load("models/machine_learning_model.joblib")  
    return model



# Function to make predictions
def make_prediction(input_data, model, columns):
    prediction = model.predict(input_data)
    prediction_proba = model.predict_proba(input_data)
    return prediction[0], prediction_proba[0]

def app():
    st.title("Make Predictions")
    
    # Load model
    preprocessing_pipeline = load_preprocessing_pipeline()
    model = load_model()

    # Create input fields based on the features your model needs
    st.write("### Enter the features for prediction:")
       
    
    gender=st.selectbox("Gender",["Male","Female"])
    SeniorCitizen = st.number_input("SeniorCitizen", min_value=0, max_value=1, step=1, value=0)
    Partner = st.selectbox("Partner", ["Yes","No"])
    Dependents = st.selectbox("Dependents", ["Yes","No"])
    PhoneService = st.selectbox("PhoneService", ["Yes","No"])
    MultipleLines = st.selectbox("MultipleLines", ["Yes","No"])
    InternetService = st.selectbox("InternetService", ["DSL", "Fiber optic", "No"])
    OnlineSecurity = st.selectbox("OnlineSecurity", ["Yes","No"])
    OnlineBackup = st.selectbox("OnlineBackup", ["Yes","No"])
    DeviceProtection = st.selectbox("DeviceProtection", ["Yes","No"])
    TechSupport = st.selectbox("TechSupport", ["Yes","No"])
    StreamingTV = st.selectbox("StreamingTV", ["Yes","No"])
    StreamingMovies = st.selectbox("StreamingMovies", ["Yes","No"])
    Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    PaperlessBilling = st.selectbox("PaperlessBilling", ["Yes","No"])
    PaymentMethod = st.selectbox("PaymentMethod", ["Bank transfer (automatic)", "Credit card (automatic)", "Electronic check", "Mailed check"])
    tenure = st.number_input("tenure", min_value=0, max_value=150)

    MonthlyCharges = st.number_input("MonthlyCharges", min_value=0, max_value=50000)
    TotalCharges = st.number_input("TotalCharges", min_value=0, max_value=1000000)


    # Collect the input data into a format your model expects (e.g., list or array)
    input_data = [gender, SeniorCitizen,Partner, Dependents, PhoneService, MultipleLines, InternetService, OnlineSecurity,
            OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod, tenure, MonthlyCharges, TotalCharges]
    
    # Column names from the training data
    columns = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService', 
            'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 
            'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 
            'Contract', 'PaperlessBilling', 'PaymentMethod', 'tenure','MonthlyCharges', 
             'TotalCharges']

    input_data = pd.DataFrame([input_data], columns=columns)
    # When user clicks the button, make predictions
    if st.button("Predict"):

        # Apply the preprocessing pipeline to the input data
        processed_data = preprocessing_pipeline.transform(input_data)

        # Ensure processed_data is 2D (for a single sample)
        
        processed_data = processed_data.reshape(processed_data.shape[0], -1)
         
        prediction, prediction_proba = make_prediction(processed_data, model,columns)
        
        if prediction == 0:
            pred="No"
            prediction_label = "Customer is not likely to Churn"
        else:
            pred="Yes"
            prediction_label = "Customer is likely to Churn"
        # Display results
        st.write(f"### Prediction: {prediction_label}")
        st.write(f"### Prediction Probabilities: {prediction_proba}")
       

        # Store the prediction details
        with open('prediction_history.csv', 'a') as f:
            f.write(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")},{gender}, {SeniorCitizen},{Partner},{ Dependents}, {PhoneService}, {MultipleLines}, {InternetService}, {OnlineSecurity},"
    f"{OnlineBackup}, {DeviceProtection},{ TechSupport}, {StreamingTV}, {StreamingMovies}, {Contract}, {PaperlessBilling}, {PaymentMethod}, {tenure}, {MonthlyCharges}, {TotalCharges},{pred},{prediction_proba}\n")
        
        st.success("Prediction saved to history.")

    # Optionally display the saved predictions
    if st.checkbox("Show Prediction History"):
        try:
            history = pd.read_csv('prediction_history.csv', names=["Timestamp", 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService', 
            'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 
            'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 
            'Contract', 'PaperlessBilling', 'PaymentMethod', 'tenure','MonthlyCharges', 
             'TotalCharges', "Prediction", "Probability"])
            st.write(history)
        except FileNotFoundError:
            st.write("No prediction history found.")
