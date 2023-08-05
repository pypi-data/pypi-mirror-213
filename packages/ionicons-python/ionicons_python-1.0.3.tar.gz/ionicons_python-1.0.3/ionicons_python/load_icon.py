import importlib.resources as pkg_resources
from ionicons_python import icons, colored_icons

def load_icon(file_name):
    file_path = (pkg_resources.files(icons) / file_name)
    with open(file_path, 'r') as f:
        icon = f.read()

    return icon


def load_color_icon(file_name):
    file_path = (pkg_resources.files(colored_icons) / file_name)
    with open(file_path, 'r') as f:
        icon = f.read()

    return icon