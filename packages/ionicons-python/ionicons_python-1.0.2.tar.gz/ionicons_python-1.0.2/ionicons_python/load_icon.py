import importlib.resources as pkg_resources
from ionicons_python import icons

def load_icon(file_name):
    file_path = (pkg_resources.files(icons) / file_name)
    with open(file_path, 'r') as f:
        icon = f.read()

    return icon