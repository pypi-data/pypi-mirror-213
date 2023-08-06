from __future__ import annotations

import enum
import itertools
from abc import ABC
from dataclasses import dataclass, field
from functools import partial
from typing import Iterable, Generic, TypeVar, Sized, TYPE_CHECKING, Any, Iterator, Collection, Literal, ClassVar

import numpy as np
import pandas as pd

from .df_utils import derive_categoricals
from .util import mangle_arg_to_set, mangle_arg_with_bool_fallback, mangle_arg_to_list, mangle_arg_to_tuple, \
    symmetric_difference, intersection, assert_in

if TYPE_CHECKING:
    from .raw import RawHeaderType


class MyStrEnum(enum.Enum):

    @classmethod
    def cast(cls, arg):
        return arg if isinstance(arg, cls) else cls(arg)

    def as_str(self):
        return str(self.value)


MDConcept = str


class MDConcepts(Iterable):
    Time = 'time'
    Object = 'object'
    Type = 'type'
    Label = 'label'

    base_columns = [Time, Object, Type, Label]

    def __iter__(self):
        return iter(MDConcepts.base_columns)


class MDExtensionConcepts(Iterable):
    Index = 'series_index'

    extension_columns = [Index]
    combined_columns = MDConcepts.base_columns + extension_columns

    def __iter__(self):
        return iter(MDExtensionConcepts.extension_columns)


def only_feature_columns(cols):
    return [c for c in cols if (c not in MDConcepts.base_columns) and (c not in MDExtensionConcepts.extension_columns)]


def project_on_feature_columns(df: pd.DataFrame):
    return df[only_feature_columns(df.columns)]


TimeseriesTypeKey = tuple[str, str]
TimeseriesFeatureLabel = str
TimeseriesFeatureLabels = tuple[TimeseriesFeatureLabel, ...]

MachineDataType = str


class MachineDataTypes(Iterable):
    E: MachineDataType = 'E'
    M: MachineDataType = 'M'
    base_types = [E, M]

    def __iter__(self) -> Iterator[MachineDataType]:
        return iter(MachineDataTypes.base_types)


ObservationTypeLabel = str
EventTypeLabel = str
MeasurementTypeLabel = str


TimeseriesTypeType = TypeVar('TimeseriesTypeType', bound='TimeseriesType')


@dataclass(frozen=True, unsafe_hash=True, eq=True, repr=True, init=False)
class TimeseriesType(Iterable, Sized):
    type: ClassVar[MachineDataType]
    label: ObservationTypeLabel
    features: TimeseriesFeatureLabels = field(default=())

    def __init__(self, label: ObservationTypeLabel, features: TimeseriesFeatureLabels = ()) -> None:
        super().__init__()
        object.__setattr__(self, 'label', label)
        object.__setattr__(self, 'features', features if isinstance(features, tuple) else tuple(features))

    def __iter__(self):
        return iter(self.features)

    def __len__(self):
        return len(self.features)

    def askey(self) -> TimeseriesTypeKey:
        return self.type, self.label

    def is_mergeable(self, other: TimeseriesType) -> bool:
        return (self.__class__ == other.__class__) and (self.type == other.type) and (self.label == other.label)

    def feature_intersection(self, other: TimeseriesType) -> set[str]:
        return set(self.features) & set(other.features)

    def feature_symmetric_difference(self, other: TimeseriesType) -> tuple[set[str], set[str]]:
        s1, s2 = set(self.features), set(other.features)
        return s1 - s2, s2 - s1

    def project(self: TimeseriesTypeType, feature_selection: bool | str | Collection[str]) -> TimeseriesTypeType:
        feature_selection = mangle_arg_with_bool_fallback(mangle_arg_to_tuple, feature_selection, if_true=self.features)
        assert all(f in self.features for f in feature_selection)
        return self.__class__(self.label, feature_selection)

    def merge(self: TimeseriesTypeType, other: TimeseriesTypeType) -> TimeseriesTypeType:
        assert self.is_mergeable(other)
        return self.__class__(self.label,
                              mangle_arg_to_tuple(itertools.chain(self.features, other.features), rm_duplicates=True))


@dataclass(frozen=True, init=False)
class EventTimeseriesType(TimeseriesType):
    type = MachineDataTypes.E


@dataclass(frozen=True, init=False)
class MeasurementTimeseriesType(TimeseriesType):
    type = MachineDataTypes.M


class TimeseriesTypeFactory:
    types = {MachineDataTypes.E: EventTimeseriesType, MachineDataTypes.M: MeasurementTimeseriesType}

    @classmethod
    def for_name(cls, arg: str):
        return cls.types[arg]


@dataclass(frozen=True, eq=True, repr=True)
class Header:
    feature_definitions: dict[TimeseriesTypeKey, TimeseriesType]
    extensions: set[MDExtensionConcepts] = field(init=False, default_factory=set)

    @classmethod
    def from_raw(cls, raw_feature_definitions: RawHeaderType):
        return cls({k: TimeseriesTypeFactory.for_name(k[0])(k[1], v) for k, v in raw_feature_definitions.items()})

    def __getitem__(self, item) -> TimeseriesFeatureLabels:
        return self.feature_definitions[item].features


TSType = TypeVar('TSType', bound=TimeseriesType)


@dataclass
class AbstractMachineDataTimeseries(Generic[TSType], ABC):
    timeseries_type: TSType
    df: pd.DataFrame


@dataclass
class MachineDataTimeseries(AbstractMachineDataTimeseries[TSType]):
    objects: Collection[str]


@dataclass
class EventSeries(MachineDataTimeseries[EventTimeseriesType]):
    pass


@dataclass
class MeasurementSeries(MachineDataTimeseries[MeasurementTimeseriesType]):
    pass


TS = TypeVar('TS', bound=MachineDataTimeseries)

TTC = TypeVar('TTC', bound='TypedTimeseriesCollection')


class TypedTimeseriesCollection(Generic[TSType, TS], ABC):
    _ts_type_cls: type[TSType] = None
    _ts_cls: type[TS] = None

    def __init__(self, timeseries_type: TSType, df: pd.DataFrame) -> None:
        super().__init__()
        self.timeseries_type: TSType = timeseries_type
        self.df: pd.DataFrame = df
        self._object_map: dict[str, TS] = {}
        self._repopulate_internal_index()

    @property
    def observation_count(self) -> int:
        return len(self.df)

    @property
    def occurring_objects(self) -> set[str]:
        return self._occurring_objects

    @property
    def time_series_count(self) -> int:
        return len(self._occurring_objects)

    @property
    def object_map(self) -> dict[str, TS]:
        return self._object_map

    @property
    def feature_column_view(self):
        return self.df.loc[:, list(self.timeseries_type.features)]

    def _repopulate_internal_index(self):
        self._internal_index = pd.Series(self.df.index, index=self.df[MDConcepts.Object])
        self._occurring_objects = set(self._internal_index.index)
        self._object_map = {obj: self.view(obj) for obj in self._occurring_objects}

    def _check_ts_features(self):
        return set(self.timeseries_type.features) <= set(self.df.columns)

    def _mk_timeseries_view(self, timeseries_type, objs) -> TS:
        df = self.df.loc[self._internal_index.loc[objs]]
        return self._ts_cls(timeseries_type, df, set(df[MDConcepts.Object]))

    def _update_timeseries_type(self, timeseries_type: TSType = None) -> None:
        self.timeseries_type = self._derive_timeseries_type()
        assert self._check_ts_features()

    def _derive_timeseries_type(self) -> TSType:
        return self._ts_type_cls(self.timeseries_type.label,
                                 only_feature_columns(self.df.columns))

    def update_index(self):
        self._repopulate_internal_index()

    def fit_to_data(self) -> None:
        self._update_timeseries_type()
        self.update_index()

    def view(self, objs: str | list[str] | slice) -> TS:
        objs = slice(None) if objs is None else objs
        return self._mk_timeseries_view(self.timeseries_type, objs)

    def __str__(self):
        return f'TimeseriesCollection(type={self.timeseries_type}, #time series={self.time_series_count}, #obs={self.observation_count}, #objects={len(self.occurring_objects)})'

    def __repr__(self) -> str:
        return str(self)

    def merge(self: TTC, other: TTC,
              axis: Literal['horizontal', 'vertical'] = 'vertical') -> TTC:
        assert axis in {'horizontal', 'vertical'}
        if axis == 'horizontal':
            assert self.timeseries_type.is_mergeable(other.timeseries_type)
            ov = self.timeseries_type.feature_intersection(other.timeseries_type)
            if ov:
                assert np.array_equal(self.df.loc[:, ov].values, other.df.loc[:, ov].values)
            _, new_fs = self.timeseries_type.feature_symmetric_difference(other.timeseries_type)
            if new_fs:
                assert self.df[MDConcepts.Time] == other.df[MDConcepts.Time]
                df = pd.concat([self.df, other.df.loc[:, new_fs]], axis='columns', ignore_index=True, copy=True)
                return self.__class__(self.timeseries_type.merge(other.timeseries_type), df)
            return self
        elif axis == 'vertical':
            assert self.timeseries_type == other.timeseries_type
            df = pd.concat([self.df, other.df], axis='index', ignore_index=True, copy=True)
            df.sort_values(MDConcepts.Time, ignore_index=True, inplace=True)
            return self.__class__(self.timeseries_type, df)

    @classmethod
    def lifted_merge(cls: type[TTC], tscs: dict[str, TTC], o_tscs: dict[str, TTC],
                     axis: Literal['horizontal', 'vertical'] = 'vertical') -> dict[str, TTC]:
        assert axis in {'horizontal', 'vertical'}
        ov = intersection(tscs.keys(), o_tscs.keys())
        s1, s2 = symmetric_difference(tscs.keys(), o_tscs.keys())
        res = {e: tscs[e] for e in s1} | {e: tscs[e].merge(o_tscs[e], axis=axis) for e in ov}
        if axis == 'horizontal':
            return res
        elif axis == 'vertical':
            return res | {e: o_tscs[e] for e in s2}


class EventTimeseriesCollection(TypedTimeseriesCollection[EventTimeseriesType, EventSeries]):
    _ts_type_cls = EventTimeseriesType
    _ts_cls = EventSeries


class MeasurementTimeseriesCollection(TypedTimeseriesCollection[MeasurementTimeseriesType, MeasurementSeries]):
    _ts_type_cls = MeasurementTimeseriesType
    _ts_cls = MeasurementSeries


ETSType = TypeVar('ETSType', bound=TimeseriesType)
MTSType = TypeVar('MTSType', bound=TimeseriesType)

ETS = TypeVar('ETS', bound=MachineDataTimeseries)
MTS = TypeVar('MTS', bound=MachineDataTimeseries)

ETSC = TypeVar('ETSC', bound=TypedTimeseriesCollection)
MTSC = TypeVar('MTSC', bound=TypedTimeseriesCollection)


class TimeseriesCollectionFactory:
    types = {MachineDataTypes.E: EventTimeseriesCollection, MachineDataTypes.M: MeasurementTimeseriesCollection}

    @classmethod
    def for_type(cls, timeseries_type: TimeseriesType):
        if isinstance(timeseries_type, EventTimeseriesType):
            return partial(cls.types[MachineDataTypes.E], timeseries_type)
        elif isinstance(timeseries_type, MeasurementTimeseriesType):
            return partial(cls.types[MachineDataTypes.M], timeseries_type)


AMD = TypeVar('AMD', bound='AbstractMachineData')


class AbstractMachineData(Generic[ETSType, MTSType, ETS, MTS, ETSC, MTSC], ABC):
    _etsc_cls: type[ETSC] = None
    _mtsc_cls: type[MTSC] = None

    def __init__(self, events: Iterable[ETSC],
                 measurements: Iterable[MTSC],
                 index_frame: pd.DataFrame = None) -> None:
        self._index_frame: pd.DataFrame = index_frame
        self.event_series_types: dict[EventTypeLabel, ETSType]
        self.measurement_series_types: dict[MeasurementTypeLabel, MTSType]
        self.event_series: dict[EventTypeLabel, ETSC] = {etc.timeseries_type.label: etc for etc in events}
        self.measurement_series: dict[MeasurementTypeLabel, MTSC] = {mtc.timeseries_type.label: mtc for mtc in
                                                                     measurements}
        self._repopulate_maps()

    @property
    def index_frame(self) -> pd.DataFrame:
        if self._index_frame is None:
            self.recalculate_index()
        return self._index_frame

    @index_frame.setter
    def index_frame(self, value: pd.DataFrame):
        self._index_frame = value

    @property
    def occurring_objects(self) -> set[str]:
        return self._occurring_objects

    @property
    def series_containers(self) -> list[ETSC | MTSC]:
        return list(self.event_series.values()) + list(self.measurement_series.values())

    @classmethod
    def from_series(cls: type[AMD], events: Iterable[ETSC],
                    measurements: Iterable[MTSC], lazy_index_creation=True) -> AMD:
        md = cls(events, measurements)
        if not lazy_index_creation:
            md.recalulate_index()
        return md

    def recalculate_index(self, **kwargs):
        self._index_frame = build_shared_index(self.series_containers,
                                               override_categorical_types=kwargs.pop('override_categorical_types',
                                                                                     True),
                                               sort_by_time=kwargs.pop('sort_by_time', True), **kwargs)

    def _repopulate_maps(self):
        self.event_series_types = {es.timeseries_type.label: es.timeseries_type for es in self.event_series.values()}
        self.measurement_series_types = {ms.timeseries_type.label: ms.timeseries_type for ms in
                                         self.measurement_series.values()}
        self.iter_all_timeseries()
        self._occurring_objects = set(self.index_frame[MDConcepts.Object])

    def fit_to_data(self, recreate_index=False):
        for tsc in self.iter_all_timeseries():
            # retain only the rows that are referenced in the overall table
            if not recreate_index:
                tsc.df = tsc.df.filter(items=self.index_frame.index, axis=0)
            tsc.fit_to_data()

        if recreate_index:
            self.recalculate_index()
        else:
            mask = pd.Series(False, index=self.index_frame.index)
            for tsc in self.iter_all_timeseries():
                mask |= self.index_frame.index.isin(tsc.df.index)
            self.index_frame = self.index_frame.loc[mask]

        self._repopulate_maps()

    def iter_all_timeseries(self) -> Iterable[TypedTimeseriesCollection]:
        return itertools.chain(self.event_series.values(), self.measurement_series.values())

    def create_joined_df(self, event_series_labels: Iterable[EventTypeLabel] | bool = None,
                         measurement_series_labels: Iterable[MeasurementTypeLabel] | bool = None):
        event_keys = self.event_series_types.keys()
        esl = mangle_arg_with_bool_fallback(mangle_arg_to_tuple, event_series_labels,
                                            if_true=event_keys,
                                            rm_duplicates=True, preserve_order=True)
        assert_in(esl, event_keys)
        measurement_keys = self.measurement_series_types.keys()
        msl = mangle_arg_with_bool_fallback(mangle_arg_to_tuple, measurement_series_labels,
                                            if_true=measurement_keys,
                                            rm_duplicates=True, preserve_order=True)
        assert_in(msl, measurement_keys)
        return pd.concat([self.index_frame] + [self.event_series[est].feature_column_view for est in esl] + [
            self.measurement_series[mst].feature_column_view for mst in msl], axis='columns', copy=False)

    def create_index_view(self, typ: MachineDataType = None, types: Collection[MachineDataType] = None, obj: str = None,
                          label: ObservationTypeLabel = None, objs: Iterable[str] = None,
                          labels: Iterable[ObservationTypeLabel] = None) -> pd.DataFrame:
        assert typ is None or types is None
        assert obj is None or objs is None
        assert label is None or labels is None

        mask = pd.Series(True, index=self.index_frame.index)
        if obj is not None:
            mask &= (self.index_frame[MDConcepts.Object] == obj)
        elif objs is not None:
            mask &= (self.index_frame[MDConcepts.Object].isin(mangle_arg_to_set(objs)))
        if label is not None:
            mask &= (self.index_frame[MDConcepts.Label] == label)
        elif labels is not None:
            mask &= (self.index_frame[MDConcepts.Label].isin(mangle_arg_to_set(labels)))
        if typ is not None:
            mask &= (self.index_frame[MDConcepts.Type] == typ)
        elif types is not None:
            mask &= (self.index_frame[MDConcepts.Type].isin(mangle_arg_to_set(typ)))

        return self.index_frame.loc[mask]

    def project(self: AMD,
                measurement_feature_selection: dict[MeasurementTypeLabel, bool | Collection[TimeseriesFeatureLabel]] = None,
                event_feature_selection: dict[EventTypeLabel, bool | Collection[TimeseriesFeatureLabel]] = None,
                project_underlying_dfs=False, copy_underlying_dfs=False) -> AMD:
        if measurement_feature_selection is None:
            measurement_feature_selection = {}
        if event_feature_selection is None:
            event_feature_selection = {}
        ms = []
        for m, fs in measurement_feature_selection.items():
            fs = mangle_arg_with_bool_fallback(mangle_arg_to_list, fs,
                                               if_true=self.measurement_series_types[m].features, preserve_order=True)
            mtc = self.measurement_series[m]
            tt = mtc.timeseries_type.project(fs)
            df = mtc.df.loc[:, MDConcepts.base_columns + list(tt.features)] if project_underlying_dfs else mtc.df
            if copy_underlying_dfs:
                df = df.copy()
            ms.append(self._mtsc_cls(tt, df))
        es = []
        for m, fs in event_feature_selection.items():
            fs = mangle_arg_with_bool_fallback(mangle_arg_to_tuple, event_feature_selection,
                                               if_true=self.event_series_types.keys(), preserve_order=True)
            etc = self.event_series[m]
            tt = etc.timeseries_type.project(fs)
            df = etc.df.loc[:, MDConcepts.base_columns + list(tt.features)] if project_underlying_dfs else etc.df
            if copy_underlying_dfs:
                df = df.copy()
            es.append(self._etsc_cls(tt, df))

        index_view = self.create_index_view(
            labels=itertools.chain(measurement_feature_selection.keys(), event_feature_selection.keys()))
        if copy_underlying_dfs:
            index_view = index_view.copy()
        return self.__class__(es, ms, index_frame=index_view)

    def is_mergeable(self, other: AbstractMachineData):
        if self.__class__ != other.__class__:
            return False
        for e, et in self.event_series_types.items():
            if o_et := other.event_series_types.get(e):
                if not et.is_mergeable(o_et):
                    return False
        for m, mt in self.measurement_series_types.items():
            if o_mt := other.measurement_series_types.get(m):
                if not mt.is_mergeable(o_mt):
                    return False
        return True

    def merge(self: AMD, other: AMD,
              axis: Literal['horizontal', 'vertical'] = 'horizontal') -> AMD:
        return self.merge_series(other.event_series, other.measurement_series, axis=axis)

    def merge_series(self, event_series: dict[EventTypeLabel, ETSC], measurement_series: dict[MeasurementTypeLabel, MTSC],
                     axis: Literal['horizontal', 'vertical'] = 'horizontal'):
        assert axis in {'horizontal', 'vertical'}
        recalc_index = axis == 'vertical'
        if event_series is None:
            event_series = {}
        if measurement_series is None:
            measurement_series = {}
        es: dict[str, ETSC] = self._etsc_cls.lifted_merge(self.event_series, event_series, axis=axis)
        ms: dict[str, MTSC] = self._mtsc_cls.lifted_merge(self.measurement_series, measurement_series, axis=axis)
        if recalc_index:
            return self.from_series(es.values(), ms.values())
        else:
            return self.__class__(es.values(), ms.values(), self.index_frame)

    def get_event_series_collection(self, label: EventTypeLabel) -> ETSC:
        return self.event_series[label]

    def get_measurement_series_collection(self, label: MeasurementTypeLabel) -> MTSC:
        return self.measurement_series[label]

    def view_measurement_series(self, label: MeasurementTypeLabel, objs: str | list[str] | slice = slice(None), **kwargs) -> MTS:
        return self.measurement_series[label].view(objs=objs)

    def view_event_series(self, label: EventTypeLabel, objs: str | list[str] | slice = slice(None), **kwargs) -> ETS:
        return self.event_series[label].view(objs=objs)

    def summary(self):
        first = min(self.index_frame[MDConcepts.Time])
        last = max(self.index_frame[MDConcepts.Time])
        num_obs = len(self.index_frame)
        return f'#Observations: {num_obs} between {first} and {last}.' + '\n' + f'#Objects: {len(self.occurring_objects)}' + '\n' + f'#Event types: {len(self.event_series_types)}' + '\n' + f'#Measurement types: {len(self.measurement_series_types)}'

    def __str__(self):
        ets = '\n'.join([f'\t{l}: {", ".join(tt.features)}' for l, tt in self.event_series_types.items()])
        mts = '\n'.join([f'\t{l}: {", ".join(tt.features)}' for l, tt in self.measurement_series_types.items()])
        objs = ' ' + ', '.join(self.occurring_objects)
        return 'MachineData {' + '\n' + 'Event types:' + '\n' + ets + '\n' + 'Measurement types:' + '\n' + mts + '\n' + 'Objects:' + objs + '\n' + '}'

    def __repr__(self):
        return str(self)


class MachineData(AbstractMachineData[
                      EventTimeseriesType, MeasurementTimeseriesType, EventSeries, MeasurementSeries, EventTimeseriesCollection, MeasurementTimeseriesCollection]):
    _etsc_cls = EventTimeseriesCollection
    _mtsc_cls = MeasurementTimeseriesCollection


def build_shared_index(series: Iterable[TypedTimeseriesCollection], index_cols=None, override_categorical_types=True,
                       sort_by_time=False):
    if index_cols is None:
        index_cols = MDConcepts.base_columns
    series = list(series)
    lengths = [len(tsc.df) for tsc in series]
    orig_idx_ranges = np.empty(len(lengths) + 1, dtype=int)
    np.cumsum(lengths, out=orig_idx_ranges[1:])
    orig_idx_ranges[0] = 0

    frame = pd.concat((tsc.df[index_cols] for tsc in series), ignore_index=True, join='inner',
                      copy=False)

    if sort_by_time:
        sorted_idx = np.argsort(frame[MDConcepts.Time])
        frame = frame.iloc[sorted_idx]
        frame.reset_index(drop=True, inplace=True)
        rev = np.empty_like(sorted_idx)
        rev[sorted_idx] = np.arange(len(sorted_idx))
        for tsc, start, end in zip(series, orig_idx_ranges[:-1], orig_idx_ranges[1:]):
            tsc.df.index = pd.Index(rev[start:end])
            tsc.update_index()
    else:
        for tsc, start, end in zip(series, orig_idx_ranges[:-1], orig_idx_ranges[1:]):
            tsc.df.index = pd.RangeIndex(start, end)
            tsc.update_index()

    cats = derive_categoricals(frame, [MDConcepts.Object, MDConcepts.Type, MDConcepts.Label])
    frame = frame.astype(cats, copy=False)
    if override_categorical_types:
        for tsc in series:
            tsc.df = tsc.df.astype(cats, copy=False)
    return frame

