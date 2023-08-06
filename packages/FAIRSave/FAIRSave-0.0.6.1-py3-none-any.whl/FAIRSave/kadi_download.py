from kadi_apy import KadiManager
import shutil
import pprint
from FAIRSave.kadi_search import search_item_id_kadi
from typing import List, Optional


def Download_Files_from_Kadi(*args, **kwargs):
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn('Warning! "Download_Files_from_Kadi" will be renamed to '
                  '"download_files_kadi" in a future release!',
                  DeprecationWarning)
    return download_files_kadi(*args, **kwargs)


def download_files_kadi(instance: str,
                        files_path: str,
                        file_list: List,
                        unpack_zip: bool,
                        collection: Optional[str] = None,
                        collection_id: Optional[int] = None,
                        record_id: Optional[int] = None,
                        record: Optional[str] = None) -> None:

    """Download files from a record on Kadi4Mat

    Args:
        Instance: The name of the instance to use in combination with a config file.
        files_path: Path to store the downloaded files
        file_list: List of files to download from record
        unpack_zip: Boolean to indicate whether the zip files should be unpacked or not.
        collection: Title of collection to search the record in. Defaults to None.
        collection_id: ID of collection to search the record in. Defaults to None.
        record_id: ID of the record to download files from. Defaults to None.
        record: Title of record to download files from. Defaults to None.
    """

    # Create Manager with configuration instance
    manager = KadiManager(instance=instance)

    if collection is not None:
        collection_id = search_item_id_kadi(instance=instance,
                                            title=record,
                                            item='record',
                                            collection=collection)

    if record is not None:
        record_id = search_item_id_kadi(instance=instance,
                                        title=record,
                                        item='record',
                                        collection=collection)

    record = manager.record(id=record_id)

    # Path to store the files for Matlab
    for file in file_list:
        file_id = record.get_file_id(file)
        record.download_file(file_id, files_path + '/' + file)

        # unzip the zip folder to acccess the position data files
        if unpack_zip == 'True':  # True is not a boolean in this case, its a string from matlab
            if file.endswith('.zip'):
                shutil.unpack_archive(files_path + '/' + file,
                                      files_path + '/' + file.strip('.zip'),
                                      'zip')


def Kadi_Metadata(*args, **kwargs):
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn('Warning! "Kadi_Metadata" will be renamed to '
                  '"download_metadata_kadi" in a future release!',
                  DeprecationWarning)
    return download_metadata_kadi(*args, **kwargs)


def download_metadata_kadi(instance: str,
                           file_path: Optional[str] = None,
                           record_id: Optional[int] = None,
                           record: Optional[str] = None,
                           collection: Optional[str] = None) -> dict:
    """Prints the Metadata of a record to a text file.

    Args:
        Instance: The name of the instance to use in combination with a config file.
        file_path: Path to store the metadata.txt. Defaults to None.
        save_as_txt: Is either False for not saving the metadata as txt file or True for saving.
        record_id: ID of the record to get metadata from. Defaults to None.
        record: Name of the record. Defaults to None.
        collection: Collection to the record in. Defaults to None.
    """

    if record is not None:
        record_id = search_item_id_kadi(instance=instance, title=record,
                                        item='record', collection=collection)

    metadata = KadiManager(instance=instance).record(id=record_id).meta

    with open(file_path + '/' + record_id + '.txt', 'w+') as f:
        pprint.pprint(metadata, indent=4, stream=f)

    return metadata
