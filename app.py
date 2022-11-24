import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page

#Sidebar
page = st.sidebar.selectbox("Explorar ou Prever", ("Prever", "Explorar"))

if page == "Prever":
    show_predict_page()
else:
    show_explore_page()