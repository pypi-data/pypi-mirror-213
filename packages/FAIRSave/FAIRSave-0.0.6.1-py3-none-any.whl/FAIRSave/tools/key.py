import re
import json
from FAIRSave.configuration import Configuration

class Key:
    """
    Class that contains the structure for one Key in the json files.
    It saves the attributes 'name', 'datatype' and 'broader_terms' for every key, as well as the optional attributes 'unit',
    'mandatory' and 'value'. It can also be located in the json file by the beginning and ending lines.
    """
    # constructor, with key name, value (or list of values) and datatype thats standardized
    # other attributes are assigned default values for easier comparability
    def __init__(self, name, datatype, location): 
        self.name = name
        self.datatype = datatype
        self.broader_terms = location
        
        self.value = None
        self.unit = None
        self.mandatory = False
        
        self.line_beginning = 0
        self.line_ending = 0
        self.line_value = 0
        self.line_unit = 0
        self.line_datatype = 0
        self.line_name = 0
    
    # add unit to key
    def set_unit(self, unit):
        self.unit = unit

    # add if key is mandatory
    def set_mandatory(self, mandatory):
        self.mandatory = mandatory

    # list of all broader terms (to retrace location)
    def set_location(self, broader_terms):
        self.broader_terms = broader_terms
    
    # change the datatype of this key
    def set_datatype(self, datatype):
        self.datatype = datatype
    
    # changes the value of the term
    def set_value(self, value):
        if value != None:
            self.value = value
    
    # add an option to the values of this key
    def add_option(self, option):
        converted_option = option
        if option == None:
            return
        elif type(self.value) == list and type(converted_option) != list:
            self.value.append(converted_option)
        elif type(self.value) == list and type(converted_option) == list:
            self.value = self.value + converted_option
        elif self.value == None and type(converted_option) != list:
            self.value = [converted_option]
        elif self.value == None and type(converted_option) == list:
            self.value = converted_option
        else:
            self.value = [self.value, converted_option]
    
    # sets the lines where the key is found in the file     
    def set_line_in_file(self, line_beginning, line_ending):
        self.line_beginning = line_beginning 
        self.line_ending = line_ending
    
    def to_string(self):
        return f"{self.name}: {self.datatype}, {self.value}, {self.unit}, at {self.broader_terms}, line: {self.line_beginning}"
    

# return boolean value if higerkey is higher up in an alphabetical order
def compare_alphabetical(higher_key: Key, lower_key: Key):
    """Function used to compare two Keys alphabetically by their names

    Args:
        higherKey (Key): a Key, that is tested to be higher in the alphabet than the other key
        lowerKey (Key): the other Key

    Returns:
        boolean: returns true if the higher key is higher (or equal) in the alphabet
    """
    
    if higher_key.name.lower() != lower_key.name.lower():
        return min(higher_key.name.lower(), lower_key.name.lower()) == higher_key.name.lower()
    else:
        return True
    

# merge sort Keys alphabetically and location wise
def sort_keys(keys: list): 
    """Merge Sorts a List of Key Objects by their name

    Args:
        keys (list): A list of Key Objects

    Returns:
        list: The ordered List
    """
    
    if len(keys) > 1:
        left = sort_keys(keys[0: int(len(keys)/2)])
        right = sort_keys(keys[int(len(keys)/2): len(keys)])

        sorted_keys = []
        index_right=0
        index_left=0
        while (index_left < len(left) and index_right < len(right)):
            if compare_alphabetical(left[index_left], right[index_right]):
                sorted_keys.append(left[index_left])
                index_left += 1
            else:
                sorted_keys.append(right[index_right])
                index_right += 1

        if index_left == len(left):
            sorted_keys += right[index_right: len(right)]
        else:
            sorted_keys += left[index_left: len(left)]
        return sorted_keys

    return keys


# Methods for finding the lines of the keys in the file:

# adds the lines where the keys occur to the keys
def add_lines_to_keys(dict_file, keys, actual_dict):
    
    lines = convert_to_line_list(dict_file)
    actual_lines = convert_to_line_list(actual_dict)
    
    diff = find_difference_in_lines(lines, actual_lines)
    key_line_dict = find_keys_in_file(actual_lines, diff)
    
    for key in keys:
        if key.name in key_line_dict and len(key_line_dict[key.name]) > 0:
            # loops through the possible lines for this key and if it is the right key it
            index = 0
            while not check_key_against_line(key, key_line_dict[key.name][index], lines):
                index += 1
                if index >= len(key_line_dict[key.name]):
                    print(Configuration.ERROR_MESSAGES['key_missing_linesearch'])
                    break
            if index < len(key_line_dict[key.name]):
                key.line_name = key_line_dict[key.name][index] - 1
                key_line_dict[key.name].pop(index)
        else:
            print(Configuration.ERROR_MESSAGES['key_missing_linesearch'])

    return keys


# finds the difference in line numbers between the dictionary being generalized and the whole json file
def find_difference_in_lines(lines, actual_lines):
    diff = 1
    index = 1
    for line in lines:
        if index == len(actual_lines) - 2:
            return diff - 1
        elif line.strip() == actual_lines[index].strip():
            index += 1
        else:
            diff = diff + index
            index = 1
    
    print(Configuration.ERROR_MESSAGES['dictionary_not_found'])
    return 0 


# turns the dict into a list of strings
def convert_to_line_list(dict_file):
    json_string = json.dumps(dict_file, indent=4, separators=(", ", " : "), sort_keys=False, ensure_ascii=False)
    lines = json_string.split("\n")
    return lines
    

# find the possible keys in this file and puts the lines of the keys in a dictionary
# does not work for surftheowl files
def find_keys_in_file(lines, diff):
    
    # the start of the key that contains name of the term
    pattern_keyname = re.compile('(key|name)')
    
    key_line_dict = {}
    
    for i,line in enumerate(lines):
        # check if Kadi4Mat or VocPopuli file
        if pattern_keyname.search(line):
            name_key = (line.split(":")[1].strip())
            name_key = name_key.strip(",")
        else:
            name_key = ""
        name_key = name_key.strip('"')
        
        if name_key == '':
            continue
        elif name_key not in key_line_dict:
            key_line_dict[name_key] = [i + diff]
        else: 
            key_line_dict[name_key].append(i + diff)
            
    return key_line_dict


# checks if the key is at the given line. If it is the lines are set to it
def check_key_against_line(key: Key, line, lines):
    
    def check_correct_key(line: str, number_of_line):
        temp_line = line
        # checks if the value matches the key
        if '"value"' in temp_line:
            if type(key.value) == str and not '"' + key.value + '"' in temp_line:
                return False
            key.line_value = number_of_line
            return True
        
        # checks if unit matches the key
        if '"unit"' in temp_line:
            if key.unit == None:
                if not 'null' in temp_line:
                    return False
            elif not '"' + key.unit + '"' in temp_line:
                return False
            key.line_unit = number_of_line
            return True
        
        # checks if the datatype matches the key
        pattern_datatype = re.compile('"(datatype|type)"') 
        if pattern_datatype.search(temp_line):
            type_in_line = temp_line.strip()
            type_in_line = temp_line.split('"')[-2]
            
            if type_in_line == "":
                return True 
            if type_in_line in Configuration.DATATYPE_CONVERSION:
                type_in_line = Configuration.DATATYPE_CONVERSION[type_in_line]
                if type_in_line != key.datatype:
                    return False
            else:
                if type_in_line != key.datatype:
                    return False 
            key.line_datatype = number_of_line
        
        return True
    
    
    pattern_open_bracket = re.compile('{') 
    pattern_closed_bracket = re.compile('( )+}|},|}') 
    
    # possible last keys (vocpopuli:"children", kadi4mat:"value", )
    pattern_last_attribute = re.compile('("children"|"value")')
    
    # find beginning of key by {
    beginning = 0
    while line - beginning > 0 and not pattern_open_bracket.search(lines[line - beginning]):
        if not check_correct_key(lines[line - beginning], line - beginning):
            return False
        
        beginning += 1
    # finds ending by } or the last attribute in the key
    end = 0
    while  line + end < len(lines) - 1 and not pattern_closed_bracket.search(lines[line + end]):
        if not check_correct_key(lines[line + end], line + end):
            return False
        
        if pattern_last_attribute.search(lines[line + end]):
            end += 1
            break
        elif line + end > len(lines) - 2:
            break
        end += 1
    
    def get_lines_of_options(key: Key, lines):
        
        max_line_diff_to_options = (len(key.value) + 1) * (key.line_ending - key.line_beginning)
        key.line_value = [0] * len(key.value)
        
        for i in range(key.line_beginning, key.line_ending + max_line_diff_to_options):
            for j,option in enumerate(key.value):
                if i < len(lines) and str(option) in lines[i]:
                    key.line_value[j] = i
                    break
                
    
    # checks the last line if it matches the key
    if check_correct_key(lines[line + end], line + end):
        # sets the lines in the key
        key.set_line_in_file(line - beginning + 1, line + end + 1)
        
        if type(key.value) == list:
            get_lines_of_options(key, lines)
            
        return True
    else:
        return False
