import os
import re
import subprocess

from termcolor import colored


def delete_char(your_str, chars_2_replace):
    for char in chars_2_replace:
        your_str = your_str.replace(char, r'')
    return your_str


def unescape_chars(your_str, chars_2_unesc):
    for char in chars_2_unesc:
        your_str = your_str.replace(f'\\{char}', char.replace('\\', ''))
    return your_str


def get_grep_regex(sed_regex, multi_line):
    grep_regex = sed_regex.split('!')[1]
    grep_regex = delete_char(grep_regex, [r'\(', r'\)'])
    grep_regex = unescape_chars(grep_regex, ['.', ','])
    return grep_regex


def get_matches(grep_command):
    matches = subprocess.getoutput(grep_command)
    return matches.split()


def replace_in_files(repo_path, source_rel, func_name, target_rel):
    patterns = [
        # imports are preceding: from foo.bar import f1, XXX, f2
        r's!\([\s\"]*\)from {0} import \(.\+\)\, \?{1}\([a-zA-Z0-9_, ]*\)\([\s\\n\",]*\)!\1from {0} import \2\3\4\n\1from {2} import {1}\4!',

        # our import is the first one, others are following: from foo.bar import XXX, f1, f2
        r's!\([\s\"]*\)from {0} import {1}\, \?\([a-zA-Z0-9_, ]\+\)\([\s\\n\",]*\)!\1from {0} import \2\3\n\1from {2} import {1}\3!',

        # our import is the first one and the only one from foo.bar import XXX
        r's!\([\s\"]*\)from {0} import {1}\([\s\\n\", ]*\)$!\1from {2} import {1}\2!',

        # regular import, with potential aliasing
        r's!\([\s\"]*\)\(import \){0}\.{1}\(.*\)!\1\2{2}\.{1}\3!'
    ]
    multi_patterns = [
        # PARENTHESIS
        # imports are preceding: from foo.bar import (f1 \n f2, XXX, f3) of the parenthesis
        r's!\([\s\"]*\)from {0} import (\(.\+\)\,\? \?{1}\(.*\))\([\s\\n\",]*\)!n1:\1\nn2:\2\nn3:\3\nn4:\4!',

        # our import is at the middle of the parenthesis


    ]
    source_rel = re.escape(source_rel)
    target_rel = re.escape(target_rel)
    func_name = re.escape(func_name)
    print(f"\n\n* File Replacement *  for {func_name}\n")
    join_char = '\t\t\n'

    matching_files = []
    for pattern in multi_patterns:

        grep_command, _ = get_command(source_rel, target_rel,
                                      func_name, pattern, repo_path, multi_line=True)
        matches = get_matches(grep_command)
        matching_files += matches

    if len(matching_files) > 0:
        end_msg = "\n Consider fixing these imports yourself \n\n"
        alert_msg = f"!! Multi-line match in :!!\n{join_char.join(set(matching_files))}" + \
            end_msg
        print(colored(alert_msg, 'red', attrs=['bold']))

    modified_files = []
    for pattern in patterns:
        # TODO: handle multiline case with parenthesis with a python function
        # by retrieving the output of grep
        grep_command, sed_command = get_command(source_rel, target_rel,
                                                func_name, pattern, repo_path)
        # print(f"Running: {grep_command}")
        matches = get_matches(grep_command)
        modified_files += matches
        for match in matches:
            os.system(sed_command + match)
    print(
        colored(f"Modified :\n{join_char.join(set(modified_files))}", 'green'))


def get_command(source_rel, target_rel, func_name, pattern, repo_path, multi_line=False):
    sed_regex = pattern.format(source_rel, func_name, target_rel)
    grep_regex = get_grep_regex(sed_regex, multi_line)
    multi = "-z" if multi_line else ""
    grep_command = f'grep -rl {multi} --include \\*.py --include \\*.ipynb "{grep_regex}" {repo_path}'
    sed_command = f'sed -i  {multi} -e \'{sed_regex}\' '
    # command = f'grep -rl {multi} --include \\*.py --include \\*.ipynb "{grep_regex}" {repo_path} | xargs sed -i  {multi} -e \'{sed_regex}\''

    return grep_command, sed_command
