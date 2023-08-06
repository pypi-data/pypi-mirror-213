from FAIRSave.configuration import Configuration
from FAIRSave.tools.key import Key, sort_keys, compare_alphabetical
from FAIRSave.tools import difference
import re

# 1: names, 2: datatypes, 3: location, 4: value, 5: units
TYPE_OF_COMPARISON = 5

# contains all the standard datatypes for comparability
DICT_STANDARD_DATATYPES = {
    type([]): 'list',
    type({}): 'dictionary',
    int: 'integer',
    str: 'string',
    float: 'float',
    type(True): 'boolean'
}

# function to choose what will be compared
def set_type_of_comparison(type):
    """Decides what of the keys should be compared:
    1: only names, 2: datatypes, 3: location, 4: value, 5: units

    Args:
        type (int): number of the above to choose comparisons
    """
    global TYPE_OF_COMPARISON
    TYPE_OF_COMPARISON = type


# compares the keys in the chosen way (a better way to choose different comparisons)
def compare_keys(key1: Key, key2: Key):
    if key1.name != key2.name:
        return
    if TYPE_OF_COMPARISON > 1:
        compare_key_datatypes(key1, key2)
    if TYPE_OF_COMPARISON > 2:
        compare_key_location(key1, key2)
    if TYPE_OF_COMPARISON > 3:
        compare_key_value(key1, key2)
        compare_value_to_datatype(key1, 1)
        compare_value_to_datatype(key2, 2)
    if TYPE_OF_COMPARISON > 4:
        compare_key_unit(key1, key2)


# Possible Comparisons
def compare_key_names(key1: Key, key2: Key):
    return compare_names_strings(key1.name, key2.name, key1, key2)
    

# returns True if the strings are considered the same key name just spelled differently
# when no keys are given no differences are caught
def compare_names_strings(name_1: str, name_2: str, key_1 = None, key_2 = None):
    if name_1 == name_2:
        return True
    elif name_1.lower() == name_2.lower():
        if key_1 != None:
            difference.character_case_mismatch(key_1, key_2)
        return True
    else:
        def levenshtein_ratio(word_1, word_2):
            if len(word_1) < len(word_2):
                return levenshtein_ratio(word_2, word_1)
            elif len(word_2) == 0:
                return len(word_1)
            previous = range(len(word_2) + 1)
            for i, c1 in enumerate(word_1):
                current = [i + 1]
                for j, c2 in enumerate(word_2):
                    insertion = previous[j + 1] + 1
                    deletion = current[j] + 1
                    if c1 == c2:
                        substitution = previous[j]
                    else:
                        substitution = previous[j] + 1
                    current.append(min(insertion, deletion, substitution))
                previous = current
            return 1 - (previous[-1]/len(word_1))
         
        if levenshtein_ratio(name_1, name_2) > 0.9:
            if key_1 != None and preliminary_filter(key_1, key_2):
                difference.misspelling(key_1, key_2)
                return True
            
        return False

# checks if the keys with similar names are possible matches through location and datatype
def preliminary_filter(key1: Key, key2: Key):
    return key1.datatype == key2.datatype and key1.broader_terms[-1] == key2.broader_terms[-1]
    

def compare_key_datatypes(key1: Key, key2: Key):
    if not key1.datatype == key2.datatype:
        difference.datatype_mismatch(key1, key2)


# compares just the broader term, so only the moved key gets a warning
def compare_key_location(key1: Key, key2: Key):
    if len(key1.broader_terms) > 0 and len(key2.broader_terms) > 0:
        if not compare_names_strings(key1.broader_terms[-1], key2.broader_terms[-1]):
            difference.location_mismatch(key1, key2)


def compare_key_unit(key1: Key, key2: Key):
    if not key1.unit == key2.unit:
        difference.unit_mismatch(key1, key2)


# Compares values to list of options/ each other and checks if mandatory values are missing
def compare_key_value(key1: Key, key2: Key):
    # if one value is mandatory but not existant
    if (key1.mandatory and key2.mandatory) and key1.value == None and key2.value == None:
        difference.mandatory_value_missing(key1, key2)
    # if one is list, it is checked if other value exists in the list
    elif type(key2.value) == type([]) and type(key1.value) != type([]):
        if not key1.value in key2.value and key1.value != None:
            for value in key2.value:
                if type(value) == str and type(key1.value)== str and compare_names_strings(value, key1.value):
                    difference.value_character_case_mismatch(key1, key2, value, key1.value)
                    return
            difference.value_mismatch_list(key1, key2, 1, key1.value)
    # if both are lists, those are compared without order
    elif type(key2.value) == type([]) and type(key1.value) == type([]):
        if not key1.value.sort() == key2.value.sort():
            difference.single_value_mismatch(key1, key2)
    # compared the other way around
    elif type(key2.value) != type([]) and type(key1.value) == type([]):
        if not key2.value in key1.value and key2.value != None:
            for value in key1.value:
                if type(value) == str and type(key2.value)== str and value.lower() == key2.value.lower():
                    difference.value_character_case_mismatch(key1, key2, value, key2.value)
                    return
            difference.value_mismatch_list(key1, key2, 2, key2.value)
    


# checks if value has the required datatype
# dates are compared to regex pattern to check
def compare_value_to_datatype(key: Key, file):
    if key.value == None:
        return
    elif key.datatype == 'date' and type(key.value) == str: 
        if not re.search("^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}$", key.value):
            difference.internal_datatype_inconsistency(key, file)
    elif not key.datatype == DICT_STANDARD_DATATYPES[type(key.value)]:
        if not type(key.value) == type([]):
            difference.internal_datatype_inconsistency(key, file)


# compares two lists of keys for existance (json vs json)
def compare_lists_of_all_keys(list1: list, list2: list):
    """
    The method sorts all keys alphabetically and iterates through them to compare if the same keys exist in both
    lists. When pairs of matching keys are found, they are compared to each other for their other values.

    Args:
        list1 (list): List of keys from the first json file
        list2 (list): List of keys from the second json file
    """
   
    list1 = sort_keys(list1)
    list2 = sort_keys(list2)

    index2 = 0
    index1 = 0
    # loops through list one to see if there is a counterpart in list 2
    while index1 < len(list1):
        # if already iterated through list 2 the keys are multiples of the last key or do not exist
        if index2 == len(list2):
            if compare_key_names(list1[index1], list2[index2 - 1]):
                compare_keys(list1[index1], list2[index2 - 1])
                difference.key_more_often_in_list(list1[index1], 2)
            else:
                difference.key_not_in_other_list(list1[index1], 2)  
        # Keys are at the same index 
        elif compare_key_names(list1[index1], list2[index2]):
            compare_keys(list1[index1], list2[index2])
            index1 += 1
            # if there are multiple of the same key in list 1
            while index1 < len(list1) and compare_key_names(list1[index1], list2[index2]):
                difference.key_more_often_in_list(list2[index2], 1)
                compare_keys(list1[index1], list2[index2])
                index1 += 1
            index2 += 1
            continue
        # same key one index higher (if multiple of one key)
        elif compare_key_names(list1[index1], list2[index2 - 1]):
            compare_keys(list1[index1], list2[index2 - 1])
            difference.key_more_often_in_list(list1[index1], 1)
        # Key either does not exist or is lower in list
        else:
            # key could exist in list2 with a higher index
            key_exists = False
            while index2 < len(list2) and compare_alphabetical(list2[index2], list1[index1]):
                if compare_key_names(list1[index1], list2[index2]):
                    compare_keys(list1[index1], list2[index2])
                    key_exists = True
                    index2 += 1
                    break
                # skipped keys dont exist in list1 (or are multiples)
                else:
                    if index2 > 0 and compare_key_names(list2[index2], list2[index2 - 1]):
                        compare_keys(list1[index1 - 1], list2[index2])
                        difference.key_more_often_in_list(list2[index2], 2)
                    else:
                        difference.key_not_in_other_list(list2[index2], 1)
                    index2 += 1
            # key does not exist in list2
            if not key_exists:
                difference.key_not_in_other_list(list1[index1], 2) 
        index1 += 1  

    # if list1 shorter than list2
    while index2 < len(list2):
        if not compare_key_names(list2[index2 - 1], list2[index2]):
            difference.key_not_in_other_list(list2[index2], 1)
        index2 += 1
        
