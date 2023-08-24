"""
LUMEN - Inventory Management System (IMS) Streamlit Application

This Streamlit application is designed for managing an inventory system. It includes features for viewing inventory,
adding and removing items, and displaying information about the application. The application is organized into pages
accessible via a navigation menu.

Author: Kevin Freire
Date: August 23, 2023
"""

import sys

import streamlit as st
from streamlit_option_menu import option_menu

sys.path.append("src/")
from src import mongodb, pages, schemas

st.set_page_config(
    layout="wide",
    page_title="LUMEN - IMS",
    page_icon="https://static.thenounproject.com/png/145436-200.png",
)
st.markdown(schemas.page_bg_img, unsafe_allow_html=True)
inventory_db = mongodb.MongoIMS(st.secrets.mongodb)

if __name__ == "__main__":
    selected = option_menu(
        None,
        ["Home", "Chat Bot", "Port Manager", "Inventory"],
        icons=["house", "robot", "gear", "archive"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if selected == "Home":
        pages.home_page()

    if selected == "Inventory":
        pages.inventory_page(inventory_db)
