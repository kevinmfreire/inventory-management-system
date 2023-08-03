import pymongo
import pandas as pd
import streamlit as st
from src.schemas import site_schema, fiber_schema, optic_schema, misc_schema

def check_connectors(con_1, con_2):
    if con_1 != 'LC':
            tmp = con_1
            con_1 = con_2
            con_2 = tmp
    return con_1, con_2

def remove_columns(df, cols):
    try:
        df = df.drop(columns=cols)
    except KeyError as e:
        print(f"Error: Column '{cols}' not found in the DataFrame.")
    return df

def set_index_with_exception_handling(df, index):
    try:
        df = df.set_index(df.columns[index])
    except IndexError as e:
        print("Error: The DataFrame is empty and cannot be set as an index.")
    return df

def convert_to_dataframe(_collection, data):
    return pd.DataFrame(list(_collection.find(data)))

def insert_data(collection, category, data):
    if category == 'site':
        # Validate against electronics schema
        if set(data.keys()) == set(site_schema.keys()):
            # Check data types and other constraints if necessary
            if all(isinstance(data[field], site_schema[field]) for field in data):
                try:
                    collection.insert_one(data)
                except pymongo.errors.DuplicateKeyError:
                    print("Site already exists. Skipping insertion.")
            else:
                print("Invalid data types for Site schema.")
        else:
            print("Invalid data structure for electronics schema.")
    elif category == 'fiber':
        # Validate against clothing schema
        if set(data.keys()) == set(fiber_schema.keys()):
            # Check data types and other constraints if necessary
            if all(isinstance(data[field], fiber_schema[field]) for field in data):
                collection.insert_one(data)
            else:
                print("Invalid data types for fiber schema.")
        else:
            print("Invalid data structure for fiber schema.")

    elif category == 'optic':
        # Validate against clothing schema
        if set(data.keys()) == set(optic_schema.keys()):
            # Check data types and other constraints if necessary
            if all(isinstance(data[field], optic_schema[field]) for field in data):
                collection.insert_one(data)
            else:
                print("Invalid data types for fiber schema.")
        else:
            print("Invalid data structure for fiber schema.")
    elif category == 'misc':
        # Validate against clothing schema
        if set(data.keys()) == set(misc_schema.keys()):
            # Check data types and other constraints if necessary
            if all(isinstance(data[field], misc_schema[field]) for field in data):
                collection.insert_one(data)
            else:
                print("Invalid data types for clothing schema.")
        else:
            print("Invalid data structure for clothing schema.")
    else:
        print("Unknown category.")

def update_data_quantity(collection, category, new_quantity, data):
    if category == 'fiber':    
        collection.update_one(data, {'$set' : {'quantity' : new_quantity}})
    elif category == 'optic':
        collection.update_one(data, {'$set' : {'quantity' : new_quantity}})
    elif category == 'misc':
        collection.update_one(data, {'$set' : {'quantity' : new_quantity}})

def generate_dict_item(category, *args):
    if category == 'site':
        fill_items = ['cili', 'address', 'city', 'state', 'country', 'zip_code', 'site_id']
        try:
            dict_item = {fill_items[i] : args[i] for i in range(len(fill_items))}
            return dict_item
        except Exception as e:
            print("An error occurred:", str(e))
    elif category == 'fiber':
        fill_items = ['cordage', 'type', 'conn1', 'conn2', 'length', 'quantity', 'site_cili']
        try:
            dict_item = {fill_items[i] : args[i] for i in range(len(fill_items))}
            return dict_item
        except Exception as e:
            print("An error occurred:", str(e))
    elif category == 'optic':
        fill_items = ['make', 'broadband', 'wavelength', 'distance', 'type', 'part_number', 'quantity', 'site_cili']
        try:
            dict_item = {fill_items[i] : args[i] for i in range(len(fill_items))}
            return dict_item
        except Exception as e:
            print("An error occurred:", str(e))
    elif category == 'misc':
        fill_items = ['brand', 'item', 'quantity', 'site_cili']
        try:
            dict_item = {fill_items[i] : args[i] for i in range(len(fill_items))}
            return dict_item
        except Exception as e:
            print("An error occurred:", str(e))

def get_site_details():
    cili = st.text_input('Enter site CILI: ').upper()
    address = st.text_input('Enter site Address: ').upper()
    city = st.text_input('City: ').upper()
    state = st.text_input('State: ').upper()
    country = st.text_input('Country: ').upper()
    zip_code = st.text_input('Zip Code: ').upper()
    site_id = st.text_input('Site ID: ').upper()
    return cili, address, city, state, country, zip_code, site_id

def get_fiber_details():
    cordage = st.selectbox('Select Fiber cordage Type', ['SIMPLEX', 'DUPLEX'])
    type_ = st.selectbox('Select Fiber Type', ['SMF', 'MMF'])
    con_1 = st.selectbox('Select Connector 1', ['LC', 'SC'])
    con_2 = st.selectbox('Select Connector 2', ['LC', 'SC'])
    length = st.text_input('Enter length (M/FT): ').upper()
    qty = st.text_input('Enter quantity: ')
    return cordage, type_, con_1, con_2, length, qty

def get_optic_details():
    make = st.text_input('Enter Manufacturer: ').upper()
    broadband = st.text_input('Enter Boradband Speed: ').upper()
    wavelength = st.selectbox('Select wavelength (nm)', ['1310', '1550'])
    range_ = st.text_input('Enter Range: ').upper()
    fiber_type = st.selectbox('Select Fiber Type', ['SMF', 'MMF'])
    part_number = st.text_input('Enter Part Number: ').upper()
    qty = st.text_input('Enter quantity: ')
    return make, broadband, wavelength, range_, fiber_type, part_number, qty

def get_misc_details():
    brand = st.text_input('Enter Brand: ').upper()
    item = st.text_input('Enter item: ').upper()
    qty = st.text_input('Enter quantity: ')
    return brand, item, qty

if __name__ == '__main__':
    dict_site = generate_dict_item('site', 'toroonxn', '151 front', 'toronto', 'ontario' , 'canada', 'm3n 2x8', 'i657h')
    dict_fiber = generate_dict_item('fiber', 'simplex', 'smf', 'lc', 'sc' , '10m', 5, 'toroonxn')
    dict_optic = generate_dict_item('optic', 'champion one', '10g', '1310', '2km' , 'smf', '10g-smf', 7, 'toroonxn')
    dict_misc = generate_dict_item('misc', 'brady', 'roll', 3, 'toroonxn')
    print(dict_site)
    print(dict_fiber)
    print(dict_optic)
    print(dict_misc)