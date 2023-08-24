"""
Streamlit Web Application for Inventory Management

This script defines a Streamlit web application with two main pages: the "Inventory Page" and the "Home Page".
The application is designed to manage inventory data, allowing users to view items, enter new sites,
add and remove items, and provides information about the application.

Author: Kevin Freire
Date: August 23, 2023
"""

import streamlit as st

from src.utils import (
    add_item_by_option,
    extract_and_insert_site_details,
    remove_item_by_option,
    set_index_with_exception_handling,
)


def inventory_page(db):
    """
    Display the Inventory Management System page.

    Args:
        db (MongoIMS): An instance of the MongoIMS class for managing inventory data.

    This page allows users to:
    - View items for a selected site, including fiber, optics, and miscellaneous items.
    - Enter details for a new site.
    - Add new items to the inventory.
    - Remove items from the inventory.
    """
    st.title("Inventory Management System")
    radio_option = st.sidebar.radio(
        "Menu", options=["View Items", "Enter new site", "Add Items", "Remove Items"]
    )

    if radio_option == "View Items":
        st.subheader("View Items")
        cili = st.selectbox("Select Site", db.get_cilis())
        fiber, optic, misc = db.get_inventory_from_cili(cili)
        st.write("### Fiber Inventory")
        st.dataframe(set_index_with_exception_handling(fiber, 0))
        st.write("### Optics Inventory")
        st.dataframe(set_index_with_exception_handling(optic, 0))
        st.write("### Misc Inventory")
        st.dataframe(set_index_with_exception_handling(misc, 0))

    if radio_option == "Enter new site":
        st.subheader("Enter Site details")
        extract_and_insert_site_details(db)

    if radio_option == "Add Items":
        st.subheader("Add New Items")
        cili = st.selectbox("Select Site", db.get_cilis())
        option = st.radio("Select Item to add: ", ("Fiber", "Optic", "Misc"))
        add_item_by_option(db, option, cili)

    if radio_option == "Remove Items":
        st.subheader("Remove Items")
        cili = st.selectbox("Select Site", db.get_cilis())
        option = st.radio("Select Item to remove: ", ("Fiber", "Optic", "Misc"))
        remove_item_by_option(db, option, cili)


def home_page():
    """
    Display the Home page with information about the application.

    This page provides information about the purpose of the application and mentions plans for future work.
    """
    st.title("Home")
    st.subheader("About")
    st.write(
        """
            This web application is intended to keep track of consumable materials that Field Technicians
            commonly use in their day to day.  It is only intended to track their fiber inventory, network
            optics and other materials such as items for label maker or office supplies.  
    """
    )
    st.subheader("Future Work")
    st.write(
        """
            In the future their are plans to implement a chatbot allowing technicians to be 
            able to chat with any PDF documents such as manuals to allow technicains to 
            troubleshoot equipment more efficiently. In addition implementign another database that
            allows technician track port assignment within the data centers.
    """
    )
