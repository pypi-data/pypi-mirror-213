import pandas as pd

from mdata.core import machine_data_def as mdd
from mdata.file_formats import io_utils


def write_machine_data_h5(filename, md: mdd.MachineData, complevel: int = 0, **kwargs) -> None:
    if 'format' not in kwargs:
        kwargs['format'] = 't'
    io_utils.ensure_directory_exists(filename)
    filename = io_utils.ensure_ext(filename, '.h5')
    with pd.HDFStore(filename, mode='w', complib='blosc', complevel=complevel) as store:
        store.put('master', md.index_frame, index=True, data_columns=mdd.MDConcepts.base_columns,
                  dropna=False, **kwargs)
        store.create_table_index('master', columns=['index', mdd.MDConcepts.Time, mdd.MDConcepts.Label], kind='full')

        def put_series(key, df):
            store.put(key, df, index=True, data_columns=mdd.MDConcepts.base_columns, dropna=False,
                      **kwargs)
            store.create_table_index(key, columns=['index', mdd.MDConcepts.Time, mdd.MDConcepts.Label], kind='full')

        for label, ess in md.event_series.items():
            put_series(f'events/{label}', ess.df)
        for label, mss in md.measurement_series.items():
            put_series(f'measurements/{label}', mss.df)
