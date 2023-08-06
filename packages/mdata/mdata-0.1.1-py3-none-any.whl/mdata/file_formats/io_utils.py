from __future__ import annotations

import io
import os
from typing import Optional


def ensure_directory_exists(path):
    dirname = os.path.dirname(path)
    if dirname != '' and not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)


def ensure_ext(path, desired_ext, override_ext=True):
    p, e = os.path.splitext(path)
    if e is None or e == '' or (override_ext and (e != desired_ext)):
        return path + desired_ext
    else:
        return path


def create_string_io(arg: str | os.PathLike[str] | bytes | io.BytesIO | io.StringIO, expected_file='.json',
                     encoding='utf-8') -> tuple[
    io.StringIO, bool]:
    source = arg
    locally_opened = False
    if isinstance(arg, bytes):
        source = io.TextIOWrapper(io.BytesIO(arg), encoding=encoding, newline='')
        locally_opened = True
    elif isinstance(arg, str | os.PathLike):
        arg = ensure_ext(arg, desired_ext=expected_file, override_ext=False)
        source = open(arg, 'r', newline='', encoding=encoding)
        locally_opened = True
    elif isinstance(arg, io.StringIO):
        source = arg
    elif isinstance(arg, io.BytesIO):
        source = io.TextIOWrapper(arg, encoding=encoding, newline='')
    return source, locally_opened


def read_csv_lines_from(arg: str | os.PathLike[str] | bytes | io.BytesIO | io.StringIO, encoding='utf-8') -> Optional[
    list[list[str]]]:
    source, locally_opened = create_string_io(arg, expected_file='.csv', encoding=encoding)
    import csv
    try:
        reader = csv.reader(source, dialect='excel')
        return [r for r in reader]
    finally:
        if locally_opened:
            source.close()


def read_json_dict_from(arg: str | os.PathLike[str] | bytes | io.BytesIO | io.StringIO, encoding='utf-8') -> Optional[
    dict]:
    source, locally_opened = create_string_io(arg, expected_file='.json', encoding=encoding)
    from json import JSONDecodeError
    try:
        import json
        return json.load(source)
    except JSONDecodeError:
        return None
    finally:
        if locally_opened:
            source.close()
