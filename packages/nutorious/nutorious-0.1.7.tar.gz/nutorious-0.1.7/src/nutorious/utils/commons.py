import yaml
from yaml.error import YAMLError


def mkstring(xs, sep=""):
    return sep.join(xs)


def print_(a):
    print(a, end="")


def coalsece(*values):
    for v in values:
        if v is not None:
            return v
    return None


def load_yaml_data(file_path: str):
    with open(file_path, "r") as f:
        try:
            file_data = yaml.safe_load(f)
            if file_data is None:
                file_data = {}
        except YAMLError as e:
            raise ValueError(f"Error parsing yaml file {file_path}:\n{e}")

        return file_data
