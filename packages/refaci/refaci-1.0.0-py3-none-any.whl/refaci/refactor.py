import ast
import itertools
import json
import os
import re
import types
from collections import defaultdict
from collections.abc import Sequence
from pathlib import Path
from typing import (
    Any,
    Callable,
    Collection,
    Generic,
    Literal,
    Mapping,
    TypeAlias,
    TypedDict,
    TypeVar,
    cast,
)

T = TypeVar("T", Path, str)
OldPath: TypeAlias = str
Alias: TypeAlias = str
NewPath: TypeAlias = str
NewAlias: TypeAlias = str


class MoveInstruction(TypedDict):
    path: NewPath
    alias: NewAlias


def refactor(
    root_dir: Path,
    imports_to_change: Mapping[OldPath, Mapping[Alias, MoveInstruction]] = types.MappingProxyType({}),
    missing_imports_to_add: Mapping[str, str] = types.MappingProxyType({}),
    replacement_dict: dict["FilePathRegex | ContentsRegex", Sequence[tuple[str, str]]] = {},
):
    dir_path_replacements = {
        regex: replacements for regex, replacements in replacement_dict.items() if isinstance(regex, DirPathRegex)
    }
    file_path_replacements = {
        regex: replacements for regex, replacements in replacement_dict.items() if isinstance(regex, FilePathRegex)
    }
    contents_re = {
        regex: replacements for regex, replacements in replacement_dict.items() if isinstance(regex, ContentsRegex)
    }

    for root, dirs, files in os.walk(root_dir):
        root = Path(root)
        dirs = [root / dir for dir in dirs]
        files = [root / file for file in files if file.endswith(".py")]

        for file in files:
            print(str(file))
            try:
                contents = file.read_text()
                file_replacements = []
                file_replacements.extend(
                    [
                        replacements
                        for regex, replacements in file_path_replacements.items()
                        if regex.pattern.search(str(file))
                    ],
                )
                file_replacements.extend(
                    [replacements for regex, replacements in contents_re.items() if regex.pattern.search(contents)],
                )
                file_replacements = tuple(itertools.chain.from_iterable(file_replacements))
                contents = refactor_imports(contents, imports_to_change, missing_imports_to_add)
                contents = globally_replace(contents, file_replacements)
                file.write_text(contents)
            except Exception as e:
                print("\033[31m" + repr(e) + "\033[0m")
        for dir in dirs:
            for regex, replacements in dir_path_replacements.items():
                if regex.pattern.search(str(dir.resolve().absolute())):
                    for replacement in replacements:
                        assert callable(replacement), "DirRegex must be a callable that accepts a dir path"
                        run_replacement(dir, replacement)


def refactor_imports(
    contents: str,
    imports_to_change: Mapping[OldPath, Mapping[Alias, MoveInstruction]] = types.MappingProxyType({}),
    missing_imports_to_add: Mapping[str, str] = types.MappingProxyType({}),
):
    tree = ast.parse(contents)
    lines = cast(list[str | list[str]], contents.splitlines())

    for node in ast.walk(tree):
        # TODO
        if isinstance(node, ast.Import):
            for alias in node.names:
                ...
        elif (
            isinstance(node, ast.ImportFrom)
            and node.module is not None
            and node.module in imports_to_change
            and node.end_lineno is not None
        ):
            replacing_lines = []
            for alias in node.names:
                if alias.name in imports_to_change[node.module]:
                    move_instruction = imports_to_change[node.module][alias.name]
                    replacing_lines.append(
                        " " * node.col_offset + f"from {move_instruction['path']} import {move_instruction['alias']}",
                    )
                else:
                    replacing_lines.append(" " * node.col_offset + f"from {node.module} import {alias.name}")
            # this trick allows us to replace without changing the number/order of lines
            lines[node.lineno - 1 : node.end_lineno] = [replacing_lines] + [[]] * (node.end_lineno - node.lineno)
    lines.insert(
        0,
        [f"from {module} import {alias}" for alias, module in missing_imports_to_add.items() if alias not in contents],
    )
    new_lines = []
    for line in lines:
        if isinstance(line, list):
            new_lines.extend(line)
        else:
            new_lines.append(line)
    return "\n".join(new_lines)


def globally_replace(contents: str, replacements: Collection[tuple[str, str] | Callable[[Path | str], str]] = ()):
    for replacement in replacements:
        contents = run_replacement(contents, replacement)
    return contents


def run_replacement(contents_or_dir_path: T, replacement: tuple[str, str] | Callable[[T], str]) -> str:
    if isinstance(contents_or_dir_path, Path):
        assert callable(replacement)

        return replacement(contents_or_dir_path)
    elif isinstance(contents_or_dir_path, str):
        if callable(replacement):
            return replacement(contents_or_dir_path)
        else:
            return contents_or_dir_path.replace(*replacement)
    else:
        raise TypeError(f"Expected Path or str, got {type(contents_or_dir_path)}")


class Compiled:
    def __init__(self, pattern: str) -> None:
        self.pattern = re.compile(pattern)


class ContentsRegex(Compiled):
    """The replacement is applied to the python file if its contents match the regex"""


class FilePathRegex(Compiled):
    """The replacement is applied to the python file if its path matches the regex"""


class DirPathRegex(Compiled):
    """The replacement is applied to the dir if its path matches the regex.

    Only function replacements are allowed
    """
