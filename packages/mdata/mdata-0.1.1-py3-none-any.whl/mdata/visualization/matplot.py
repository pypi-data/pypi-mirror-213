from typing import TypedDict, Collection, Optional

import matplotlib.pyplot as plt
import seaborn as sns

from mdata.core import mdd

def create_basic_stacked_subplots(md: mdd.MachineData, measurement_type: str, objects: set[str] = None, features: list[str] = None, figsize=None):
    tsc = md.measurement_series[measurement_type]
    os = objects
    fs = features
    if os is None:
        os = list(tsc.object_map.keys())
    else:
        assert os <= set(tsc.object_map.keys())
        os = [o for o in tsc.object_map if o in os]
    if fs is None:
        fs = list(tsc.timeseries_type.features)
    else:
        assert set(fs) <= set(tsc.timeseries_type.features)
        fs = [f for f in fs if f in tsc.timeseries_type.features]

    fig, axs = plt.subplots(len(fs), 1, sharex=True, figsize=figsize)

    for i, f in enumerate(fs):
        for o in os:
            ts = tsc.view(o)
            sns.lineplot(data=ts.df, x='time', y=f, ax=axs[i])
        # axs[i].plot(tsc.df.time, tsc.df[f])
        # axs[i].set_title(f)
    fig.tight_layout()
    return fig
