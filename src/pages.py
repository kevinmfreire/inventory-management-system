import streamlit as st
from src.utils import set_index_with_exception_handling, extract_and_insert_site_details, add_item_by_option, remove_item_by_option, get_infra_details

def inventory_page(db):
    st.title('Inventory Management System')
    radio_option = st.sidebar.radio('Menu', options=['View Items', 'Enter new site', 'Add Items', 'Remove Items'])

    if radio_option=='View Items':
        st.subheader('View Items')
        cili = st.selectbox('Select Site', db.get_cilis())
        fiber, optic, misc = db.get_inventory_from_cili(cili)
        st.write('### Fiber Inventory')
        st.dataframe(set_index_with_exception_handling(fiber, 0))
        st.write('### Optics Inventory')
        st.dataframe(set_index_with_exception_handling(optic, 0))
        st.write('### Misc Inventory')
        st.dataframe(set_index_with_exception_handling(misc, 0))

    if radio_option=='Enter new site':
        st.subheader('Enter Site details')
        extract_and_insert_site_details(db)

    if radio_option=='Add Items':
        st.subheader('Add New Items')
        cili = st.selectbox('Select Site', db.get_cilis())
        option = st.radio('Select Item to add: ',
                        ('Fiber', 'Optic', 'Misc'))
        add_item_by_option(db, option, cili)

    if radio_option=='Remove Items':
        st.subheader('Remove Items')
        cili = st.selectbox('Select Site', db.get_cilis())
        option = st.radio('Select Item to remove: ',
                        ('Fiber', 'Optic', 'Misc'))
        remove_item_by_option(db, option, cili)

def home_page():
    st.title('Home')
    st.subheader('About')
    st.write('''
            This web application is intended to keep track of consumable materials that Field Technicians
            commonly use in their day to day.  It is only intended to track their fiber inventory, network
            optics and other materials such as items for label maker or office supplies.  
    ''')
    st.subheader('Future Work')
    st.write('''
            In the future their are plans to implement a chatbot allowing technicians to be 
            able to chat with any PDF documents such as manuals to allow technicains to 
            troubleshoot equipment more efficiently. In addition implementign another database that
            allows technician track port assignment within the data centers.
    ''')
