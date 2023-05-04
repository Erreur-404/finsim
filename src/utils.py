"""
Read the constants from the constants file
\return the constants in a dict format
"""
def read_constants():
    constants_path = os.path.join(os.path.dirname(__file__), 'constants.json')
    with open(constants_path, 'r') as f:
        return json.load(f)


"""
Clamp the parameter so that it does not go below 0.
\param      attrib: The value to clamp
\return     The clamped parameter
"""
def clamp(attrib):
    return 0 if attrib < 0 else attrib
