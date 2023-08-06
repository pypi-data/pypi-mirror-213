class Configuration:

    # unwanted mistakes can be commented out, mismatches not in this dictionary will not be found
    # the value of the keys can be changed as needed, the key names need to stay the same
    TYPES_OF_DIFFERENCE = {
        'unmatched_keys_file_one': 'unmatched_keys_file_one',
        'unmatched_keys_file_two': 'unmatched_keys_file_two',
        'all_mandatory_value_missing': 'all_mandatory_value_missing',
        'character_case_mismatch': 'character_case_mismatch',
        'datatype_mismatch': 'datatype_mismatch',
        'general_warning': 'general_warning',
        'internal_datatype_inconsistency': 'internal_datatype_inconsistency',
        'mandatory_key_not_in_other_list': 'mandatory_key_not_in_other_list',
        'key_not_in_other_list': 'key_not_in_other_list',
        'mandatory_value_missing': 'mandatory_value_missing',
        'misspelling': 'misspelling',
        'location_mismatch': 'location_mismatch',
        'mandatory_value_mismatch': 'mandatory_value_mismatch',
        'single_value_mismatch': 'single_value_mismatch',
        'value_mismatch_list': 'value_mismatch_list',
        'value_character_case_mismatch_list': 'value_character_case_mismatch_list',
        'unit_mismatch': 'unit_mismatch',
    }

    # warning messages of the different mistake types
    WARNING_MESSAGE = {
        'character_case_mismatch': 'Warning, "%s" and "%s" have different capital letters.',
        'datatype_mismatch': 'Warning, "%s" has different datatypes: %s and %s',
        'internal_datatype_inconsistency': 'Warning, value in "%s" is "%s" but should be of type %s',
        'key_not_in_other_list': 'Warning, "%s" does not exist in the %i. file',
        'keys_not_in_1': 'Warning, following keys of the first file are not in the second file: ',
        'keys_not_in_2': 'Warning, following keys of the second file are not in the first file: ',
        'mandatory_key_not_in_other_list': 'Warning, "%s" is mandatory and does not exist in the %i. file',
        'mandatory_value_missing': 'Warning, following keys are mandatory but their values are null: %s',
        'mandatory_value_mismatch': 'Warning, mandatory Key "%s" has different values: "%s" and "%s"',
        'missing_metadata': "Warning, %s could not be found in the file at the in the configuration defined position.",
        'missing_linked_records': 'Warning, link missing in file 1: %s',
        'misspelling': 'Warning, "%s" and "%s" are spelled differently.',
        'location_mismatch': 'Warning, "%s" found at different locations: %s, %s',
        'license_mismatch': 'Warning, the licenses are different: "%s" and "%s"',
        'linked_record_unnecessary': 'Warning, link missing in file 2: %s',
        'single_value_mismatch': 'Warning, values of "%s" do not match: "%s" and "%s"',
        'record_type_mismatch': 'Warning, the record types do not match: "%s" and "%s"',
        'title_mismatch': 'Warning, title "%s" does not match the scheme.',
        'value_mismatch_list': 'Warning, value of "%s" (%s) not in the options.',
        'value_character_case_mismatch_list': 'Warning, value of "%s" (%s) has different capital letters/ is spelled differently than the option (%s)',
        'unit_mismatch': 'Warning, "%s" has different units: %s and %s',
        'multiple_keys': '--> Key "%s" is %i times more in file %i.',
        'unknown_record_type': 'Warning, the type of this record is not listed as an option in the configuration. (%s)',
        'unmatched_keys_file_one': 'Warning, following keys of the first file are not in the second file: %s',
        'unmatched_keys_file_two': 'Warning, following keys of the second file are not in the first file: %s',
    }

    # all possible occuring error messages that are not part of a warning/ mismatch
    ERROR_MESSAGES = {
        'Levenshtein': "Error, if misspelling should be found, the Levenshtein library needs to be installed.",
        'unknown_json': 'Error, Structure of Json File not recognized. (Can be added in the configuration file)',
        'incomplete_key': "Error, Key is incomplete/ cannot be read.",
        'key_missing_linesearch': "Error, Key not found or not enough lines.",
        'dictionary_not_found': "Error, dictionary could not be found.",
        'loading_file': "Error, file could not be loaded.",
        'batch_not_enough_files': "Error, at least one first file and one second file needed",
        'metadata_not_found_line': "Error, %s can not be found in the file."
    }

    # necessary regexpatterns
    REGEX_PATTERNS = {
        'record_title': '%s.*([0-9]{4}|)'
    }

    # table for the datatype conversion to standardized types
    DATATYPE_CONVERSION = {
        "str": 'string',
        "dict": 'dictionary',
        "list": 'list',
        "int": 'integer',
        "float": 'float',
        "bool": 'boolean',
        "date": 'date'
    }

    # allowed record types
    RECORD_TYPES = [
        'lab equipment',
        'industrial procedure',
        'scientific procedure',
        'data processing',
        'experimental object'
    ]

    # all the different types of metadata that can be searched for
    TYPES_OF_METADATA = [
        'license',
        'type',
        'title',
        'link'
    ]

    # the paths for the batch validation
    PATH_TO_OUTPUT = 'output'
    PATH_BATCH_INPUT_FIRST_FILE = 'batch_input/first_file/'
    PATH_BATCH_INPUT_SECOND_FILE = 'batch_input/second_file/'

    ##################################################################################################

    """
    To add new type of file:
    make dictionary where all the terms are defined like below, then add name of dictionary to all the files

    KEY_TYPE_OF_JSON = {

        # the necessary keys to get to the part that  will be searched/ converted
        'keys_to_searched_part': [""],
        'type_of_searched_part': dict / list,

        # functions needed to find the correct part to be searched for
        # unnecessary functions can be deleted
        'get_correct_list_by_name': False,

        # keys where the searched attributes are
        # 'next_layer', 'term_name' and 'datatype' need to exist, the rest is optional and can be deleted
        'next_layer': "",
        'term_name': "",
        'datatype': "",
        'unit': "",
        'value': "",
        'datatype_for_options': "",
        'validation': "",
        'options': "",
        'mandatory': "",

        # keys to metadata

    }
    """

    KEYS_VOCPOPULI = {
        'keys_to_searched_part': ['children'],
        'type_of_searched_part': list,

        # functions needed to find the correct part to be searched for
        'get_correct_list_by_name': True,

        # keys where the searched attributes are
        'next_layer': "children",
        'term_name': "name",
        'datatype': "datatype",
        'datatype_for_options': "individual",

        # keys to metadata
        'related_vocabularies': "related",
        'title': "name"

    }

    KEYS_KADI_RECORD = {
        'keys_to_searched_part': ['extras'],
        'type_of_searched_part': list,

        # functions needed to find the correct part to be searched for

        # keys where the searched attributes are
        'next_layer': "value",
        'term_name': "key",
        'datatype': "type",
        'unit': "unit",
        'value': "value",

        # keys to metadata
        'license': "license",
        'type': "type",
        'title': "title",
        'all_linked_records': 'links',
        'linked_record':  'record_to'
    }

    KEYS_KADI_TEMPLATE_TYPE_1 = {
        'keys_to_searched_part': ['data'],
        'type_of_searched_part': list,

        # functions needed to find the correct part to be searched for

        # keys where the searched attributes are
        'next_layer': "value",
        'term_name': "key",
        'datatype': "type",
        'unit': "unit",
        'value': "value",
        'validation': "validation",
        'options': "options",
        'mandatory': "required",

        # keys to metadata
        'license': "license",
        'title': "title",


    }

    KEYS_KADI_TEMPLATE_TYPE_2 = {
        'keys_to_searched_part': ['data', 'extras'],
        'type_of_searched_part': list,

        # functions needed to find the correct part to be searched for

        # keys where the searched attributes are
        'next_layer': "value",
        'term_name': "key",
        'datatype': "type",
        'unit': "unit",
        'value': "value",
        'validation': "validation",
        'options': "options",
        'mandatory': "required",

        # keys to metadata
        'license': ["data", "license"],
        'title': "title",
        'type': ['data', 'type']

    }

    # all the different dictionaries for all the types of json files
    TYPES_OF_JSON_FILES = [
        KEYS_KADI_RECORD,
        KEYS_KADI_TEMPLATE_TYPE_1,
        KEYS_KADI_TEMPLATE_TYPE_2,
        KEYS_VOCPOPULI
    ]

    # all the configuration dictionaries of vocabularies
    TYPES_VOCABULARIES = [
        KEYS_VOCPOPULI
    ]
