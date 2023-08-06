from kadi_apy import KadiManager
from kadi_apy.globals import CONFIG_PATH
import re
from typing import Optional, List
import  requests
import configparser


def Search_Item_Titles(*args, **kwargs):
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn('Warning! "Search_Item_Titles" will be renamed to '
                  '"search_item_titles_kadi" in a future release!',
                  DeprecationWarning)
    return search_item_titles_kadi(*args, **kwargs)


def search_item_titles_kadi(instance: str,
                            item: str,
                            keywords: Optional[str] = None,
                            title: Optional[str] = None,
                            tags: Optional[str] = None,
                            description: Optional[str] = None,
                            record_type: Optional[str] = None,
                            collection_id: Optional[int] = None,
                            collection: Optional[str] = None,
                            visibility: Optional[str] = 'private') -> List[str]:

    """Search for Items.

    Args:
        instance: The name of the instance to use in combination with a config file.
        item: item: The resource type defined either as string or class.
        keywords: Words in title or tags to search for. Defaults to None.
        title: Words in title to search for. Defaults to None.
        tags: Words in tags to search for. Defaults to None.
        description: Words in description to search for. Defaults to None.
        record_type: Type of record to search for. Defaults to None.
        colection_id: ID of collection to search in. Defaults to None.
        collection: Name of collection to search in. Defaults to None.

    Returns:
        list: List of titles of items found in Kadi4Mat.
    """
    # Replace empty strings with None
    if keywords == "":
        keywords = None
    if title == "":
        title = None
    if tags == "":
        tags = None
    if description == "":
        description = None

    if collection is not None:
        collection_id = search_item_id_kadi(instance,
                                            title=collection,
                                            item='collection')

    sr = KadiManager(instance=instance).search_resource()

    search_results = (sr.search_items(item=item,
                                      type=record_type,
                                      collection=collection_id,
                                      per_page=100,
                                      visibility=visibility))
    pages = search_results.json()['_pagination'].get('total_pages')

    title_list = []
    for n in range(1, pages+1):
        var = sr.search_items(item=item,
                              type=record_type,
                              collection=collection_id,
                              per_page=100,
                              page=n,
                              visibility=visibility).json().get('items')
        if keywords is not None:
            title_list += [x['title']
                           for x in var
                           if (keywords in x['title']
                               or any(keywords in s for s in x['tags'])
                               or keywords in x['plain_description'])
                           ]
        if title is not None:
            title_list += [x['title']
                           for x in var
                           if title in x['title']]
        if tags is not None:
            title_list += [x['title']
                           for x in var
                           if any(tags in s for s in x['tags'])]
        if description is not None:
            title_list += [x['title']
                           for x in var
                           if description in x['plain_description']]
        if all(x is None for x in [keywords, title, tags, description]):
            title_list += [x['title'] for x in var]

    return title_list


def Search_Item_ID(*args, **kwargs):
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn('Warning! "Search_Item_ID" will be renamed to '
                  '"search_item_id_kadi" in a future release!',
                  DeprecationWarning)
    return search_item_id_kadi(*args, **kwargs)


def search_item_id_kadi(instance: str,
                        title: str,
                        item: str,
                        collection: Optional[str] = None,
                        collection_id: Optional[int] = None,
                        record_type: Optional[str] = None,
                        visibility: Optional[str] = 'private') -> int:
    """Search for ID of item.

    Args:
        instance: The name of the instance to use in combination with a config file.
        title: Title of the record to get the ID from.
        item: The resource type defined as string.
        collection: Title of collection to search in. Defaults to None.
        collection_id: ID of collection to search in. Defaults to None.
        record_type: Type of record to search ID from. Defaults to None.

    Returns:
        int: Id of the record.
    """
    if collection is not None:
        collection_id = search_item_id_kadi(instance,
                                            title=collection,
                                            item='collection')

    sr = KadiManager(instance=instance).search_resource()
    search_results = (sr.search_items(item=item,
                                      collection=collection_id,
                                      type=record_type,
                                      title=title,
                                      per_page=100,
                                      visibility=visibility))
    pages = search_results.json()['_pagination'].get('total_pages')
    records = []
    for n in range(1, pages+1):
        page_records = sr.search_items(item=item,
                                       collection=collection_id,
                                       type=record_type,
                                       title=title,
                                       per_page=100,
                                       page=n,
                                       visibility=visibility).json().get('items')
        records = records + page_records

    title_id_tuple = [(x['title'], x['id'])
                      for x in records
                      if x['title'] == title][0]

    return title_id_tuple[1]

def search_record_from_file_kadi(instance: str,
                                 file_id: str):
    """Search for ID of record which contains a specific file.
    
    Args:
        instance: The name of the instance to use in combination with a config file.
        file_id: ID of the file whose recrd is searched.
        
    Returns:
        int: ID of the record.
    """
    
    # Get Kadi4Mat access token for API call
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    token = config[instance]['pat']
    
    # Get file response from API call
    endpoint = "https://kadi4mat.iam-cms.kit.edu/api/records/files/" + file_id
    bearer_token = "Bearer " + token
    headers = {"Authorization": bearer_token}
    file = requests.get(endpoint, headers=headers)
    
    # Read record id where file is stored from metadata
    record_id = int(file.json().get('_links').get('record').replace("https://kadi4mat.iam-cms.kit.edu/api/records/",""))
    
    return record_id


def Search_Item_Identifier(*args, **kwargs):
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn('Warning! "Search_Item_Identifier" will be renamed to '
                  '"search_item_identifier_kadi" in a future release!',
                  DeprecationWarning)
    return search_item_identifier_kadi(*args, **kwargs)


def search_item_identifier_kadi(instance: str,
                                title: str,
                                item: str,
                                collection: Optional[str] = None,
                                collection_id: Optional[int] = None,
                                record_type: Optional[str] = None,
                                visibility: Optional[str] = 'private') -> int:
    """Search for ID of item.

    Args:
        instance: The name of the instance to use in combination with a config file.
        title: Title of the record to get the ID from.
        item: The resource type defined as string.
        collection: Title of collection to search in. Defaults to None.
        collection_id: ID of collection to search in. Defaults to None.
        record_type: Type of record to search ID from. Defaults to None.

    Returns:
        int: Identifier of the record.
    """

    if collection is not None:
        collection_id = search_item_id_kadi(instance,
                                            title=collection,
                                            item='collection')

    sr = KadiManager(instance=instance).search_resource()
    search_results = (sr.search_items(item=item,
                                      collection=collection_id,
                                      type=record_type,
                                      title=title,
                                      per_page=100,
                                      visibility=visibility))
    pages = search_results.json()['_pagination'].get('total_pages')
    records = []
    for n in range(1, pages+1):
        page_records = sr.search_items(item=item,
                                       collection=collection_id,
                                       type=record_type,
                                       title=title,
                                       per_page=100,
                                       page=n,
                                       visibility=visibility).json().get('items')
        records = records + page_records
    title_identifier_tuple = [(x['title'], x['identifier'])
                      for x in records
                      if x['title'] == title][0]

    return title_identifier_tuple[1]


def Search_Files(*args, **kwargs):
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn('Warning! "Search_Files" will be renamed to '
                  '"search_files_kadi" in a future release!',
                  DeprecationWarning)
    return search_files_kadi(*args, **kwargs)


def search_files_kadi(instance: str,
                      record_id: Optional[int] = None,
                      record: Optional[str] = None):
    """Searches for files attached to a record in Kadi4Mat.

    Args:
        instance (str): The name of the instance to use in combination with a config file.
        record_id (int): ID of the record in Kadi4Mat. Defaults to None.
        record (str): Name of the record in Kadi4Mat. Defaults to None.

    Returns:
        filelist (list): List of files attached to record.
    """

    if record is None and record_id is None:
        raise ValueError('Choose a record to get files from.')

    if record is not None:
        record_id = search_item_id_kadi(instance=instance,
                                        title=record,
                                        item='record')
    record = KadiManager(instance=instance).record(id=record_id)
    pages = record.get_filelist().json()['_pagination'].get('total_pages')
    filelist = []
    for n in range(1, pages+1):
        files_in_page = (record.get_filelist(per_page=100, page=n)
                         .json()
                         .get('items'))
        filelist += [x['name'] for x in files_in_page]

    return filelist
