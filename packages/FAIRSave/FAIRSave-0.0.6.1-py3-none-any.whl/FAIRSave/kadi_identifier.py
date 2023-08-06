from kadi_apy import KadiManager
import uuid
from FAIRSave.kadi_search import search_item_id_kadi
import math
import itertools
from typing import Optional, List
import re


def is_valid_identifier(identifier_to_test: str) -> bool:
    pattern = "[a-z]{3}-[a-z]{3}-[0-9a-z]{4}-[0-9a-z]{8}-[0-9a-z]{4}-4[0-9a-z]{3}-[89ab][0-9a-z]{3}-[0-9a-z]{12}"
    prog = re.compile(pattern)
    if prog.match(identifier_to_test):
        return True
    else:
        return False


def Kadi_not_UUID_identifiers(*args, **kwargs):
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn('Warning! "Kadi_not_UUID_identifiers" will be renamed to '
                  '"get_non_uuid_identifiers_kadi" in a future release!',
                  DeprecationWarning)
    return get_non_uuid_identifiers_kadi(*args, **kwargs)


def get_non_uuid_identifiers_kadi(instance: str,
                                  collection_title: Optional[str] = None,
                                  collection_id: Optional[str] = None) -> List:
    """This function should find all identifiers that are not UUID."""

    if collection_title is not None:
        collection_id = search_item_id_kadi(instance=instance,
                                            title=collection_title,
                                            item='collection')

    searchresource = KadiManager(instance=instance).search_resource()
    search_results = searchresource.search_items(item='record',
                                                 collection=collection_id,
                                                 per_page=100)
    total_items = search_results.json()['_pagination'].get('total_items')
    per_page = search_results.json()['_pagination'].get('per_page')

    tuples = []
    for n in range(math.ceil(total_items / per_page)):
        var = searchresource.search_items(item='record',
                                          collection=collection_id,
                                          per_page=100,
                                          page=n+1).json().get('items')
        identifier_id_tuple = [(x['title'], x['identifier'], x['id'])
                               for x in var
                               if not is_valid_identifier(x['identifier'])]
        tuples.append(identifier_id_tuple)

    list_of_tuples = list(itertools.chain.from_iterable(tuples))

    return list_of_tuples


def Kadi_replace_identifier_with_UUID(*args, **kwargs):
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn('Warning! "Kadi_replace_identifier_with_UUID" will be renamed to '
                  '"replace_identifier_uuid_kadi" in a future release!',
                  DeprecationWarning)
    return replace_identifier_uuid_kadi(*args, **kwargs)


def replace_identifier_uuid_kadi(instance: str,
                                 collection_title: Optional[str] = None,
                                 collection_id: Optional[str] = None):
    if collection_title is not None:
        collection_id = search_item_id_kadi(instance=instance,
                                            title=collection_title,
                                            item='collection')

    identifier_id_tuples = get_non_uuid_identifiers_kadi(instance=instance,
                                                         collection_id=collection_id)

    for title, identifier, id in identifier_id_tuples:
        record = KadiManager(instance=instance).record(id=id)
        identifier_uuid = str(uuid.uuid4())

        # First two words in record title are shortened to 3 chars
        record_name_words = title.split(' ')[:2]
        identifier_text = '-'.join((record_name_word[:3]
                                    for record_name_word in record_name_words))
        record_number = title[-4:]
        new_identifier = (identifier_text + '-' + record_number + '-' + identifier_uuid).lower()
        record.edit(identifier=new_identifier).json()
