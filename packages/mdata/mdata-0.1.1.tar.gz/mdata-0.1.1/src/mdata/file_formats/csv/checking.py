from mdata.core.raw import raw_machine_data_types
from .importing import read_raw_data, read_machine_data, read_machine_data_from_canonical_basename
from .. import io_utils
from ..validity_checking_utils import *


def is_valid_canonical_file_pair(base_path):
    try:
        read_machine_data_from_canonical_basename(base_path, validity_checking=True)
    except ValidityCheckingException:
        return False
    return True


def is_valid_file_pair(header_path, data_path):
    try:
        read_machine_data(header_path, data_path, validity_checking=True)
    except ValidityCheckingException:
        return False
    return True


def check_if_readable_header_definition_file(path):
    seen_labels = set()
    try:
        lines_from = io_utils.read_csv_lines_from(path)
    except Exception as e:
        raise MalformedHeaderFileException('Unparsable csv: ' + str(e) + '.')
    for row in lines_from:
        key = tuple(row[:2])
        if len(row) < 2:
            raise MalformedHeaderFileException('Incomplete timeseries type specification.')
        if key in seen_labels:
            raise MalformedHeaderFileException('Duplicate timeseries type specification.')
        seen_labels.add(key)
    return True


def check_if_readable_header_definition_file_json(path):
    d = io_utils.read_json_dict_from(path)
    if d is None:
        raise MalformedHeaderFileException('Unparsable json.')
    for typ in ['event-types', 'measurement-types']:
        seen_labels = set()
        if typ in d:
            for label in d[typ]:
                if label in seen_labels:
                    # json load swallows duplicates, so this can never happen
                    raise MalformedHeaderFileException('Duplicate timeseries type specification.')
                seen_labels.add(label)
                if not isinstance(d[typ][label], list):
                    raise MalformedHeaderFileException('Incomplete timeseries type specification.')
    return True


def check_if_valid_raw_header(raw_header):
    seen_labels = set()
    for key, fs in raw_header.items():
        typ, label = key
        if fs is None:
            raise MalformedHeaderFileException('Empty timeseries type specification.')
        if typ not in raw_machine_data_types:
            raise MalformedHeaderFileException('Unrecognized observation type.')
        seen_labels.add(key)
    return True


def check_if_valid_data_file(path):
    df = read_raw_data(path)
    check_if_valid_raw_data(df)
    return True


def check_if_valid_raw_data(df):
    if any(c not in df.columns for c in base_raw_machine_data_columns):
        raise MalformedDataFileException(
            f'Data is missing base column(s): {set(base_raw_machine_data_columns) - set(df.columns)}.')
    check_time_column(df)
    placeholder_cols = get_placeholder_cols(df)
    to_be_cols = gen_feature_column_names(len(placeholder_cols))
    if any(a != b for a, b in zip(placeholder_cols, to_be_cols)):
        raise MalformedDataFileException('Placeholder feature columns have unexpected labels.')
    return True
