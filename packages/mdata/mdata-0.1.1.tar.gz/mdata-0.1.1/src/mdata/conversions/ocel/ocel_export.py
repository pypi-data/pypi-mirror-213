import pandas as pd

import mdata.core.machine_data_def as mdd
from pm4py.objects.ocel.obj import OCEL, constants


def create_ocel(md: mdd.MachineData):
    raise NotImplemented
    pd.DataFrame()
    os = md.index_frame[mdd.MDConcepts.Object].unique()
    for mt, tsc in md.measurement_series.items():
        i = 0
        m_obj = pd.DataFrame(tsc.df, columns=list(tsc.timeseries_type.features))
        m_obj = m_obj.assign(**{constants.DEFAULT_OBJECT_TYPE: tsc.timeseries_type.label, constants.DEFAULT_OBJECT_ID: i})
    for et, tsc in md.event_series.items():
        tsc.timeseries_type.features

    ...