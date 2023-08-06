from kadi_apy.globals import CONFIG_PATH
import configparser
import os
from pathlib import Path

OPERATOR_PATH = Path.home().joinpath(".operatorconfig")


def Show_Kadi_Instances(*args, **kwargs):
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn('Warning! "Show_Kadi_Instances" will be renamed to '
                  '"get_instances_kadi" in a future release!',
                  DeprecationWarning)
    return get_instances_kadi(*args, **kwargs)


def get_instances_kadi():
    """_summary_

    Raises:
        KadiAPYConfigurationError: No config file was found.

    Returns:
        list: Instances saved in config file
    """
    # Config_path from:
    # https://gitlab.com/iam-cms/kadi-apy/-/blob/develop/kadi_apy/globals.py
    # CONFIG_PATH = Path.home().joinpath(".kadiconfig")

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    instances = config.sections()
    instances.pop(0)  # pop global instance
    instances.pop(0)  # pop my_kadi_instance

    return instances


def Create_Kadi_Instance(*args, **kwargs):
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn('Warning! "Create_Kadi_Instance" will be renamed to '
                  '"create_instance_kadi" in a future release!',
                  DeprecationWarning)
    return create_instance_kadi(*args, **kwargs)


def create_instance_kadi(instance: str,
                         host: str,
                         pat: str):
    """Creates a config file, if not existing,
    and creates an instance in the config file

    Args:
        instance (str): Name of the instance to be created
        host (str): fully qualified domain name of the Kadi4Mat instance
        pat (str): personal access token (PAT)
    """
    if not os.path.isfile(CONFIG_PATH):
        os.system('cmd /c "kadi-apy config create"')

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    # config.remove_section("my_kadi_instance")
    # config.sections().remove('my_kadi_instance')
    config.add_section(instance)
    config.set(instance, 'host', host)
    config.set(instance, 'pat', pat)
    with open(CONFIG_PATH, 'w+') as configfile:
        config.write(configfile)


def read_operator_config(instance):
    if os.path.isfile(OPERATOR_PATH):
        operator_config = configparser.ConfigParser()
        operator_config.read(OPERATOR_PATH)

        first_name = operator_config[instance]['First Name']
        last_name = operator_config[instance]['Last Name']
        institution = operator_config[instance]['Institution']
        user_role = operator_config[instance]['User Role']
        user_token = operator_config[instance]['User Token']
        building = operator_config[instance]['Building']
        floor = operator_config[instance]['Floor']
        room_number = operator_config[instance]['Room Number']
        institution_location = operator_config[instance]['Institution (Location)']
        tags = operator_config[instance]['Tags']
        description = operator_config[instance]['Description']
    else:
        raise FileNotFoundError("Create a config file using write_operator_config()")

    return (first_name, last_name, institution,
            user_role, user_token, building,
            floor, room_number, institution_location,
            tags, description)


def write_operator_config(operator_config):
    with open(OPERATOR_PATH, 'w+') as configfile:
        operator_config.write(configfile)
