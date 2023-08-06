import csv
import json

from mdata.core import machine_data_def as mdd
from mdata.core import raw
from mdata.file_formats import io_utils
from .shared import mk_filename_pair


def write_raw_header(path, header: raw.RawHeaderType):
    io_utils.ensure_directory_exists(path)
    path = io_utils.ensure_ext(path, '.csv')
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for (tpy, label), attributes in header.items():
            row = [tpy, label] + list(attributes)
            writer.writerow(row)


def write_raw_header_json(path, header: raw.RawHeaderType):
    io_utils.ensure_directory_exists(path)
    path = io_utils.ensure_ext(path, '.json')
    with open(path, 'w') as file:
        res = {'event-types': {}, 'measurement-types': {}}
        for tt_key, fs in header.items():
            if tt_key[0] == raw.MACHINE_DATA_TYPES_DICT[raw.MachineDataTypes.E]:
                res['event-types'][tt_key[1]] = list(fs)
            elif tt_key[0] == raw.MACHINE_DATA_TYPES_DICT[raw.MachineDataTypes.M]:
                res['measurement-types'][tt_key[1]] = list(fs)
        json.dump(res, file)


def write_raw_data(path, df: raw.RawDataType):
    io_utils.ensure_directory_exists(path)
    path = io_utils.ensure_ext(path, '.csv')
    df.to_csv(path, index=False)


def write_machine_data(path, md: mdd.MachineData, header_type='csv'):
    header_file, data_file = mk_filename_pair(path, header_type=header_type)
    raw_header = raw.convert_to_raw_header(md)
    if header_type == 'csv':
        write_raw_header(header_file, raw_header)
    elif header_type == 'json':
        write_raw_header_json(header_file, raw_header)
    write_raw_data(data_file, raw.convert_to_raw_data(md))


def write_header_only(path, md: mdd.MachineData, header_type='csv'):
    header_file, _ = mk_filename_pair(path, header_type=header_type)
    raw_header = raw.convert_to_raw_header(md)
    if header_type == 'csv':
        write_raw_header(header_file, raw_header)
    elif header_type == 'json':
        write_raw_header_json(header_file, raw_header)


def write_data_only(path, md: mdd.MachineData):
    _, data_file = mk_filename_pair(path)
    write_raw_data(data_file, raw.convert_to_raw_data(md))
