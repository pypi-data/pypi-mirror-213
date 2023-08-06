from ..machine_data_def import *


@dataclass
class IndexedMachineDataTimeseries(MachineDataTimeseries[TSType]):
    indices: Collection[int]


@dataclass
class IndexedEventSeries(IndexedMachineDataTimeseries[EventTimeseriesType]):
    pass


@dataclass
class IndexedMeasurementSeries(IndexedMachineDataTimeseries[MeasurementTimeseriesType]):
    pass


TSI = TypeVar('TSI', bound=IndexedMachineDataTimeseries)


class TypedIndexedTimeseriesCollection(Generic[TSType, TS, TSI], TypedTimeseriesCollection[TSType, TS]):
    _tsi_cls: type[TSI] = None

    def __init__(self, timeseries_type: TSType, df: pd.DataFrame) -> None:
        super().__init__(timeseries_type, df)

    @property
    def occurring_series_indices(self) -> pd.Index:
        return self._series_indices

    @property
    def time_series_count(self) -> int:
        return self._internal_index.index.size

    def _repopulate_internal_index(self):
        self._internal_index = pd.Series(self.df.index,
                                         index=[self.df[MDConcepts.Object], self.df[MDExtensionConcepts.Index]])
        self._occurring_objects = set(self._internal_index.index.get_level_values(0))
        self._series_indices = self._internal_index.index.get_level_values(1).unique()

    def _mk_indexed_timeseries_view(self, timeseries_type, objs, indices) -> TSI:
        df = self.df.loc[self._internal_index.loc[objs, indices]]
        return self._tsi_cls(timeseries_type, df, set(df[MDConcepts.Object]), df[MDExtensionConcepts.Index].unique())

    def get_for_obj_and_index(self, obj, index) -> TSI:
        return self._mk_indexed_timeseries_view(self.timeseries_type, obj, index)

    def view_indexed(self, objs: str | list[str] | slice, indices: str | list[str] | slice) -> TSI:
        if objs is None:
            objs = slice(None)
        if indices is None:
            indices = slice(None)
        return self._mk_indexed_timeseries_view(self.timeseries_type, objs, indices)

    def _mk_timeseries_view(self, timeseries_type, objs) -> TS:
        df = self.df.loc[self._internal_index.loc[objs, :]]
        return self._ts_cls(timeseries_type, df, set(df[MDConcepts.Object]))

    def __str__(self):
        return f'IndexedTimeseriesCollection(type={self.timeseries_type}, #time series={self.time_series_count}, #obs={self.observation_count}, #objects={len(self.occurring_objects)}, #series_indices={len(self.occurring_series_indices)})'


class IndexedEventTimeseriesCollection(
    EventTimeseriesCollection, TypedIndexedTimeseriesCollection[EventTimeseriesType, EventSeries, IndexedEventSeries]):
    #_ts_type_cls = EventTimeseriesType
    #_ts_cls = EventSeries
    _tsi_cls = IndexedEventSeries


class IndexedMeasurementTimeseriesCollection(
    MeasurementTimeseriesCollection, TypedIndexedTimeseriesCollection[MeasurementTimeseriesType, MeasurementSeries, IndexedMeasurementSeries]):
    #_ts_type_cls = MeasurementTimeseriesType
    #_ts_cls = MeasurementSeries
    _tsi_cls = IndexedMeasurementSeries


ETSI = TypeVar('ETSI', bound=IndexedMachineDataTimeseries)
MTSI = TypeVar('MTSI', bound=IndexedMachineDataTimeseries)


class AbstractMultiplicityMachineData(Generic[ETSI, MTSI], AbstractMachineData[
    EventTimeseriesType, MeasurementTimeseriesType, EventSeries, MeasurementSeries, IndexedEventTimeseriesCollection, IndexedMeasurementTimeseriesCollection]):
    _etsc_cls = IndexedEventTimeseriesCollection
    _mtsc_cls = IndexedMeasurementTimeseriesCollection
    _etsi_cls: type[ETSI] = None
    _mtsi_cls: type[MTSI] = None

    def recalculate_index(self, **kwargs):
        super().recalculate_index(index_cols=MDExtensionConcepts.combined_columns, **kwargs)

    @property
    def occurring_series_indices(self) -> pd.Index:
        return self._occurring_series_indices

    def _repopulate_maps(self):
        super()._repopulate_maps()
        self._occurring_series_indices = pd.Index(self.index_frame[MDExtensionConcepts.Index].unique())

    def view_event_series(self, label: EventTypeLabel, objs: str | list[str] | slice = None,
                          indices: str | list | slice = None,
                          **kwargs) -> MTSI:
        assert label is not None
        return self.event_series[label].view_indexed(objs, indices)

    def view_measurement_series(self, label: MeasurementTypeLabel, objs: str | list[str] | slice = None,
                                indices: str | list | slice = None,
                                **kwargs) -> MTSI:
        assert label is not None
        return self.measurement_series[label].view_indexed(objs, indices)

    def summary(self):
        first = min(self.index_frame[MDConcepts.Time])
        last = max(self.index_frame[MDConcepts.Time])
        num_obs = len(self.index_frame)
        return f'#Observations: {num_obs} between {first} and {last}.' + '\n' + f'#Objects: {len(self.occurring_objects)}' + '\n' + f'#Series Indices: {len(self.occurring_series_indices)}' + '\n' + f'#Event types: {len(self.event_series_types)}' + '\n' + f'#Measurement types: {len(self.measurement_series_types)}'

    def __str__(self) -> str:
        ets = '\n'.join([f'\t{l}: {", ".join(tt.features)}' for l, tt in self.event_series_types.items()])
        mts = '\n'.join([f'\t{l}: {", ".join(tt.features)}' for l, tt in self.measurement_series_types.items()])
        objs = ' ' + ', '.join(self.occurring_objects)
        sidx = ' ' + str(self.occurring_series_indices)
        return 'MachineData {' + '\n' + 'Event types:' + '\n' + ets + '\n' + 'Measurement types:' + '\n' + mts + '\n' + 'Objects:' + objs + '\n' + 'Series Indices:' + sidx + '\n' + '}'


class MultiplicityMachineData(AbstractMultiplicityMachineData[IndexedEventSeries, IndexedMeasurementSeries]):
    _etsi_cls = IndexedEventSeries
    _mtsi_cls = IndexedMeasurementSeries
