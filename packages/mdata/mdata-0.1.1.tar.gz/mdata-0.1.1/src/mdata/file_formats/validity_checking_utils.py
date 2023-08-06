from mdata.core.raw import RawHeaderType, RawDataType, create_header_from_raw, gen_feature_column_names, \
    base_raw_machine_data_columns


class ValidityCheckingException(Exception):
    pass


class SyntacticValidityException(ValidityCheckingException):
    pass


class SemanticValidityException(ValidityCheckingException):
    pass


class UnsupportedHeaderFileFormat(SyntacticValidityException):
    pass


class MalformedHeaderFileException(SyntacticValidityException):
    pass


class MalformedDataFileException(SyntacticValidityException):
    pass


class InsufficientHeader(SemanticValidityException):
    pass


class InconsistentTimeseriesType(SemanticValidityException):
    pass


def get_placeholder_cols(df):
    return [c for c in df.columns if c not in base_raw_machine_data_columns]


def check_header_data_compatibility(header: RawHeaderType, data: RawDataType):
    header = create_header_from_raw(header)
    placeholder_cols = get_placeholder_cols(data)
    to_be_cols = gen_feature_column_names(len(placeholder_cols))
    for group, idx in data.groupby(['type', 'label']).groups.items():
        tpy, label = group
        if (tpy, label) not in header.feature_definitions:
            raise InsufficientHeader
        f = header.feature_definitions[tpy, label].features
        f_len = len(f)
        for i, c in enumerate(placeholder_cols):
            assert c == to_be_cols[i]
            if i < f_len:
                # type checking if possible in the future
                pass
            if i >= f_len and not data.loc[idx, c].isna().all():
                raise InconsistentTimeseriesType
    return True


def check_time_column(data: RawDataType):
    import pandas.core.dtypes.common
    if not pandas.core.dtypes.common.is_datetime64_any_dtype(data['time']):
        raise MalformedDataFileException('Time column could not be parsed as datetime')
