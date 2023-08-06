import FAIRSave.kadi_download
import FAIRSave.kadi_instances
import FAIRSave.kadi_record
import FAIRSave.kadi_template
import FAIRSave.kadi_search


class ELNManager:
    """
    A "template" class which can be used to repurpose the functions
    used in FS-Utilities for working with Kadi4Mat.
    """
    # Download functions
    def download_files(self):
        raise NotImplementedError

    def download_metadata(self):
        raise NotImplementedError

    # Instances control
    def get_instances(self):
        raise NotImplementedError

    def create_instance(self):
        raise NotImplementedError

    # Record manipulation
    def create_record(self):
        raise NotImplementedError

    def record_add_tags(self):
        raise NotImplementedError

    def record_add_metadata(self):
        raise NotImplementedError

    # Template manipulation
    def create_template(self):
        raise NotImplementedError

    # Search functions
    def search_item_titles_kadi(self):
        raise NotImplementedError

    def search_item_id(self):
        raise NotImplementedError

    def search_files(self):
        raise NotImplementedError


class KadiELNManager(ELNManager):
    """
    An example of using the ELNManager with the functions already present
    """
    # Download functions
    def download_files(self, *args, **kwargs):
        return FAIRSave.kadi_download.download_files_kadi(*args, **kwargs)

    def download_metadata(self, *args, **kwargs):
        return FAIRSave.kadi_download.download_metadata_kadi(*args, **kwargs)

    # Instances control
    def get_instances(self, *args, **kwargs):
        return FAIRSave.kadi_instances.get_instances_kadi(*args, **kwargs)

    def create_instance(self, *args, **kwargs):
        return FAIRSave.kadi_instances.create_instance_kadi(*args, **kwargs)

    # Record manipulation
    def create_record(self, *args, **kwargs):
        return FAIRSave.kadi_record.create_record_kadi(*args, **kwargs)

    def record_add_tags(self, *args, **kwargs):
        return FAIRSave.kadi_record.record_add_tags_kadi(*args, **kwargs)

    def record_add_metadata(self, *args, **kwargs):
        return FAIRSave.kadi_record.record_add_metadata_kadi(*args, **kwargs)

    # Template manipulation
    def create_template(self, *args, **kwargs):
        return FAIRSave.kadi_template.create_template_kadi(*args, **kwargs)

    # Search functions
    def search_item_titles_kadi(self, *args, **kwargs):
        return FAIRSave.kadi_search.search_item_titles_kadi(*args, **kwargs)

    def search_item_id(self, *args, **kwargs):
        return FAIRSave.kadi_search.search_item_id_kadi(*args, **kwargs)

    def search_files(self, *args, **kwargs):
        return FAIRSave.kadi_search.search_files_kadi(*args, **kwargs)
