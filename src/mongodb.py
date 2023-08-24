"""
MongoIMS - MongoDB Inventory Management System

This script defines a class, MongoIMS, for managing inventory data stored in a MongoDB database.
It utilizes the pymongo library for MongoDB interactions and streamlit for creating a user interface.

Author: Kevin Freire
Date: August 23, 2023
"""

import pymongo
import streamlit as st

from utils import (
    generate_dict_item,
    update_data_quantity,
    remove_columns,
    check_connectors,
    insert_data,
    convert_to_dataframe,
)


@st.cache_resource
def init_connection(uri):
    """
    Initialize a connection to the MongoDB database.

    Args:
        uri (str): The MongoDB connection URI.

    Returns:
        pymongo.MongoClient: A MongoDB client instance.
    """
    return pymongo.MongoClient(uri)


@st.cache_resource
def load_inventory_collections(_client):
    """
    Load collections from the MongoDB database.

    Args:
        _client (pymongo.MongoClient): A MongoDB client instance.

    Returns:
        dict: A dictionary containing MongoDB collections.
    """
    db = _client.inventory_db
    collections = {
        "site": db.sites,
        "fiber": db.fibers,
        "optic": db.optics,
        "misc": db.misc,
    }
    return collections


class MongoIMS:
    """
    MongoIMS - MongoDB Inventory Management System

    This class provides an interface to manage inventory data stored in a MongoDB database.
    It facilitates interactions with MongoDB collections for different inventory categories,
    offers methods to query, insert, and update inventory items, and supports operations
    related to specific "cili" values for sites.

    Attributes:
        uri (str): The MongoDB connection URI.
        client (pymongo.MongoClient): A MongoDB client instance.
        collection (dict): MongoDB collections.
    """
    
    def __init__(self, credentials):
        """
        Initialize the MongoIMS instance with MongoDB credentials.

        Args:
            credentials (object): An object containing MongoDB user and password.

        Attributes:
            uri (str): The MongoDB connection URI.
            client (pymongo.MongoClient): A MongoDB client instance.
            collection (dict): MongoDB collections.
        """
        self.uri = f"mongodb+srv://{credentials.user}:{credentials.password}@inventory.wjwchhk.mongodb.net/?retryWrites=true&w=majority"
        self.client = init_connection(self.uri)
        self.collection = load_inventory_collections(self.client)
        self.collection["site"].create_index([("cili", pymongo.ASCENDING)], unique=True)

    def check_inventory(self, category, *args):
        """
        Check inventory for a given category and item attributes.

        Args:
            category (str): The category of the item.
            *args: Variable-length arguments representing item attributes.

        Returns:
            tuple: A tuple containing the current quantity, input quantity, and item data.
        """
        data = generate_dict_item(category, *args)
        input_qty = data.pop("quantity")
        cur_qty = None
        try:
            cur_qty = self.collection[category].find_one(data, {"quantity": 1})[
                "quantity"
            ]
        except Exception as e:
            print("An error occurred:", str(e))
        return cur_qty, input_qty, data

    def insert_collection_data(self, category, *args):
        """
        Insert data into the specified category's collection.

        Args:
            category (str): The category of the item.
            *args: Variable-length arguments representing item attributes.
        """
        dict_data = generate_dict_item(category, *args)
        if category == "fiber":
            dict_data["conn1"], dict_data["conn2"] = check_connectors(
                dict_data["conn1"], dict_data["conn2"]
            )
        insert_data(self.collection[category], category, dict_data)

    def update_collection_data(
        self, category, current_quantity, amount_to_remove, data
    ):
        """
        Update the quantity of an item in the specified category's collection.

        Args:
            category (str): The category of the item.
            current_quantity (int): The current quantity of the item.
            amount_to_remove (int): The amount to remove from the quantity.
            data (dict): Item data used to identify the item.
        """
        new_quantity = max(0, current_quantity + amount_to_remove)
        update_data_quantity(self.collection[category], category, new_quantity, data)

    def get_cilis(self):
        """
        Get a list of distinct "cili" values from the "site" collection.

        Returns:
            list: A list of distinct "cili" values.
        """
        return self.collection["site"].distinct("cili")

    def get_inventory_from_cili(self, cili):
        """
        Get inventory data associated with a "cili" from various collections.

        Args:
            cili (str): The "cili" value to retrieve data for.

        Returns:
            tuple: A tuple containing dataframes for fiber, optic, and misc inventory.
        """
        fiber_documents = remove_columns(
            convert_to_dataframe(self.collection["fiber"], {"site_cili": cili}),
            ["_id", "site_cili"],
        )
        optic_documents = remove_columns(
            convert_to_dataframe(self.collection["optic"], {"site_cili": cili}),
            ["_id", "site_cili"],
        )
        misc_documents = remove_columns(
            convert_to_dataframe(self.collection["misc"], {"site_cili": cili}),
            ["_id", "site_cili"],
        )
        return fiber_documents, optic_documents, misc_documents

    def check_site(self, cili):
        """
        Check if a site with a given "cili" exists in the "site" collection.

        Args:
            cili (str): The "cili" value to check.

        Returns:
            dict: The site document if found, otherwise None.
        """
        return self.collection["site"].find_one({"cili": cili})
