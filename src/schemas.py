site_schema = {
    'cili' : str,
    'address' : str,
    'city' : str,
    'state' : str,
    'country' : str,
    'zip_code' : str,
    'site_id' : str
}

fiber_schema = {
    'cordage' : str,
    'type' : str,
    'conn1' : str,
    'conn2' : str,
    'length' : str,
    'quantity' : int,
    'site_cili' : str
}

optic_schema = {
    'make' : str,
    'broadband' : str,
    'wavelength' : str,
    'distance' : str,
    'type' : str,
    'part_number' : str,
    'quantity' : int,
    'site_cili' : str
}

misc_schema = {
    'brand' : str,
    'item' : str,
    'quantity' : int,
    'site_cili' : str
}

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://wallpaperaccess.com/full/2454628.png");
background-size: 100%;
display: flex;
background-position: top left;
background-repeat: no-repeat;
background-attachment: fixed;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""