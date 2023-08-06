from mdata.core import mdd


def print_types(md: mdd.MachineData):
    print('Timeseries Types:')
    for e_ts_type in md.event_series_types.values():
        print(e_ts_type)
    for m_ts_type in md.measurement_series_types.values():
        print(m_ts_type)
