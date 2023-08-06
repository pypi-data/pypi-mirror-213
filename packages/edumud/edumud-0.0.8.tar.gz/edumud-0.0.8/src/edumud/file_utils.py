import yaml


def load_config(config_name: str):
    """load configuration file.

    Args:
        config_name (str): config (yaml) file path and name

    Returns:
        (dict): yaml file contents
    """
    with open(config_name) as config_file:
        hp = yaml.safe_load(config_file)  # hp = house_parameters
        return hp
