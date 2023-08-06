import re
from FAIRSave.configuration import Configuration
from FAIRSave.tools.json_reader import determine_type_of_file
from FAIRSave.tools import difference
from FAIRSave.tools.key import convert_to_line_list

metadata = []
lines_metadata = []

# determines the relevant class of the vocabulary by reading the title of a record
def determine_relevant_class(dict_1, dict_2):
    
    global metadata
    global lines_metadata
    metadata = [{}, {}]
    lines_metadata = [{}, {}]
    
    config_dict_1 = determine_type_of_file(dict_1)
    config_dict_2 = determine_type_of_file(dict_2)
    
    metadata[0] = extract_metadata(dict_1, config_dict_1)
    metadata[1] = extract_metadata(dict_2, config_dict_2)
    
    if config_dict_1 in Configuration.TYPES_VOCABULARIES and 'title' in config_dict_2:
        config_dict_1['record_title'] = dict_2[config_dict_2['title']]
        find_linked_records(dict_2, config_dict_2, dict_1, config_dict_1, 2)
    elif config_dict_2 in Configuration.TYPES_VOCABULARIES and 'title' in config_dict_1:
        config_dict_2['record_title'] = dict_1[config_dict_1['title']]
        find_linked_records(dict_1, config_dict_1, dict_2, config_dict_2, 1)
    
    lines_metadata[0] = find_metadata(dict_1, metadata[0], lines_metadata[0], config_dict_1)
    lines_metadata[1] = find_metadata(dict_2, metadata[1], lines_metadata[1], config_dict_2)
    
    # compares the found metadata
    check_licenses()
    check_record_type()
    check_linked_records()
    if config_dict_1 in Configuration.TYPES_VOCABULARIES and 'title' in config_dict_2:
        check_name(metadata[1]['title'], dict_1 ,config_dict_1, 1)
    elif config_dict_2 in Configuration.TYPES_VOCABULARIES and 'title' in config_dict_1:
        check_name(metadata[0]['title'], dict_2 ,config_dict_2, 0)
    
 
 # reads the metadata that is specified in the configuration from the json files   
def extract_metadata(file: dict, cofig_dict: dict):
    information = {}
    
    # iterates through all the possible metadata categories and tries to read them from the file
    for info in Configuration.TYPES_OF_METADATA:
        try:
            if info in cofig_dict:
                if type(cofig_dict[info]) == list:
                    relevant_part = file
                    for key in cofig_dict[info]:
                        relevant_part = relevant_part[key]
                    information[info] = relevant_part
                elif cofig_dict[info] in file:
                    information[info] = file[cofig_dict[info]]
                else:
                    difference.general_warning(Configuration.WARNING_MESSAGE['missing_metadata'] % info)
        except:
            difference.general_warning(Configuration.WARNING_MESSAGE['missing_metadata'] % info)
            
    return information


# accessor method to the metadata of the records already read
def get_metadata():
    return metadata


# finds the relations in the vocabulary and checks if the links in the records match
def find_linked_records(record: dict, key_dict: dict, vocab_dict: dict, keys_vocab: dict, file_number_record):
    global metadata
    related_terms = []
    for vocab in vocab_dict[keys_vocab['next_layer']]:
        if vocab[keys_vocab['term_name']] in keys_vocab['record_title']:
            related_terms = vocab[keys_vocab['related_vocabularies']]
 
    if 'all_linked_records' in key_dict and key_dict['all_linked_records'] in record:
        linked_records = record[key_dict['all_linked_records']]
    else: 
        return
    
    linked_records_titles = []
    for linked_record in linked_records:
        if key_dict['title'] in linked_record[key_dict['linked_record']]:
            linked_records_titles.append(linked_record[key_dict['linked_record']][key_dict['title']])
            
    if file_number_record == 1:
        metadata[0]['linked_records'] = linked_records_titles
        metadata[1]['linked_records'] = related_terms
    else:
        metadata[1]['linked_records'] = linked_records_titles
        metadata[0]['linked_records'] = related_terms
                

# checks if the same links are in the vocabulary under related and linked in the record
def check_linked_records():
    if 'linked_records' in metadata[0] and 'linked_records' in metadata[1]:
        
        relations = metadata[1]['linked_records'].copy()
        links = metadata[0]['linked_records'].copy()
        lines_relations = list(lines_metadata[1]['linked_records'])
        lines_links = list(lines_metadata[0]['linked_records'])
        
        i = 0
        j = 0
        number_links = len(links)
        number_relations = len(relations)
        for j in range(0, number_links):
            for i in range(0, number_relations):
                while j < len(links) and i < len(relations) and (relations[i] in links[j] or links[j] in relations[i]):
                    relations.pop(i)
                    links.pop(j)
                    lines_relations.pop(i)
                    lines_links.pop(j)
                if i == len(relations) - 1 and j < len(links):
                    difference.general_warning(Configuration.WARNING_MESSAGE['linked_record_unnecessary'] % links[j], line_file_1 = lines_links[j]) 

        if len(relations) > 0:
            for x, record in enumerate(relations):
                difference.general_warning(Configuration.WARNING_MESSAGE['missing_linked_records'] % record, line_file_2 = lines_links[x])


# checks if the licenses (if each file has one) of both match
def check_licenses():
    if 'license' in metadata[0] and 'license' in metadata[1]:
        warning = Configuration.WARNING_MESSAGE['license_mismatch'] % (metadata[0]['license'], metadata[1]['license'])
        if metadata[0]['license'] != metadata[1]['license']:
            if 'license' in lines_metadata[0] and 'license' in lines_metadata[1]:
                difference.general_warning(warning, line_file_1=lines_metadata[0]['license'], line_file_2=lines_metadata[1]['license'])
    
    
# checks if the record type matches (if both files have one) and if the types are an option listed in the configuration
def check_record_type():
    for i, information in enumerate(metadata):
        if "type" in information:
            if not information["type"] in Configuration.RECORD_TYPES:
                if i == 0:
                    difference.general_warning( Configuration.WARNING_MESSAGE['unknown_record_type'] % information["type"], line_file_1=lines_metadata[0]["type"])
                else:
                    difference.general_warning( Configuration.WARNING_MESSAGE['unknown_record_type'] % information["type"], line_file_2=lines_metadata[1]["type"])
    
    if 'type' in metadata[0] and 'type' in metadata[1]:
        warning = Configuration.WARNING_MESSAGE['record_type_mismatch'] % (metadata[0]['type'], metadata[1]['type'])
        if metadata[0]['type'] != metadata[1]['type']:
            difference.general_warning(warning, line_file_1=lines_metadata[0]['type'], line_file_2=lines_metadata[1]['type'])


# iterates through the dictionary and finds all the metadata that was read from the file
def find_metadata(json_dictionary, metadata_dict, lines_metadata_dict, config_dict):
    lines = convert_to_line_list(json_dictionary)
    
    for data in metadata_dict:
        for i ,line in enumerate(lines):
            if type(metadata_dict[data]) == str and metadata_dict[data] in line:
                if data in config_dict:
                    if str(config_dict[data]) in line or i > 0 and str(config_dict[data]) in lines[i - 1]:
                        lines_metadata_dict[data] = i
                else:
                    lines_metadata_dict[data] = i
                break
            elif type(metadata_dict[data]) == list:
                for p, value in enumerate(metadata_dict[data]):
                    if value in line:
                        if data not in lines_metadata_dict:
                            lines_metadata_dict[data] = [0] * len(metadata_dict[data])
                        
                        if str(config_dict['title']) in line:
                            lines_metadata_dict[data][p] = i
                            break
                        elif str(metadata_dict[data][p - 1]) in lines[i - 1] or str(metadata_dict[data][p - 1]) in lines[i + 1]:
                            lines_metadata_dict[data][p] = i
                            break
                        
    
    # all values not found are given the default value 0
    for data in metadata_dict:
        if data not in lines_metadata_dict:
            lines_metadata_dict[data] = 0
            print(Configuration.ERROR_MESSAGES['metadata_not_found_line'] % (data))

    print(lines_metadata_dict)
    return lines_metadata_dict


# checks the the title of a record for the given scheme_ class friendly name + free title + optional number
def check_name(title, dict_vocab, cofig_vocab, file_nr_title):
    name_relevant_class = ''
    for child in dict_vocab[cofig_vocab['next_layer']]:
        if child[cofig_vocab['term_name']] in title:
            name_relevant_class = child[cofig_vocab['term_name']]
            break
        
    pattern_record_title = re.compile(Configuration.REGEX_PATTERNS['record_title'] % name_relevant_class)
    if not pattern_record_title.match(title):
        if file_nr_title == 0:
            difference.general_warning(Configuration.WARNING_MESSAGE['title_mismatch'] % title, line_file_1=lines_metadata[file_nr_title]['title'])
        else:
            difference.general_warning(Configuration.WARNING_MESSAGE['title_mismatch'] % title, line_file_2=lines_metadata[file_nr_title]['title'])
        