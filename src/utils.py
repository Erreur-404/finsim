import json, os


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


"""
Print informationnal message if the debug level meets the message level
\param      message: The message to print
\param      current_level: The verbose level. Usually given as a command line parameter
\param      message_level: The lowest verbose level needed to display the message
"""
def debug_print(message: str, current_level: int = 0, message_level: int = 1):
    if current_level >= message_level:
        print(message)
