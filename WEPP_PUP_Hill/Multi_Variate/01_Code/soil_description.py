# soil description_functions.py



# Adjust line/column indices based on actual WEPP input file structure
PARAMETER_LOCATIONS = {
    "datver": (0, 0),							# Define parameter locations: {parameter_name: (line_number, column_index)}
    "comments": {"position": (1, 0), "type": str},
    "ntemp": {"position": (2, 0), "type": int},
    "ksflag": {"position": (2,1), "type":int},				# detailed description available in user wepp documents
    "slid": {"position": (3, 0), "type": str},
    "textid": {"position": (3, 1), "type": str},
    "nsl": {"position": (3, 2), "type": int},
    "salb": {"position": (3, 3), "type": float},
    "sat":{"position": (3, 4),"type": float},
    "CKi": {"position":(3, 5),"type": float},
    "CKr": {"position":(3, 6),"type": float},
    "Cshcrit":{"position": (3, 7),"type": float},
    "Ke": {"position":(3, 8),"type": float},
    "solthk": {"position":(4, 0),"type": float},
    "sand": {"position":(4, 1 ),"type": float},
    "clay": {"position":(4, 2),"type": float},
    "orgmat": {"position":(4, 3),"type": float},
    "cec": {"position":(4, 4),"type": float},
    "rfg": {"position":(4, 5),"type": float},
    "aniso": {"position":(5, 2),"type": float},
    "Ksat": {"position":(5, 3),"type": float},
    # Add more parameters as needed/ if it is in model
}

























