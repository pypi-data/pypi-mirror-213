from typing import Dict, List, Optional
from collections import defaultdict
import os
import sys
import re


FileContent = str
Filename = str
Pathname = str
VariableName = str


def find_python_filenames(paths: List[Pathname]):
    """Recursively searches for Python filenames in provided paths."""
    filenames = []
    for path in paths:
        if os.path.isfile(path):
            if os.path.splitext(path)[1] == ".py":
                filenames.append(path)
        else:
            filenames += [os.path.join(dp, f) for dp, dn, filenames in os.walk(path)
                          for f in filenames if os.path.splitext(f)[1] == ".py"]
    return filenames


def read_files(filenames: List[Filename]) -> Dict[Filename, FileContent]:
    files = {}
    for filename in filenames:
        with open(filename, "r") as f:
            files[filename] = f.read()
    return files


def parse_global_names(files: Dict[Filename, FileContent]) -> Dict[VariableName, Filename]:
    patterns = [r"^(\w+)\s*=", r"^def\s+(\w+)\s*\(?", r"^class\s+(\w+)\s*\(?:?"]

    global_variable_names = {}
    for filename, file_content in files.items():
        for pattern in patterns:
            global_variable_names_in_file = re.findall(pattern, file_content, re.MULTILINE)
            for name in global_variable_names_in_file:
                global_variable_names[name] = filename
    return global_variable_names


def find_unused_names(files: Dict[str, str], global_names: Dict[VariableName, Filename]
                      ) -> Dict[VariableName, Filename]:
    name_occourencies = defaultdict(int)
    for name in global_names.keys(): 
        for file_content in files.values():
            name_occourencies[name] += file_content.count(name)

    unused_variables = {name: filename for name, filename in global_names.items() if name_occourencies[name] == 1}
    return unused_variables


def print_unused_names(unused_names: Dict[VariableName, Filename]):
    # TODO: add line number to output
    print()
    for name, filename in unused_names.items():
        print(filename, "\033[91mF851\033[0m", f"Global \033[1m{name}\033[0m is never used")


def main(args: Optional[List[str]] = None) -> None:
    args = args or sys.argv[1:]

    python_filenames = find_python_filenames(paths=args)
    files = read_files(python_filenames)

    global_names = parse_global_names(files)
    unused_names = find_unused_names(files, global_names)

    print_unused_names(unused_names)


if __name__ == "__main__":
    main()
