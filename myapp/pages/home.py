import streamlit as st
from PIL import Image
import streamlit_authenticator as stauth
from datetime import datetime


def app():

    # Load your image 
    image = Image.open("images/churn.png")

     # Display the image at full width
    st.image(image, use_column_width=True)
    
    # Display the title below the image
    st.title("Welcome to the Customer Churn Prediction App")
    
    st.markdown("""This app is built to interact with a trained machine learning model (Random Forest Classifier) and predict whether a Customer is likely to Churn. """)

    #Navigation tabs 
    tab1, tab2, tab3, tab4, tab5 =st.tabs(["Home", "Data", "Dashboard", "Predict", "History"])
    with tab1:
        # Content for the Home tab
        st.write("This is the Home page. It provides an overview of the app and links to resources.")
        st.write("The app uses a random classifier model to predict whether a customer is likely to churn")
        st.write("This app is built using Streamlit, a Python library for creating web applications")
        st.write("Below is a link to the machine learning model on github")
        st.markdown("[GitHub](https://github.com/noemie-wanjiru/Customer-churn.git)")
        st.markdown("## **How to use the app**")
        st.write("1. Select the 'Predict' tab")
        st.write("2. Fill in the customer data in the form")
        st.write("3. Click the 'Predict' button to get the prediction")
        st.write("4. The app will display the prediction and prediction probabilities")
        st.write("To look at the prediction history navigate to the prediction page  and select the date")
        

    with tab2:
        # Content for the Data tab
        st.write("This is the Data page. It provides a preview of the dataset used for training.")
        st.write("The dataset used in this app from a database provided by Azubi Africa")
        st.write("This dataset includes features such as customer demographics, service usage, and payment history.")
    
    with tab3:
        # Content for the Dashboard tab
        st.write("This is the Dashboard page. It contains interactive data visualizations and KPIs for the data")

    with tab4:
        # Content for the Predict tab
        st.write("This is the Predict page. It allows users to input their customer data and make predictions.")

    with tab5:
        # Content for the History tab
        st.write("This is the History page. It displays past predictions made by users.")
   
