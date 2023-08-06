import json
from FAIRSave.tools import json_reader
from FAIRSave.tools import surftheowl_json
from FAIRSave.tools.comparison import compare_lists_of_all_keys, set_type_of_comparison
from FAIRSave.tools.difference import print_differences, get_all_differences, reset, export_errors_as_json
from FAIRSave.tools.key import add_lines_to_keys
from FAIRSave.tools.metadata import determine_relevant_class
from FAIRSave.configuration import Configuration


def compare_jsons_from_dictionary(dict1: dict, dict2: dict):  
    """General function to call if two jsons are compared.
    It first determines what kind of jsons files they are, then converts them to a general list of keys.
    Both lists then are compared for key existence, datatypes, structure, value and units.
    Differences are printed to the Terminal.
    For the comparison to work each file must have at least one key, and both files must be json files.

    Args:
        dict1 (dict): json file loaded into a python dictionary
        dict2 (dict): json file loaded into a python dictionary
        
    Returns:
       list: all the detected differences as Object Difference. It contains the different keys (key and other_key),
       the file it was found (file), the type of difference (type_of_difference) and an error message as attributes 
       (error_message). The last item in the list is a dictionary containing key that exist a different number of times, with the
       number of difference as value.
    """
    
    reset()
    
    determine_relevant_class(dict1, dict2)
    
    list1 = determine_and_convert_input(dict1)
    list2 = determine_and_convert_input(dict2)
    
    add_lines_to_keys(dict1, list1, get_actual_dict(dict1))
    add_lines_to_keys(dict2, list2, get_actual_dict(dict2))

    if len(list1) > 0 and len(list2) > 0:
        compare_lists_of_all_keys(list1, list2)
    else:
        print(Configuration.ERROR_MESSAGES['loading_file'])
    
    print_differences()
    return get_all_differences()


def compare_jsons_from_path(path1: str, path2: str):
    """General function to call if two jsons are compared.
    It first determines what kind of jsons files they are, then converts them to a general list of keys.
    Both lists then are compared for key existence, datatypes, structure, value and units.
    Differences are printed to the Terminal.
    For the comparison to work each file must have at least one key, and both files must be json files.

    Args:
        path1 (String): path to the first json file
        path2 (String): path to the second json file
    
    Returns:
       list: all the detected differences as Object Difference. It contains the different keys (key and other_key),
       the file it was found (file), the type of difference (type_of_difference) and an error message as attributes 
       (error_message). The last item in the list is a dictionary containing key that exist a different number of times, with the
       number of difference as value.
    """
    
    reset()
    
    try:
        file1 = open(path1)
        file2 = open(path2)

        dict1 = json.load(file1)
        dict2 = json.load(file2)
        
        result = compare_jsons_from_dictionary(dict1, dict2)
        
        export_errors_as_json(path1.split("/")[-1], path2.split("/")[-1])

        return result
    
    except json.decoder.JSONDecodeError:
        print(Configuration.ERROR_MESSAGES['loading_file'])
    

# function determines if json is Kadi4Mat record/template or SurfTheOwl json or vocabulary and converts it to list of keys
def determine_and_convert_input(json_dict: dict):
    """Determines what type 

    Args:
        json_dict (dict): The json file in the format of a python dictionary
        
    Returns:
        list: the list with the converted general keys
    """
    
    if 'normal_Objects' in json_dict:
        set_type_of_comparison(4)
        return surftheowl_json.dict_to_list_of_keys(json_dict)
    else:
        return json_reader.dict_to_list_all_keys(json_dict)



# function that determines what type of file it is and returns the part of the dictionary that contains the terms
def get_actual_dict(json_dict):
    for type in Configuration.TYPES_OF_JSON_FILES:
        actual_dict = json_reader.determine_searched_part(json_dict, type)
        if actual_dict != None:
            return actual_dict
    return json_dict