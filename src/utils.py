"""
Inventory Management Functions and User Interface

This script contains various functions for managing inventory data in a MongoDB database and a Streamlit-based user interface.
It provides functions for checking connectors, removing columns from DataFrames, setting DataFrame indices, converting database
collections to DataFrames, inserting, updating, and generating dictionary items. It also defines functions to get details for
different inventory categories and to add or remove items from the inventory.

Author: Kevin Freire
Date: August 23, 2023
"""

import pandas as pd
import pymongo
import streamlit as st

from src.schemas import fiber_schema, misc_schema, optic_schema, site_schema


def check_connectors(con_1, con_2):
    """
    Check and possibly swap connector values to ensure 'LC' is always in con_1.

    Args:
        con_1 (str): Connector 1 type.
        con_2 (str): Connector 2 type.

    Returns:
        tuple: A tuple containing the possibly swapped connector values.
    """
    if con_1 != "LC":
        tmp = con_1
        con_1 = con_2
        con_2 = tmp
    return con_1, con_2


def remove_columns(df, cols):
    """
    Remove specified columns from a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to modify.
        cols (list): A list of column names to remove.

    Returns:
        pd.DataFrame: The modified DataFrame with specified columns removed.
    """
    try:
        df = df.drop(columns=cols)
    except KeyError as e:
        print(f"Error: Column '{cols}' not found in the DataFrame.")
    return df


def set_index_with_exception_handling(df, index):
    """
    Set the index of a DataFrame to the specified column with exception handling.

    Args:
        df (pd.DataFrame): The DataFrame to modify.
        index (int): The index of the column to set as the DataFrame index.

    Returns:
        pd.DataFrame: The modified DataFrame with the specified index.
    """
    try:
        df = df.set_index(df.columns[index])
    except IndexError as e:
        print("Error: The DataFrame is empty and cannot be set as an index.")
    return df


def convert_to_dataframe(_collection, data):
    """
    Convert a MongoDB collection to a Pandas DataFrame.

    Args:
        _collection: The MongoDB collection to convert.
        data (dict): The query parameters for the MongoDB find operation.

    Returns:
        pd.DataFrame: A DataFrame containing the retrieved data from the MongoDB collection.
    """
    return pd.DataFrame(list(_collection.find(data)))


def insert_data(collection, category, data):
    """
    Insert data into a MongoDB collection based on the specified category.

    Args:
        collection: The MongoDB collection to insert data into.
        category (str): The category of the item to insert.
        data (dict): The data to insert into the collection.

    Note:
        This function validates the data against the corresponding schema for the given category.
    """
    if category == "site":
        if set(data.keys()) == set(site_schema.keys()):
            if all(isinstance(data[field], site_schema[field]) for field in data):
                try:
                    collection.insert_one(data)
                except pymongo.errors.DuplicateKeyError:
                    print("Site already exists. Skipping insertion.")
            else:
                print("Invalid data types for Site schema.")
        else:
            print("Invalid data structure for electronics schema.")
    elif category == "fiber":
        if set(data.keys()) == set(fiber_schema.keys()):
            if all(isinstance(data[field], fiber_schema[field]) for field in data):
                collection.insert_one(data)
            else:
                print("Invalid data types for fiber schema.")
        else:
            print("Invalid data structure for fiber schema.")

    elif category == "optic":
        if set(data.keys()) == set(optic_schema.keys()):
            if all(isinstance(data[field], optic_schema[field]) for field in data):
                collection.insert_one(data)
            else:
                print("Invalid data types for fiber schema.")
        else:
            print("Invalid data structure for fiber schema.")
    elif category == "misc":
        if set(data.keys()) == set(misc_schema.keys()):
            if all(isinstance(data[field], misc_schema[field]) for field in data):
                collection.insert_one(data)
            else:
                print("Invalid data types for clothing schema.")
        else:
            print("Invalid data structure for clothing schema.")
    else:
        print("Unknown category.")


def update_data_quantity(collection, category, new_quantity, data):
    """
    Update the quantity of an item in a MongoDB collection based on the specified category.

    Args:
        collection: The MongoDB collection to update.
        category (str): The category of the item to update.
        new_quantity (int): The new quantity value.
        data (dict): The data used to identify the item for updating.
    """
    if category == "fiber":
        collection.update_one(data, {"$set": {"quantity": new_quantity}})
    elif category == "optic":
        collection.update_one(data, {"$set": {"quantity": new_quantity}})
    elif category == "misc":
        collection.update_one(data, {"$set": {"quantity": new_quantity}})


def generate_dict_item(category, *args):
    """
    Generate a dictionary item based on the specified category and input arguments.

    Args:
        category (str): The category of the item to generate.
        *args: Variable-length arguments representing item attributes.

    Returns:
        dict: A dictionary representing the item with keys based on the category schema.
    """
    if category == "site":
        fill_items = [
            "cili",
            "address",
            "city",
            "state",
            "country",
            "zip_code",
            "site_id",
        ]
        try:
            dict_item = {fill_items[i]: args[i] for i in range(len(fill_items))}
            return dict_item
        except Exception as e:
            print("An error occurred:", str(e))
    elif category == "fiber":
        fill_items = [
            "cordage",
            "type",
            "conn1",
            "conn2",
            "length",
            "quantity",
            "site_cili",
        ]
        try:
            dict_item = {fill_items[i]: args[i] for i in range(len(fill_items))}
            return dict_item
        except Exception as e:
            print("An error occurred:", str(e))
    elif category == "optic":
        fill_items = [
            "make",
            "broadband",
            "wavelength",
            "distance",
            "type",
            "part_number",
            "quantity",
            "site_cili",
        ]
        try:
            dict_item = {fill_items[i]: args[i] for i in range(len(fill_items))}
            return dict_item
        except Exception as e:
            print("An error occurred:", str(e))
    elif category == "misc":
        fill_items = ["brand", "item", "quantity", "site_cili"]
        try:
            dict_item = {fill_items[i]: args[i] for i in range(len(fill_items))}
            return dict_item
        except Exception as e:
            print("An error occurred:", str(e))


def get_site_details():
    """
    Get user input for Site details.

    Returns:
        tuple: A tuple containing the following details:
        - cili (str): The CILI (Common Installation Location Identifier) value of the site.
        - address (str): The address of the site.
        - city (str): The city where the site is located.
        - state (str): The state or province where the site is located.
        - country (str): The country where the site is located.
        - zip_code (str): The ZIP code or postal code of the site.
        - site_id (str): A unique identifier for the site.
    """
    cili = st.text_input("Enter site CILI: ").upper()
    address = st.text_input("Enter site Address: ").upper()
    city = st.text_input("City: ").upper()
    state = st.text_input("State: ").upper()
    country = st.text_input("Country: ").upper()
    zip_code = st.text_input("Zip Code: ").upper()
    site_id = st.text_input("Site ID: ").upper()
    return cili, address, city, state, country, zip_code, site_id


def get_fiber_details():
    """
    Get user input for Fiber inventory item details.

    Returns:
        tuple: A tuple containing the following details:
        - cordage (str): Fiber cordage type (e.g., "SIMPLEX", "DUPLEX").
        - type_ (str): Fiber type (e.g., "SMF", "MMF").
        - con_1 (str): Connector 1 type (e.g., "LC", "SC").
        - con_2 (str): Connector 2 type (e.g., "LC", "SC").
        - length (str): Length of the fiber (Meters or Feet).
        - qty (str): Quantity of the fiber.
    """
    cordage = st.selectbox("Select Fiber cordage Type", ["SIMPLEX", "DUPLEX"])
    type_ = st.selectbox("Select Fiber Type", ["SMF", "MMF"])
    con_1 = st.selectbox("Select Connector 1", ["LC", "SC"])
    con_2 = st.selectbox("Select Connector 2", ["LC", "SC"])
    length = st.text_input("Enter length (M/FT): ").upper()
    qty = st.text_input("Enter quantity: ")
    return cordage, type_, con_1, con_2, length, qty


def get_optic_details():
    """
    Get user input for Optic inventory item details.

    Returns:
        tuple: A tuple containing the following details:
        - make (str): Manufacturer of the optic.
        - broadband (str): Broadband speed of the optic.
        - wavelength (str): Wavelength in nanometers (e.g., "1310", "1550").
        - range_ (str): Range of the optic.
        - fiber_type (str): Fiber type (e.g., "SMF", "MMF").
        - part_number (str): Part number of the optic.
        - qty (str): Quantity of the optic.
    """
    make = st.text_input("Enter Manufacturer: ").upper()
    broadband = st.text_input("Enter Boradband Speed: ").upper()
    wavelength = st.selectbox("Select wavelength (nm)", ["1310", "1550"])
    range_ = st.text_input("Enter Range: ").upper()
    fiber_type = st.selectbox("Select Fiber Type", ["SMF", "MMF"])
    part_number = st.text_input("Enter Part Number: ").upper()
    qty = st.text_input("Enter quantity: ")
    return make, broadband, wavelength, range_, fiber_type, part_number, qty


def get_misc_details():
    """
    Get user input for Miscellaneous inventory item details.

    Returns:
        tuple: A tuple containing the following details:
        - brand (str): Brand of the miscellaneous item.
        - item (str): Name or description of the miscellaneous item.
        - qty (str): Quantity of the miscellaneous item.
    """
    brand = st.text_input("Enter Brand: ").upper()
    item = st.text_input("Enter item: ").upper()
    qty = st.text_input("Enter quantity: ")
    return brand, item, qty


def add_item_by_option(database, option, cili):
    """
    Add an item to the inventory based on the user's selection.

    Args:
        database (MongoIMS): An instance of the MongoIMS class for managing inventory data.
        option (str): The selected inventory category (e.g., 'Fiber', 'Optic', 'Misc').
        cili (str): The CILI value of the site associated with the item.
    """
    if option == "Fiber":
        cordage, type_, con_1, con_2, length, qty = get_fiber_details()
        if st.button("Update Inventory"):
            curr, qty, data = database.check_inventory(
                "fiber", cordage, type_, con_1, con_2, length, int(qty), cili
            )
            if curr:
                database.update_collection_data("fiber", curr, qty, data)
                st.success("Table Update!")
            else:
                database.insert_collection_data(
                    "fiber", cordage, type_, con_1, con_2, length, int(qty), cili
                )
                st.success("Table Update!")

    if option == "Optic":
        (
            make,
            broadband,
            wavelength,
            range_,
            fiber_type,
            part_number,
            qty,
        ) = get_optic_details()
        if st.button("Update Inventory"):
            curr, qty, data = database.check_inventory(
                "optic",
                make,
                broadband,
                wavelength,
                range_,
                fiber_type,
                part_number,
                int(qty),
                cili,
            )
            if curr:
                database.update_collection_data("optic", curr, qty, data)
                st.success("Table Update!")
            else:
                database.insert_collection_data(
                    "optic",
                    make,
                    broadband,
                    wavelength,
                    range_,
                    fiber_type,
                    part_number,
                    int(qty),
                    cili,
                )
                st.success("Table Update!")

    if option == "Misc":
        brand, item, qty = get_misc_details()
        if st.button("Update Inventory"):
            curr, qty, data = database.check_inventory(
                "misc", brand, item, int(qty), cili
            )
            if curr:
                database.update_collection_data("misc", curr, qty, data)
                st.success("Table Update!")
            else:
                database.insert_collection_data("misc", brand, item, int(qty), cili)
                st.success("Table Update!")


def remove_item_by_option(database, option, cili):
    """
    Remove an item from the inventory based on the user's selection.

    Args:
        database (MongoIMS): An instance of the MongoIMS class for managing inventory data.
        option (str): The selected inventory category (e.g., 'Fiber', 'Optic', 'Misc').
        cili (str): The CILI value of the site associated with the item.
    """
    if option == "Fiber":
        cordage, type_, con_1, con_2, length, qty = get_fiber_details()
        if st.button("Update Inventory"):
            curr, qty, data = database.check_inventory(
                "fiber", cordage, type_, con_1, con_2, length, int(qty), cili
            )
            if curr:
                database.update_collection_data("fiber", curr, -qty, data)
                st.success("Table Update!")
            else:
                st.write("Item does not exist.")

    if option == "Optic":
        (
            make,
            broadband,
            wavelength,
            range_,
            fiber_type,
            part_number,
            qty,
        ) = get_optic_details()
        if st.button("Update Inventory"):
            curr, qty, data = database.check_inventory(
                "optic",
                make,
                broadband,
                wavelength,
                range_,
                fiber_type,
                part_number,
                int(qty),
                cili,
            )
            if curr:
                database.update_collection_data("optic", curr, -qty, data)
                st.success("Table Update!")
            else:
                st.write("Item does not exist.")

    if option == "Misc":
        brand, item, qty = get_misc_details()
        if st.button("Update Inventory"):
            curr, qty, data = database.check_inventory(
                "misc", brand, item, int(qty), cili
            )
            if curr:
                database.update_collection_data("misc", curr, -qty, data)
                st.success("Table Update!")
            else:
                st.write("Item does not exist.")


def extract_and_insert_site_details(database):
    """
    Extract and insert site details into the inventory database.

    Args:
        database (MongoIMS): An instance of the MongoIMS class for managing inventory data.
    """
    cili, address, city, state, country, zip_code, site_id = get_site_details()

    if st.button("Add"):
        if not database.check_site(cili):
            database.insert_collection_data(
                "site", cili, address, city, state, country, zip_code, site_id
            )
            st.success("Table Update!")
        else:
            st.write("Site already exists.")


if __name__ == "__main__":
    dict_site = generate_dict_item(
        "site",
        "toroonxn",
        "151 front",
        "toronto",
        "ontario",
        "canada",
        "m3n 2x8",
        "i657h",
    )
    dict_fiber = generate_dict_item(
        "fiber", "simplex", "smf", "lc", "sc", "10m", 5, "toroonxn"
    )
    dict_optic = generate_dict_item(
        "optic", "champion one", "10g", "1310", "2km", "smf", "10g-smf", 7, "toroonxn"
    )
    dict_misc = generate_dict_item("misc", "brady", "roll", 3, "toroonxn")
    print(dict_site)
    print(dict_fiber)
    print(dict_optic)
    print(dict_misc)
