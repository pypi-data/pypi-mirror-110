#!/usr/bin/env python

import pdb
import re
import sys
import traceback
from copy import copy
from multiprocessing.sharedctypes import Value
from pathlib import Path

import click
from git import Repo

from src.files_op import (check_file_name_structure, clean_file,
                          get_containing_repo_dir)
from src.find_replace import replace_in_files
from src.utils import deduce_package_path, multi_startswith

DOCU_KEYS = ['"""']
D_KEYS = [' ', '\t', '\n']
IMPORT_KEYS = ['from', 'import']
BODY_KEYS = ['def', 'class', '@']
MAIN_KEYS = ["if __name__ == '__main__':", 'if __name__ == "__main__":']
VALID_KEYS = DOCU_KEYS + D_KEYS + IMPORT_KEYS + BODY_KEYS + MAIN_KEYS


class Buffer():

    def __init__(self, script_dict, indexes=None):
        # DO NOT PUT indexes=[]: it refers to the same goddamn variable
        self.name = None
        self.script_dict = script_dict
        self.indexes = [] if indexes is None else indexes

    def append_line(self, line, top=False):
        """
        Append the line to the top/bottom of the script_dict and make it part of the
        current buffer
        """
        if len(self.script_dict) == 0:
            insert_index = 0
        elif top:
            insert_index = min(self.script_dict.keys()) - 1
        else:
            insert_index = max(self.script_dict.keys())+1
        self.script_dict[insert_index] = line
        self.append(insert_index)

    def append(self, index):
        self.indexes.append(index)

    def ref_lines(self):
        return [self.script_dict[index] for index in sorted(self.indexes)]

    def print(self):
        return "".join(self.ref_lines())

    def delete(self):
        for index in self.indexes:
            # Access it via self
            del self.script_dict[index]
        self.indexes = []

    def empty(self):
        return len(self.indexes) == 0

    def copy_to(self, other_script_dict, top=False):
        """Append a copy of the lines pointed by the current buffer in the target dict
        """
        lines = copy(self.ref_lines())
        if len(other_script_dict) == 0:
            insert_index = 0
        elif top:
            insert_index = min(other_script_dict.keys()) - len(lines)
        else:
            insert_index = max(other_script_dict.keys())+1

        indexes = range(insert_index, insert_index+len(lines))

        for i, line in zip(indexes, lines):
            other_script_dict[i] = line
        return Buffer(other_script_dict, indexes)

    def migrate(self, other_script_dict, top=False):
        self.copy_to(other_script_dict, top=top)
        self.delete()

    def find_name(self):
        for line in self.ref_lines():
            if line.startswith('@'):
                continue
            else:
                if not (line.startswith('class') or line.startswith('def')):
                    raise ValueError(
                        "Line starts neither with class nor with def")
                break
        if line.startswith('class'):
            p = re.compile("class (.*?)[:\(]")
        elif line.startswith('def'):
            p = re.compile("def (.*?)\(")
        result = p.search(line)
        name = result.group(1)
        self.name = name

    def __getitem__(self, key):
        return self.script_dict[self.indexes[key]]

    def __repr__(self):
        return f"Buffer: name={self.name}" + str(self.ref_lines())


class ImportBuffer():
    def __init__(self, script_dict, script):

        script = "\n" + "".join(script)  # for regex matching
        self.script_dict = script_dict
        r1 = r'\n((?:from\s+[\.a-zA-Z0-9_]+\s+)?import[ \.\ta-zA-Z0-9_]+)'
        r2 = r'\n(from\s+[\.a-zA-Z0-9_]+\s+import \([ \n\,\ta-zA-Z0-9_]+\))'
        self.imports = re.findall(r1, script) + re.findall(r2, script)

    def copy_to(self, other_script_dict, top=True):
        if len(other_script_dict) == 0:
            insert_index = 0
        elif top:
            insert_index = min(other_script_dict.keys()) - len(self.imports)
        else:
            insert_index = max(other_script_dict.keys())+1

        indexes = range(insert_index, insert_index+len(self.imports))

        for i, line in zip(indexes, self.imports):
            other_script_dict[i] = line

    def append(self, line):
        self.imports.append(line)

    def append_line(self, line, top=True):
        """
        Append the line to the top/bottom of the script_dict and make it part of the
        current buffer
        """
        if len(self.script_dict) == 0:
            insert_index = 0
        elif top:
            insert_index = min(self.script_dict.keys()) - 1
        else:
            insert_index = max(self.script_dict.keys())+1
        self.script_dict[insert_index] = line
        self.append(line)


class FileRep():
    def __init__(self, file_path, package_path=None):
        # paths
        self.file_path = Path(file_path)
        if package_path is None:
            package_path = deduce_package_path(self.file_path, "src")
        self.package_path = package_path

        # relative path to the package
        self.rel_path = (self.package_path.name /
                         self.file_path.relative_to(package_path)).with_suffix("")
        self.package_path = package_path

        # Set the attributes
        script = self.file_path.open("r").readlines()
        script_dict, import_buffer, f_buffers = self.parse(script)
        self.script_dict = script_dict
        self.import_buffer = import_buffer
        # allows to access the buffers by name
        self.f_buffers_map = {buffer.name: buffer for buffer in f_buffers}

    def parse(self, script):
        """Parse the script passed in parameter into a file representation
        """
        # buffer for function/ class lines
        script_dict = {i: line for i, line in enumerate(script)}
        Buffer.script_dict = script_dict
        import_buffer = ImportBuffer(script_dict, script)
        f_buffers = []
        f_buffer = Buffer(script_dict)
        for i, line in script_dict.items():
            # new function/ class
            if multi_startswith(line, BODY_KEYS):
                if f_buffer.empty() or f_buffer[-1].startswith('@'):
                    f_buffer.append(i)
                    continue
                else:
                    f_buffers.append(f_buffer)
                    f_buffer = Buffer(script_dict, [i])
                    continue
            if multi_startswith(line, D_KEYS) and not f_buffer.empty():
                f_buffer.append(i)
                continue

        # Last iteration
        if not f_buffer.empty():
            f_buffers.append(f_buffer)

        # Name the functions/classes
        for f_buffer in f_buffers:
            f_buffer.find_name()
        return script_dict, import_buffer, f_buffers

    def print_functions(self):
        names = "\n".join(list(self.f_buffers_map.keys()))
        print(names)

    def linearize(self,):
        return "".join(self.get_code_lines())

    def get_code_lines(self):
        return [self.script_dict[key] for key in sorted(self.script_dict)]

    def list_funcs(self):
        return sorted(list(self.f_buffers_map.keys()))

    def migrate_func(self, func_name, other):
        # Extract the function buffer
        f_buffer = self.f_buffers_map[func_name]
        # Create a migrated copy, append the lines to the other ref dict
        migrated_buffer = f_buffer.copy_to(other.script_dict, top=False)
        other.f_buffers_map[func_name] = migrated_buffer
        # Delete the old buffer
        f_buffer.delete()
        del self.f_buffers_map[func_name]

    def send_funcs_to(self, other, func_names):
        """
        Send the functions present in func_names to another filerep instance
        """
        # we make sure the required functions are present
        if not (all([func_name in self.f_buffers_map.keys()
                     for func_name in func_names])):
            raise ValueError(
                "The requested functions are not in the source file")

        # we make sure the required functions is not present in the target directory
        if (any([func_name in other.f_buffers_map.keys()
                 for func_name in func_names])):
            raise ValueError(
                "A function is already existing in the target file")

        for func_name in func_names:
            # append the function to the other file
            self.migrate_func(func_name, other)

        # Resolving the imports
        # We resolve the external imports (pandas, numpy etc)
        self.import_buffer.copy_to(other.script_dict, top=True)

        # TODO: ideally we want to make sure that no cyclic dependency is created,
        # but this is not yet possible due to the send all/clean after policy.
        # We add potential dependencies on the local functions
        other.import_buffer.append_line(self.get_local_imports(), top=True)

        # And resolve the dependencies on the leaving functions too
        self.import_buffer.append_line(
            other.get_local_imports(function_names=func_names), top=True)

    def get_package_2_module_import_path(self):
        return '.'.join(self.rel_path.parts)

    def get_local_imports(self, function_names=None):
        """
        Return an import line for the current file importing the functions passed in parameter.
        Default to all the functions of the module.
        """
        if function_names is None:
            function_names = list(self.f_buffers_map.keys())
        else:
            assert(all([name in self.f_buffers_map.keys()
                   for name in function_names]))
        return "from {0} import {1}\n".format(self.get_package_2_module_import_path(), ', '.join(function_names))

    def write(self):
        with self.file_path.open("w") as f:
            f.write(self.linearize())


@click.option('-s', '--source_path', 'source_path', help='Source absolute or relative path', default=None)
@click.option('-t', '--target_path', 'target_path', help='Target absolute or relative path', default=None)
@click.option('-p', '--package', 'package_path', default=None)
@click.option('-e', '--elements', 'func_names', multiple=True, default=None)
@click.option('-l', '--list_funcs', 'list_path')
@click.command()
def refacto(source_path=None, target_path=None, list_path=None, func_names=None, package_path=None):
    if list_path is not None:
        list_path = Path(list_path)
        try:

            if not (source_path is None and target_path is None and func_names == ()):
                raise ValueError("-l flag has to be used on its own")
            check_file_name_structure(list_path)
            list_file_rep = FileRep(list_path, package_path=package_path)
            list_file_rep.print_functions()
            return 0
        except Exception as e:
            print(e)
            extype, value, tb = sys.exc_info()
            traceback.print_exc()
            pdb.post_mortem()

    # We use absolute path for robustness
    source_path = Path(source_path).absolute()
    target_path = Path(target_path).absolute()

    # Check the provided paths structure
    check_file_name_structure(source_path)
    check_file_name_structure(target_path)

    # Check that the git repo is the same for both source and target
    git_repo_source = get_containing_repo_dir(source_path)
    git_repo_target = get_containing_repo_dir(target_path)
    if git_repo_source != git_repo_target:
        raise ValueError("Both files are not in the same git repo")

    # Initialize the git repository
    git_repo_dir = git_repo_source
    repo = Repo(git_repo_dir)
    if repo.is_dirty():
        raise ValueError("Repo is dirty")

    #
    try:
        # Lint, sort the imports and remove the unused ones
        print("Linting files..\n")
        clean_file(source_path)
        clean_file(target_path)

        # Extract the file representations for the source and the target files
        print("Modifying source and target files..\n")

        source_file_rep = FileRep(source_path, package_path=package_path)
        target_file_rep = FileRep(target_path, package_path=package_path)

        # Execute the transfrer of functions
        source_file_rep.send_funcs_to(target_file_rep, func_names)

        # Save the changes
        target_file_rep.write()
        source_file_rep.write()

        # Similar post-refactor cleaning
        print("Linting files..\n")
        clean_file(source_path)
        clean_file(target_path)

        source_rel = source_file_rep.get_package_2_module_import_path()
        target_rel = target_file_rep.get_package_2_module_import_path()

        for func_name in func_names:
            replace_in_files(git_repo_dir, source_rel, func_name, target_rel)

        repo.git.add(update=True)
        repo.git.commit(
            '-m', f'Refactor: move {",".join(func_names)} from {source_rel} to {target_rel}')
    except Exception as e:
        print(e)
        print("An error occurred: the working tree will be reset to its initial state.")
        # if anything goes wrong, we want to recover the previous state
        repo.head.reset(index=True, working_tree=True)
        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem()
