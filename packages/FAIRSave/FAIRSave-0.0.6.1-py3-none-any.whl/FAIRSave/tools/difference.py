from FAIRSave.tools.key import Key
from FAIRSave.configuration import Configuration
import json

multiple_keys = {}
mandatory_keys_that_are_null = []
differences_unmatched_keys_file_one = []
differences_unmatched_keys_file_two = []
all_differences = []
number_of_differences = 0


class Difference:
    """
    Class that the structure for a difference found in comparing the json files. 
    It contains the different keys (key and other_key), the file it was found (file),
    the type of difference (type_of_difference) and an error message as attributes (error_message)
    """
    def __init__(self, key: Key, other_key: Key, type_of_difference, file, error_message) -> None:
        self.key = key
        self.other_key = other_key
        self.type_of_difference = type_of_difference
        self.file = file # 1/2 for the files, 0 if in both
        self.error_message = error_message
        self.all_lines = self.get_lines()
        if self.all_lines != None:
            self.lines = [self.all_lines[0], self.all_lines[2]]
        else: 
            self.lines = [0, 0]
        self.lines_with_error = self.get_lines_with_error()
        
    
    def add_line(self, line, x):
        if self.lines[x - 1] != 0:
            self.lines[x - 1].append(line)
        else: 
            self.lines[x - 1] = [line]
    
    def get_lines(self):
        """ Gets the lines from the relevant keys

        Returns:
            list: containing the lines for beginning and end in each key 
            [key file one beginning, key file one end, key file two beginning, key file two end]
        """
        if self.other_key == None and self.key != None:
            if self.file == 1:
                return [self.key.line_beginning, self.key.line_ending, 0, 0]
            elif self.file == 2:
                return [0, 0, self.key.line_beginning, self.key.line_ending]
        elif self.key == None:
            return None
        else:
            return[self.key.line_beginning, self.key.line_ending, self.other_key.line_beginning, self.other_key.line_ending]
    
    def get_line_option(self):
        if type(self.key.value) == str and type(self.other_key.value) == list:
            value = self.key.value.lower()
            options = self.other_key.value
            options = [x.lower() for x in options]
            index = options.index(value)
            return  [self.key.line_value, self.other_key.line_value[index]]
        elif type(self.key.value) == list and type(self.other_key.value) == str:
            value = self.other_key.value.lower()
            options = self.key.value
            options = [x.lower() for x in options]
            index = options.index(value)
            return [self.key.line_value[index], self.other_key.line_value]
        
    
    def get_lines_with_error(self):
        lines = [0,0]
        match self.type_of_difference:
            case 'character_case_mismatch' | 'misspelling' | 'location_mismatch':
                lines = [self.key.line_name, self.other_key.line_name]
            case 'datatype_mismatch':
                lines = [self.key.line_datatype, self.other_key.line_datatype]
            case 'internal_datatype_inconsistency':
                lines = [self.key.line_value, 0]
            case 'mandatory_value_missing' | 'mandatory_value_mismatch' | 'single_value_mismatch' | 'value_mismatch_list':
                lines = [self.key.line_value, self.other_key.line_value]
            case 'value_character_case_mismatch_list':
                lines = self.get_line_option()
            case 'unit_mismatch':
                lines = [self.key.line_unit, self.other_key.line_unit]
            case 'key_not_in_other_list' | 'mandatory_key_not_in_other_list':
                lines = [self.key.line_name, 0]

        if self.file == 2:
            return [lines[1], lines[0]]
        else: 
            return lines
    
    # adds single differences that make up this differences
    def add_single_diffs(self, differences: list):
        self.single_diffs = differences
    
    # adds a key value pair where the mistake is located (necessary for the general warnings to locate)
    def add_key_value_information(self, key, value):
        self.key_value = [key, value]
        

# access to the number of differences found
def get_number_of_differences():
    global number_of_differences
    number_of_differences = len(all_differences) + len(differences_unmatched_keys_file_one) + len(differences_unmatched_keys_file_two)
    
    if len(mandatory_keys_that_are_null) > 0:
        number_of_differences -= 1
    if len(differences_unmatched_keys_file_one) > 0:
        number_of_differences -= 1
    if len(differences_unmatched_keys_file_two) > 0:
        number_of_differences -= 1
    if len(all_differences) > 0 and type(all_differences[-1]) == dict:
        number_of_differences -= 1
    
    return number_of_differences
      
# prints all saved Differences/ Mismatches
def print_differences():
    
    for difference in all_differences:
        if difference.error_message != None and difference.type_of_difference != 'key_not_in_other_list':
            print(difference.error_message)
    
    for key in multiple_keys: 
        if multiple_keys[key] > 0:
            print(Configuration.WARNING_MESSAGE['multiple_keys'] % (key, multiple_keys[key], 1))
        elif multiple_keys[key] < 0:
            print(Configuration.WARNING_MESSAGE['multiple_keys'] % (key, -multiple_keys[key], 2))
            
    def get_names_of_diff_list(list_of_differences):
        names = []
        for diff in list_of_differences:
            if diff.key.name not in names:
                names.append(diff.key.name)
        return names

    if len(mandatory_keys_that_are_null) > 0 and 'mandatory_value_missing' in Configuration.TYPES_OF_DIFFERENCE:
        print(Configuration.WARNING_MESSAGE['mandatory_value_missing'] % get_names_of_diff_list(mandatory_keys_that_are_null))
    
    if len(differences_unmatched_keys_file_one) > 0 and 'unmatched_keys_file_one' in Configuration.TYPES_OF_DIFFERENCE:
        print(Configuration.WARNING_MESSAGE['unmatched_keys_file_one'] % get_names_of_diff_list(differences_unmatched_keys_file_one))
    
    if len(differences_unmatched_keys_file_two) > 0 and 'unmatched_keys_file_two' in Configuration.TYPES_OF_DIFFERENCE:
        print(Configuration.WARNING_MESSAGE['unmatched_keys_file_two'] % get_names_of_diff_list(differences_unmatched_keys_file_two))
    

# makes a json file from all the errors in the folder output
def export_errors_as_json(filename_one: str, filename_two: str):
    
    list_of_error_dicts = []
    
    for diff in all_differences:
        
        if type(diff) != Difference:
            continue
        elif diff.type_of_difference in ['unmatched_keys_file_one', 'unmatched_keys_file_two', 'all_mandatory_value_missing']:
            continue
        
        error_dict = {}
        error_dict["message"] = diff.error_message
        error_dict["type"] = Configuration.TYPES_OF_DIFFERENCE[diff.type_of_difference] 
        error_dict["filenames"] = [filename_one, filename_two]
        
        # gets the lines where the term begins in each file
        if diff.lines == None:
            error_dict["lines"] = [0, 0]
        else:
            error_dict["lines"] = [diff.lines[0], diff.lines[1]]
        
        if diff.key != None:
            error_dict["key"] = diff.key.name 
        
        list_of_error_dicts.append(error_dict)

    # Serializing json
    json_object = json.dumps(list_of_error_dicts, indent=4)
 
    # Writing to error file
    with open(f"output/errors_{filename_one}_{filename_two}.json", "w") as file:
        file.write(json_object)

        
        
# accessor method to the list containing all found differences
def get_all_differences():
    """Accessor method to all the differences found during the validation.
    Function should only be called after the comparison processes are done.

    Returns:
        list: list of all differences
        index -1 has all the multiple keys stored in a dictionary with the name as its key and the difference in 
        numbers as value
    """
    global all_differences
   
    if len(differences_unmatched_keys_file_one) > 0 and 'unmatched_keys_file_one' in Configuration.TYPES_OF_DIFFERENCE:
        unmatched_keys_one = Difference(None, None, 'unmatched_keys_file_one', 1, Configuration.WARNING_MESSAGE['keys_not_in_1'])
        unmatched_keys_one.add_single_diffs(differences_unmatched_keys_file_one)
        all_differences.append(unmatched_keys_one)
        
    if len(differences_unmatched_keys_file_two) > 0 and 'unmatched_keys_file_two' in Configuration.TYPES_OF_DIFFERENCE:
        unmatched_keys_two = Difference(None, None, 'unmatched_keys_file_two', 2, Configuration.WARNING_MESSAGE['keys_not_in_2'])
        unmatched_keys_two.add_single_diffs(differences_unmatched_keys_file_two)
        all_differences.append(unmatched_keys_two)
        
    if len(mandatory_keys_that_are_null) > 0 and 'all_mandatory_value_missing' in Configuration.TYPES_OF_DIFFERENCE:
        diff_missing_mandatory_values = Difference(None, None, 'all_mandatory_value_missing', 0, Configuration.WARNING_MESSAGE['mandatory_value_missing'] % '')
        diff_missing_mandatory_values.add_single_diffs(mandatory_keys_that_are_null)
        all_differences.append(diff_missing_mandatory_values)
        
    all_differences.append(multiple_keys)
    return all_differences


# general warnings that are independent from the keys
def general_warning(warning_message: str, key = None, value = None, line_file_1 = 0, line_file_2 = 0):
    if 'general_warning' in Configuration.TYPES_OF_DIFFERENCE:
        diff = Difference(None, None, 'general_warning', 0, warning_message)
        all_differences.append(diff)
        if key != None or value != None:
            diff.add_key_value_information(key, str(value))
        if line_file_1 != 0 or line_file_2 != 0:
            diff.add_line(line_file_1, 1)
            diff.add_line(line_file_1, 2)
            diff.lines_with_error = [line_file_1, line_file_2]


# different capitalized letters
def character_case_mismatch(key: Key, other_key: Key):
    if 'character_case_mismatch' in Configuration.TYPES_OF_DIFFERENCE:
        all_differences.append(Difference(key, other_key, 'character_case_mismatch', 0, 
            Configuration.WARNING_MESSAGE['character_case_mismatch'] % (key.name, other_key.name)))


# datatypes of the same key are different
def datatype_mismatch(key: Key, other_key: Key):
    if 'datatype_mismatch' in Configuration.TYPES_OF_DIFFERENCE:
        all_differences.append(Difference(key, other_key, 'datatype_mismatch', 0, 
            Configuration.WARNING_MESSAGE['datatype_mismatch'] % (key.name, key.datatype, other_key.datatype)))


# value does not match datatype
def internal_datatype_inconsistency(key: Key, file):
    if 'internal_datatype_inconsistency' in Configuration.TYPES_OF_DIFFERENCE:
        all_differences.append(Difference(key, None, 'internal_datatype_inconsistency', file, 
            Configuration.WARNING_MESSAGE['internal_datatype_inconsistency'] % (key.name, key.value, key.datatype)))


# handles it if key more often in one file than the other
def key_more_often_in_list(key: Key, x):
    if key.name.lower() in multiple_keys:
        if x == 1:
            multiple_keys[key.name.lower()] += 1
        else:
            multiple_keys[key.name.lower()] -= 1 
    else:
        if x == 1:
            multiple_keys[key.name.lower()] = 1
        else:
            multiple_keys[key.name.lower()] = -1 


# key not on the other (x) file
def key_not_in_other_list(key: Key, x):
    """ Difference if one key does not exist in one file
    Args:
        key (Key): key in question
        x (int): the number of the file where the key is not in
    """
    if key.mandatory and 'mandatory_key_not_in_other_list' in Configuration.TYPES_OF_DIFFERENCE:
        all_differences.append(Difference(key, None, 'mandatory_key_not_in_other_list', 3 - x, 
            Configuration.WARNING_MESSAGE['mandatory_key_not_in_other_list'] % (key.name, x)))
    else:
        diff_missing_key = Difference(key, None, 'key_not_in_other_list', 3 - x,
                Configuration.WARNING_MESSAGE['key_not_in_other_list'] % (key.name, x))
        if x == 2:
            differences_unmatched_keys_file_one.append(diff_missing_key)
        elif x == 1:
            differences_unmatched_keys_file_two.append(diff_missing_key)
        if 'key_not_in_other_list' in Configuration.TYPES_OF_DIFFERENCE:
            all_differences.append(diff_missing_key)
            

# both sides don't have a value assigned despite being mandatory
def mandatory_value_missing(key: Key, other_key: Key):
    if 'mandatory_value_missing' in Configuration.TYPES_OF_DIFFERENCE:
        diff_mandatory_missing = Difference(key, other_key, 'mandatory_value_missing', 0, 
            Configuration.WARNING_MESSAGE['mandatory_value_missing'] % key.name)
        mandatory_keys_that_are_null.append(diff_mandatory_missing)
        all_differences.append(diff_mandatory_missing)

# both keys are spelled differently (more mistakes than just capital letters)
def misspelling(key: Key, other_key: Key):
     if 'misspelling' in Configuration.TYPES_OF_DIFFERENCE:
        all_differences.append(Difference(key, other_key, 'misspelling', 0, 
            Configuration.WARNING_MESSAGE['misspelling'] % (key.name, other_key.name)))

# key was found at a different location
def location_mismatch(key: Key, other_key: Key):
    if 'location_mismatch' in Configuration.TYPES_OF_DIFFERENCE:
        all_differences.append(Difference(key, other_key, 'location_mismatch', 0, 
            Configuration.WARNING_MESSAGE['location_mismatch'] % (key.name, key.broader_terms, other_key.broader_terms)))

# mandatory key has different values
def mandatory_value_mismatch(key: Key, other_key: Key):
    if 'mandatory_value_mismatch' in Configuration.TYPES_OF_DIFFERENCE:
        all_differences.append(Difference(key, other_key, 'mandatory_value_mismatch', 0, 
            Configuration.WARNING_MESSAGE['mandatory_value_mismatch'] % (key.name, key.value, other_key.value)))


# two keys do not have the same value
def single_value_mismatch(key: Key, other_key: Key):
    if 'single_value_mismatch' in Configuration.TYPES_OF_DIFFERENCE:
        all_differences.append(Difference(key, other_key, 'single_value_mismatch', 0, 
            Configuration.WARNING_MESSAGE['single_value_mismatch'] % (key.name, key.value, other_key.value)))


# value is not in the possible options
def value_mismatch_list(key: Key, other_key:Key, x, value):
    if 'value_mismatch_list' in Configuration.TYPES_OF_DIFFERENCE:
        all_differences.append(Difference(key, other_key, 'value_mismatch_list', x, 
            Configuration.WARNING_MESSAGE['value_mismatch_list'] % (key.name, value)))
    

# the value of a key has different capital letters than the option
def value_character_case_mismatch(key: Key, other_key: Key, value, option):
    if 'value_character_case_mismatch_list' in Configuration.TYPES_OF_DIFFERENCE:
        all_differences.append(Difference(key, other_key, 'value_character_case_mismatch_list', 0, 
            Configuration.WARNING_MESSAGE['value_character_case_mismatch_list'] % (key.name, value, option)))


# same key has different units
def unit_mismatch(key: Key, other_key: Key):
    if 'unit_mismatch' in Configuration.TYPES_OF_DIFFERENCE:
        all_differences.append(Difference(key, other_key, 'unit_mismatch', 0, 
            Configuration.WARNING_MESSAGE['unit_mismatch'] % (key.name, key.unit, other_key.unit)))


# resets all the global variables, should be done before each comparison
def reset():
    global multiple_keys
    global mandatory_keys_that_are_null
    global all_differences
    global differences_unmatched_keys_file_one
    global differences_unmatched_keys_file_two
    differences_unmatched_keys_file_one = []
    differences_unmatched_keys_file_two = []
    multiple_keys = {}
    mandatory_keys_that_are_null = []
    all_differences = []
    
    # resetting the configuration dictionaries
    possible_entries = ['record_title', 'needed_links']
    for key_dict in Configuration.TYPES_OF_JSON_FILES:
        for entry in possible_entries:
            key_dict.pop(entry, None)
            
