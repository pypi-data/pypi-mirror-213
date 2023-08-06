from __future__ import annotations

import itertools
from typing import TypedDict

import pandas as pd

from mdata.core.machine_data_def import MDConcepts, TimeseriesTypeFactory, only_feature_columns, \
    TimeseriesCollectionFactory, EventTimeseriesCollection, MachineData, MeasurementTimeseriesCollection, \
    MachineDataTypes, build_shared_index
from mdata.core.raw import create_machine_data_from_raw, RawHeaderType, RawDataType


def ets_from_df(df: pd.DataFrame, **kwargs):
    return ts_from_df(df, type=MachineDataTypes.E, **kwargs)


def mts_from_df(df: pd.DataFrame, **kwargs):
    return ts_from_df(df, type=MachineDataTypes.M, **kwargs)


def ts_from_df(df: pd.DataFrame, **kwargs):
    def match_spec_and_df(concept, col_idx):
        spec = kwargs.get(concept)
        if concept not in df.columns:
            assert spec is not None
            df.insert(col_idx, concept, spec)
        else:
            df_type = df.iloc[0][concept]
            assert spec is None or spec == df_type
            spec = df_type
        return spec

    if MDConcepts.Time in kwargs:
        spec_time = kwargs[MDConcepts.Time]
        # if spec_time == 'artificial':
        from mdata.core import df_utils
        df.insert(0, MDConcepts.Time, df_utils.create_artificial_daterange(df))
    spec_object = match_spec_and_df(MDConcepts.Object, 1)
    spec_type = match_spec_and_df(MDConcepts.Type, 2)
    spec_label = match_spec_and_df(MDConcepts.Label, 3)

    tt_cls = TimeseriesTypeFactory.for_name(spec_type)
    features = only_feature_columns(df.columns)
    tt = tt_cls(spec_label, tuple(features))
    return TimeseriesCollectionFactory.for_type(tt)(df)


SeriesSpec = TypedDict('SeriesSpec',
                       {'df': pd.DataFrame, MDConcepts.Object: str, MDConcepts.Time: str, MDConcepts.Label: str},
                       total=False)


def machine_data_from_spec(*series_defs: SeriesSpec, sort_by_time=True, **kwargs):
    ets, mts = [], []
    for sd in series_defs:
        assert 'df' in sd
        tsc = ts_from_df(**sd)
        if isinstance(tsc, EventTimeseriesCollection):
            ets.append(tsc)
        elif isinstance(tsc, MeasurementTimeseriesCollection):
            mts.append(tsc)

    index_frame = build_shared_index(itertools.chain(ets, mts), sort_by_time=sort_by_time, **kwargs)
    return MachineData(ets, mts, index_frame)


def machine_data_from_df(df: RawDataType, header: RawHeaderType):
    return create_machine_data_from_raw(df, header)
