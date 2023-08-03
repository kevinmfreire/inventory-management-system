import streamlit as st
import sys

sys.path.append('src/')
from src import mongodb, utils, schemas

st.set_page_config(layout="wide", page_title='LUMEN - IMS', page_icon='https://static.thenounproject.com/png/145436-200.png')
st.markdown(schemas.page_bg_img, unsafe_allow_html=True)
db = mongodb.MongoIMS(st.secrets.mongodb)

if __name__=='__main__':
    st.title('Inventory Management System')

    radio_option = st.sidebar.radio('Menu', options=['View Items', 'Enter new site', 'Add Items', 'Remove Items'])

    if radio_option=='View Items':
        st.subheader('View Items')
        cili = st.selectbox('Select Site', db.get_cilis())
        fiber, optic, misc = db.get_inventory_from_cili(cili)
        st.write('### Fiber Inventory')
        st.dataframe(utils.set_index_with_exception_handling(fiber, 0))
        st.write('### Optics Inventory')
        st.dataframe(utils.set_index_with_exception_handling(optic, 0))
        st.write('### Misc Inventory')
        st.dataframe(utils.set_index_with_exception_handling(misc, 0))

    if radio_option=='Enter new site':
        st.subheader('Enter Site details')
        cili, address, city, state, country, zip_code, site_id = utils.get_site_details()

        if st.button('Add'):
            if not db.check_site(cili):
                db.insert_collection_data('site', cili, address, city, state, country, zip_code, site_id)
                st.success('Table Update!')
            else:
                st.write('Site already exists.')

    if radio_option=='Add Items':
        st.subheader('Add New Items')
        cili = st.selectbox('Select Site', db.get_cilis())
        option = st.radio('Select Item to add: ',
                          ('Fiber', 'Optic', 'Misc'))

        if option == 'Fiber':
            cordage, type_, con_1, con_2, length, qty = utils.get_fiber_details()
            if st.button('Update Inventory'):
                db.insert_collection_data('fiber', cordage, type_, con_1, con_2, length, int(qty), cili)
                st.success('Table Update!')
        
        if option == 'Optic':
            make, broadband, wavelength, range_, fiber_type, part_number, qty = utils.get_optic_details()
            if st.button('Update Inventory'):
                db.insert_collection_data('optic', make, broadband, wavelength, range_, fiber_type, part_number, int(qty), cili)
                st.success('Table Update!')

        if option == 'Misc':
            brand, item, qty = utils.get_misc_details()
            if st.button('Update Inventory'):
                db.insert_collection_data('misc', brand, item, int(qty), cili)
                st.success('Table Update!')

    if radio_option=='Remove Items':
        st.subheader('Remove Items')
        cili = st.selectbox('Select Site', db.get_cilis())
        option = st.radio('Select Item to remove: ',
                          ('Fiber', 'Optic', 'Misc'))
        
        if option == 'Fiber':
            cordage, type_, con_1, con_2, length, qty = utils.get_fiber_details()
            if st.button('Update Inventory'):
                curr, qty, data = db.check_inventory('fiber', cordage, type_, con_1, con_2, length, int(qty), cili)
                if curr:
                    db.update_collection_data('fiber', curr, qty, data)
                    st.success('Table Update!')
                else:
                    st.write('Item does not exist.')
        
        if option == 'Optic':
            make, broadband, wavelength, range_, fiber_type, part_number, qty = utils.get_optic_details()
            if st.button('Update Inventory'):
                curr, qty, data = db.check_inventory('optic', make, broadband, wavelength, range_, fiber_type, part_number, int(qty), cili)
                if curr:
                    db.update_collection_data('optic', curr, qty, data)
                    st.success('Table Update!')
                else:
                    st.write('Item does not exist.')

        if option == 'Misc':
            brand, item, qty = utils.get_misc_details()
            if st.button('Update Inventory'):
                curr, qty, data = db.check_inventory('misc', brand, item, int(qty), cili)
                if curr:
                    db.update_collection_data('misc', curr, qty, data)
                    st.success('Table Update!')
                else:
                    st.write('Item does not exist.')
    