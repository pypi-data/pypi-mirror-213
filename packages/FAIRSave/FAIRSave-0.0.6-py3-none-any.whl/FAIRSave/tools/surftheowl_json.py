from FAIRSave.tools.key import Key

list_of_all_keys = []

# the same datatypes from the surf the owl converter
DICT_STANDARD_DATATYPES = {
    "str": 'string',
    type([]): 'string',
    type({}.keys()): 'dictionary',
    "int": 'integer',
    "float": 'float',
    "bool": 'boolean',
    "dateTimeStamp": 'date',
}

# structural keys of the surf the owl json files
KEYS_TO_SKIP = [
    "Contextual Type",
    "normal_Objects",
    "special_Objects"
]

# starts conversion with the fist layer in the dictionary
def dict_to_list_of_keys(dictionary):
    global list_of_all_keys
    list_of_all_keys = []
    # Skips the title of the SurfTheOWL json file
    for key in dictionary:
        read_layer(dictionary[key], [])
    return list_of_all_keys
    
    
# recursively reads the keys out of the layers of the dictionary
def read_layer(dictionary, location: list):

    next_keys = list(dictionary.keys())

    for key in next_keys:
        # key contains more keys
        if type(dictionary[key]) == type({}):
            add_top_key(key, dictionary[key].keys(), location)
            read_layer(dictionary[key], location + [key])
        # key contains list of possibly more keys
        elif type(dictionary[key]) == type([]) and key not in KEYS_TO_SKIP:
            # check that there are no dictionaries in the list
            values = list(dictionary[key])
            for i in range(0, len(values)):
                if type(values[i]) == type({}):
                    read_layer(values[i], location  + [key])
                    values[i] = values[i].keys()
            add_top_key(key, values, location)
        # regular key
        else:
            add_standard_key(key, dictionary[key], None, location)


# adds a key with sub keys
def add_top_key(key, value, location: list):
    global list_of_all_keys
    if key not in KEYS_TO_SKIP:
        new_key = Key(key, list(value), DICT_STANDARD_DATATYPES[type(value)])
        new_key.set_location(location)
        list_of_all_keys.append(new_key)


# adds a key without sub keys
def add_standard_key(key, datatype, value, location: list):
    global list_of_all_keys
    if key not in KEYS_TO_SKIP:
        if datatype in DICT_STANDARD_DATATYPES:
            new_key = Key(key, value, DICT_STANDARD_DATATYPES[datatype])
        else:
            new_key = Key(key, value, DICT_STANDARD_DATATYPES[type(datatype)])
        new_key.set_location(location)
        list_of_all_keys.append(new_key)

