import pandas as pd

from mdata.core import machine_data_def as mdd


def read_machine_data_h5(filename) -> mdd.MachineData:
    # ext = io_utils.ensure_ext(filename, '.h5', override_ext=False)
    with pd.HDFStore(filename, mode='r') as store:
        measurements, events = [], []
        rel_groups = next(store.walk('/'))[1]
        if 'events' in rel_groups:
            (path, groups, leaves) = next(store.walk('/events'))
            for label in leaves:
                key = '/'.join([path, label])
                df: pd.DataFrame = store.get(key)
                ets = mdd.EventTimeseriesCollection(
                    mdd.EventTimeseriesType(label, mdd.only_feature_columns(df.columns)),
                    df)
                events.append(ets)
        if 'measurements' in rel_groups:
            (path, groups, leaves) = next(store.walk('/measurements'))
            for label in leaves:
                key = '/'.join([path, label])
                df: pd.DataFrame = store.get(key)
                mts = mdd.MeasurementTimeseriesCollection(
                    mdd.MeasurementTimeseriesType(label, mdd.only_feature_columns(df.columns)), df)
                measurements.append(mts)
        return mdd.MachineData(events, measurements, store.get('master'))
