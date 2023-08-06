from FAIRSave.configuration import Configuration
from FAIRSave.tools.key import Key

list_of_all_keys = []
key_dict = {}
needed_links = []

# Converts the dictionary of the json to a list of key objects
def dict_to_list_all_keys(json_dict: dict):
    # resets keys from previous conversion
    global list_of_all_keys
    list_of_all_keys = []

    # tests what type of json file it is
    for type_of_file in Configuration.TYPES_OF_JSON_FILES:
        actual_dict = determine_searched_part(json_dict, type_of_file)
        if actual_dict != None:
            break
    
    if type(actual_dict) == list:
        for terms in actual_dict:
            read_layer(terms, [])
    elif type(actual_dict) == dict:
        read_layer(actual_dict, [])
    else:
        print(Configuration.ERROR_MESSAGES['unknown_json'])
        return None
    
    return list_of_all_keys


# tests what type of json file it is and return the correct dict from Configuration
def determine_type_of_file(json_dict):
    for type_of_file in Configuration.TYPES_OF_JSON_FILES:
        if determine_searched_part(json_dict, type_of_file) != None:
            return type_of_file


# determines what is the part to be converted into general Keys
# returns None if the key dictionary is not the right one for this file
def determine_searched_part(json_dict: dict, assumed_key_dict: dict):
    
    # goes through all the keys to check if the part works
    searched_part = json_dict
    for key in assumed_key_dict['keys_to_searched_part']:
        if key in searched_part:
            searched_part = searched_part[key]
        else:
            return None
    
    # additional functions needed for some types of json files 
    def get_correct_list_by_name():
        global key_dict
        # reads the main layer and not the related terms of vocpopuli files by looking for the correct name
        for vocab in searched_part:
            
            if 'record_title' in assumed_key_dict and vocab[assumed_key_dict['term_name']] in assumed_key_dict['record_title']:
                key_dict = assumed_key_dict
            
                if key_dict['next_layer'] in vocab:
                    return vocab[key_dict['next_layer']]
                else:
                    return vocab
            elif vocab[assumed_key_dict['term_name']] in json_dict[assumed_key_dict['term_name']]:
                key_dict = assumed_key_dict
                if key_dict['next_layer'] in vocab:
                    return vocab[key_dict['next_layer']]
                else:
                    return vocab
                
        return searched_part
    
    if 'get_correct_list_by_name' in assumed_key_dict and assumed_key_dict['get_correct_list_by_name']:
        searched_part = get_correct_list_by_name()  
        
        if assumed_key_dict['related_vocabularies'] in searched_part:
            assumed_key_dict['needed_links'] = searched_part[assumed_key_dict['related_vocabularies']]
            print(assumed_key_dict['needed_links'])
            
        
    
    # checks if the correct type was found
    if type(searched_part) == assumed_key_dict['type_of_searched_part']:
        global key_dict
        key_dict = assumed_key_dict
        return searched_part
    else:
        return None
 
   
            
# Determines the type of the layer: checks if there is a sublayer after this layer
def read_layer(searched_part, location: list):
    
    # list containing dictionaries: each dictionary read in as a layer
    if type(searched_part) == list:
        for term in searched_part:
            read_layer(term, location)
    
    # the searched part is not a term but a value
    elif type(searched_part) != dict:
        return
    
    # not a full key, used in kadi records to simulate list items                    
    elif not key_dict['term_name'] in searched_part and key_dict['next_layer'] in searched_part:
        # this dictionary does not have a name because it simulates a list
        read_layer(searched_part[key_dict['next_layer']], location)
    
    # layer is a key
    elif key_dict['term_name'] in searched_part and key_dict['datatype'] in searched_part:
        # term is not a key but an option
        if 'datatype_for_options' in key_dict and searched_part[key_dict['datatype']] == key_dict['datatype_for_options']:
            return
        
        # makes key out of this dict
        list_of_all_keys.append(to_key(searched_part, location))
        if key_dict['next_layer'] in searched_part:
            read_layer(searched_part[key_dict['next_layer']], location + [searched_part[key_dict['term_name']]])
        
    else:
        print(Configuration.ERROR_MESSAGES['incomplete_key'])



def to_key(term_dict: dict, location):
    
    name = term_dict[key_dict['term_name']]
    if term_dict[key_dict['datatype']] in Configuration.DATATYPE_CONVERSION:
        datatype = Configuration.DATATYPE_CONVERSION[term_dict[key_dict['datatype']]]
    else:
        datatype = term_dict[key_dict['datatype']]
    key = Key(name, datatype, location)
    
    # when the options for the key are dictionaries with a certain datatype 
    if 'datatype_for_options' in key_dict:
        if key_dict['next_layer'] in term_dict:
            for child in term_dict[key_dict['next_layer']]:
                if child[key_dict['datatype']] == key_dict['datatype_for_options']:
                    key.add_option(child[key_dict['term_name']])
    
    # the validation (options and requirement) is added to the key object
    if 'validation' in key_dict and key_dict['validation'] in term_dict:
        if 'mandatory' in key_dict and key_dict['mandatory'] in term_dict[key_dict['validation']]:
            key.set_mandatory(term_dict[key_dict['validation']][key_dict['mandatory']])
        if 'options' in key_dict and key_dict['options'] in term_dict[key_dict['validation']]:
            key.add_option(term_dict[key_dict['validation']][key_dict['options']])
                    
    # the value of the term is added to the key object
    if 'value' in key_dict and key_dict['value'] in term_dict:
        # the value of this term is added
        if type(term_dict[key_dict['value']]) != list and type(term_dict[key_dict['value']]) != dict:
            key.set_value(term_dict[key_dict['value']])
        # the names of the contained keys are added as value
        # elif type(term_dict[key_dict['value']]) == list:
            #for term in term_dict[key_dict['value']]:
                #if type(term) == dict and key_dict['term_name'] in term:
                    #key.add_option(term[key_dict['term_name']])
            
    # the unit of this term is added to the key object
    if 'unit' in key_dict and key_dict['unit'] in term_dict:
        key.set_unit(term_dict[key_dict["unit"]])

    return key

