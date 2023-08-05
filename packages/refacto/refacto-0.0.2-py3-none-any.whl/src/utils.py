

def multi_startswith(your_str, keys):
    """Check whether yout_str starts with one of the provided keys

    Args:
        your_str (str): query string
        keys (list of str): possible starts
    """
    return any([your_str.startswith(key) for key in keys])


def reassemble(*args):
    """Join all the strings present in the arguments into a single string

    Returns:
        list of list of string: list containing the text to concatenate
    """
    return "".join("".join(arg) for arg in args)


def flatten(your_list):
    """Flatten the list of list of elements into a list of element

    Args:
        your_list ([list of list of elements]): list to be flatten

    Returns:
        [list of el]: flattened list
    """
    return [item for sublist in your_list for item in sublist]


def deduce_package_path(file_path, package_name):
    for parent in file_path.parents:
        if parent.name == package_name:
            return parent
    raise ValueError(f"File {file_path} has no parent named {package_name}")
