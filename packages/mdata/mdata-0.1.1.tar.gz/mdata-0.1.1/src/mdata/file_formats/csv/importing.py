import json
import os.path
from typing import Literal

import pandas as pd

from mdata.core import machine_data_def as mdd
from mdata.core import raw
from mdata.file_formats import io_utils
from mdata.file_formats.csv.shared import mk_filename_pair


def read_raw_data(path) -> raw.RawDataType:
    # path = ensure_ext(path, '.csv', override_ext=False)
    df = pd.read_csv(path)
    df[raw.COLUMN_NAME_DICT[raw.MDConcepts.Time]] = pd.to_datetime(
        df[raw.COLUMN_NAME_DICT[raw.MDConcepts.Time]])
    return df


def read_machine_data(header_path, data_path, validity_checking=True, header_type: Literal['infer', 'csv', 'json']='infer') -> mdd.MachineData:
    if header_type == 'infer':
        header_type = os.path.splitext(header_path)[1][1:]
    if header_type not in ['csv', 'json']:
        from mdata.file_formats.validity_checking_utils import UnsupportedHeaderFileFormat
        raise UnsupportedHeaderFileFormat(header_type)
    if validity_checking:
        if header_type == 'csv':
            from .checking import check_if_readable_header_definition_file
            check_if_readable_header_definition_file(header_path)
        if header_type == 'json':
            from .checking import check_if_readable_header_definition_file_json
            check_if_readable_header_definition_file_json(header_path)

    raw_header: raw.RawHeaderType = None
    if header_type == 'csv':
        raw_header = read_raw_header(header_path)
    elif header_type == 'json':
        raw_header = read_raw_header_json(header_path)

    if validity_checking:
        from .checking import check_if_valid_raw_header
        check_if_valid_raw_header(raw_header)

    raw_data = read_raw_data(data_path)

    if validity_checking:
        from .checking import check_if_valid_raw_data
        from mdata.file_formats.validity_checking_utils import check_header_data_compatibility
        check_if_valid_raw_data(raw_data)
        check_header_data_compatibility(raw_header, raw_data)

    return raw.create_machine_data_from_raw(raw_data, raw_header)


def read_machine_data_from_canonical_basename(basepath, validity_checking=True, header_type: Literal['csv', 'json']='csv') -> mdd.MachineData:
    header_file, data_file = mk_filename_pair(basepath, header_type=header_type)
    return read_machine_data(header_file, data_file, validity_checking=validity_checking, header_type=header_type)


def read_raw_header_json(path) -> raw.RawHeaderType:
    d = io_utils.read_json_dict_from(path)
    res = {}
    if 'event-types' in d:
        for et, fs in d['event-types'].items():
            res[raw.MACHINE_DATA_TYPES_DICT[raw.MachineDataTypes.E], et] = tuple(fs)
    if 'measurement-types' in d:
        for mt, fs in d['measurement-types'].items():
            res[raw.MACHINE_DATA_TYPES_DICT[raw.MachineDataTypes.M], mt] = tuple(fs)
    return res


def read_raw_header(path) -> raw.RawHeaderType:
    metadata = {}
    for row in io_utils.read_csv_lines_from(path):
        metadata[row[0], row[1]] = tuple(row[2:]) if len(row) > 2 else []
    return metadata
