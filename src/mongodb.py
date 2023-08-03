import pymongo
import streamlit as st
from utils import *

@st.cache_resource
def init_connection(uri):
    return pymongo.MongoClient(uri)

@st.cache_resource
def load_collections(_client):
    db = _client.inventory_db
    collections = {
            'site' : db.sites,
            'fiber' : db.fibers,
            'optic' : db.optics,
            'misc' : db.misc
        }
    return collections

class MongoIMS():
    def __init__(self, credentials):
        self.uri = f"mongodb+srv://{credentials.user}:{credentials.password}@inventory.wjwchhk.mongodb.net/?retryWrites=true&w=majority"
        self.client = init_connection(self.uri)
        self.collection = load_collections(self.client)
        self.collection['site'].create_index([('cili', pymongo.ASCENDING)], unique=True)

    def check_inventory(self, category, *args):
        data = generate_dict_item(category, *args)
        input_qty = data.pop('quantity')
        cur_qty = None
        try:
            cur_qty = self.collection[category].find_one(data, {'quantity' : 1})['quantity']
        except Exception as e:
            print("An error occurred:", str(e))
        return cur_qty, input_qty, data

    def insert_collection_data(self, category, *args):
        dict_data = generate_dict_item(category, *args)
        if category == 'fiber':
            dict_data['conn1'], dict_data['conn2'] = check_connectors(dict_data['conn1'], dict_data['conn2'])
        insert_data(self.collection[category], category, dict_data)

    def update_collection_data(self, category, current_quantity, amount_to_remove, data):
        new_quantity = max(0, current_quantity + amount_to_remove)
        update_data_quantity(self.collection[category], category, new_quantity, data)

    def get_cilis(self):
        return self.collection['site'].distinct('cili')
    
    def get_inventory_from_cili(self, cili):
        fiber_documents = remove_columns(convert_to_dataframe(self.collection['fiber'], {'site_cili' : cili}), ['_id', 'site_cili'])
        optic_documents = remove_columns(convert_to_dataframe(self.collection['optic'], {'site_cili' : cili}), ['_id', 'site_cili'])
        misc_documents = remove_columns(convert_to_dataframe(self.collection['misc'], {'site_cili' : cili}), ['_id', 'site_cili'])
        return fiber_documents, optic_documents, misc_documents
    
    def check_site(self, cili):
        return self.collection['site'].find_one({'cili' : cili})
