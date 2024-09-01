import streamlit as st
from pages import home, data, dashboard, predict, history

PAGES ={
    "Home": home,
    "Data": data,
    "Dashboard": dashboard,
    "Predict": predict,
    "History": history
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    
# Display the selected page
page = PAGES[selection]
page.app()





