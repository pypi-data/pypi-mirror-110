import os
from plistlib import InvalidFileException


def check_file_name_structure(path):
    """Check the structure of the provided path

    Args:
        path (pathlib.Path): source or target path
    """
    if not path.exists():
        raise FileNotFoundError(str(path))
    if path.suffix != '.py':
        raise InvalidFileException(f"{path} is not a python file")


def iterate_parents(p):
    """Iterate on the parents of the path provided in parameter

    Args:
        p (pathlib.Path):

    Yields:
        [pathlib.Path]: parent directories
    """
    p = p.absolute()
    p = p if p.is_dir() else p.parent
    while str(p) != p.root:
        yield p
        p = p.parent


def get_containing_repo_dir(path):
    """Return the path to the lowest-level repository that contains the path
    provided in parameter. Raise an exception if no repository is found.

    Args:
        path ([type]): [description]

    Returns:
        [pathlib.Path]: directory of the closest containing git repository
    """
    for parent in iterate_parents(path):
        ls_objects = list(parent.iterdir())
        if any([obj.is_dir() and obj.name == '.git' for obj in ls_objects]):
            return parent
    raise FileNotFoundError(
        f"No git repository seems to be a parent directory of {path.absolute()}")


def format_file_imports(file_path):
    """
    Format the imports in the file pointed by path
    """
    # TODO: do not pass by a call to os system

    os.system(
        f"autoflake  --in-place  --remove-all-unused-imports {file_path.absolute()}")


def sort_file_imports(file_path):
    os.system(f"isort {file_path.absolute()}")


def lint_file(file_path):
    os.system(f"autopep8 --in-place {file_path.absolute()}")


def clean_file(file_path):
    lint_file(file_path)
    sort_file_imports(file_path)
    format_file_imports(file_path)
