import yaml


def sequence_representer(dumper, data):
    return dumper.represent_sequence(u"tag:yaml.org,2002:seq", data, flow_style=True)


yaml.add_representer(tuple, sequence_representer)
yaml.add_representer(list, sequence_representer)


def write_yaml(filename, dct):
    """Save a dict as yaml.

    Formatting is done as follows:

    Dicts are NOT expressed in flowstyle (newlines for dictionary keys),
    but tuples and lists are done in flowstyle (inline).

    Args:
        filename: Path to file.
        dct: Dict to save.

    """

    with open(filename, "w") as outfile:
        yaml.dump(dct, outfile, default_flow_style=False)


def read_yaml(filename):
    with open(filename, "r") as stream:
        dct = yaml.safe_load(stream)

    return dct
