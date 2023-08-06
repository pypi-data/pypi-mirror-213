from itertools import cycle
from typing import TypedDict, Collection

import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from mdata.core import machine_data_def as mdd
from mdata.core.util import mangle_arg_to_set, mangle_arg_with_bool_fallback, mangle_arg_to_list


def create_overview_plot(md: mdd.MachineData, downsample_to=10_000, use_gl=True):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.1)

    def create_hovertemplate(fs):
        return '<b>time: %{x:%X}</b>' \
            + '<br>' \
            + '<br>'.join([f'<i>{f}: %{{customdata[{i}]}}</i>' for i, f in enumerate(fs)]) + '<extra></extra>'

    def derive_colors(series, colorscale=plotly.colors.qualitative.Plotly):
        codes, _ = pd.factorize(series)
        codes = codes % len(colorscale)
        return np.take(colorscale, codes)

    did_downsample = False
    colorscale = plotly.colors.qualitative.Plotly
    objs = md.occurring_objects
    color_dict = {o: c for o, c in zip(objs, cycle(colorscale))}

    for tsc in md.iter_all_timeseries():
        timeseries_type = tsc.timeseries_type
        typ = timeseries_type.type
        row = 1 if typ == mdd.MachineDataTypes.E else 2
        fs = timeseries_type.features
        for g, gidx in tsc.df.groupby(mdd.MDConcepts.Object).groups.items():
            obj = g
            df = tsc.df.loc[gidx]
            c = color_dict[g]

            length = len(df)
            if downsample_to and length > downsample_to:
                assert length > 0
                step = max(1, int(length / downsample_to + .5))
                idx = np.arange(0, length, step)
                df = df.iloc[idx]
                did_downsample = True

            x, y = df[mdd.MDConcepts.Time], df[mdd.MDConcepts.Label]
            f_df = mdd.project_on_feature_columns(df)
            cls = go.Scattergl if use_gl else go.Scatter
            marker = dict(color=c)  # size=2
            n = f'{timeseries_type.type}_{timeseries_type.label}_{obj}'
            g = cls(name=n, customdata=f_df, x=x, y=y, mode='markers',
                    hovertemplate=create_hovertemplate(fs), marker=marker, legendgroup=obj,
                    showlegend=False)
            fig.add_trace(g, row=row, col=1)

    for o in objs:
        # dummy traces for legend
        fig.add_trace(
            go.Scatter(x=[None], y=[None], marker=dict(color=color_dict[o]), mode='markers', name=o,
                       line={'color': 'rgba(0, 0, 0, 0)'}, legendgroup=o, showlegend=True, hoverinfo='none'), row=1,
            col=1)

    fig.update_yaxes(categoryorder='category descending', side='left')
    fig.update_yaxes(title_text='Events', visible=True, type='category', row=1, col=1)
    fig.update_yaxes(title_text='Measurements', visible=True, type='category', row=2, col=1)

    # if not md.has_event_series():
    #    fig.update_yaxes()
    title_text = 'Overview'
    if did_downsample:
        title_text += f'<br><sup>(sampled to {downsample_to} data points per series)</sup>'
    fig.update_layout(title=dict(text=title_text, xanchor='center', x=0.5, font_size=24),
                      legend=dict(title_text='Objects', x=0, y=1.2, orientation='h'))
    # fig.update_layout(title=dict(x=0), row=1, col=1)

    return fig


class Selection(TypedDict):
    object: str
    measurement: str
    features: list[str] | bool
    events: set[str] | bool


def create_timeseries_plot(md: mdd.MachineData, measurement_type: str, object: str,
                           features: Collection[str] | bool = True,
                           events: Collection[str] | bool = True, downsample_to=15_000, split_into_subplots=False):
    events = mangle_arg_with_bool_fallback(mangle_arg_to_set, events, if_true=md.event_series_types.keys())
    tsc = md.measurement_series[measurement_type]
    features = mangle_arg_with_bool_fallback(mangle_arg_to_list, features, if_true=tsc.timeseries_type.features)

    assert set(features) <= set(tsc.timeseries_type.features)
    df = tsc.df

    sampler = None
    full_length = len(df)
    if full_length > downsample_to:
        from tsdownsample import MinMaxLTTBDownsampler
        sampler = MinMaxLTTBDownsampler()

    df = df.loc[df[mdd.MDConcepts.Object] == object, [mdd.MDConcepts.Time] + features]

    if split_into_subplots:
        f_count = max(1, len(features))
        row_heights = [.9 / f_count] * f_count + [.1]
    else:
        row_heights = [.9, .1]
    fig = make_subplots(rows=len(row_heights), cols=1, row_heights=row_heights, shared_xaxes=True,
                        vertical_spacing=0.05)

    for i, f in enumerate(features, start=1):
        # go.scatter.Line()
        x, y = df[mdd.MDConcepts.Time], df[f]
        isna_ = ~y.isna()
        x, y = x[isna_], y[isna_]
        if sampler is not None:
            x = x.values
            y = y.values
            sidx = sampler.downsample(x, y, n_out=downsample_to)
            x = x[sidx]
            y = y[sidx]

        row = i if split_into_subplots else 1
        fig.add_trace(go.Scattergl(name=f, x=x, y=y, mode='lines'), row=row, col=1)

    last_row_idx = len(row_heights)
    for e in events:
        edf = md.event_series[e].df
        edf = edf.loc[edf.object == object]
        x = edf[mdd.MDConcepts.Time]
        fig.add_trace(
            go.Scatter(name=e, x=x, y=np.zeros_like(x), mode='markers',
                       marker=dict(size=10, line_width=4, symbol='line-ns-open')), row=last_row_idx, col=1)

    fig.update_yaxes(row=last_row_idx, col=1, visible=False)

    title_text = 'Timeseries'
    if sampler is not None:
        title_text += f'<br><sup>(sampled to {downsample_to} out of {full_length} data points)</sup>'
    fig.update_layout(title_text=title_text, showlegend=True,
                      legend=dict(x=0, y=-0.2, orientation='h'))

    return fig


def create_measurement_frequency_plot(md: mdd.MachineData, use_hz=True):
    fig = go.Figure()
    colorscale = plotly.colors.qualitative.Plotly
    objs = md.occurring_objects
    color_dict = {o: c for o, c in zip(objs, cycle(colorscale))}
    for m, msc in md.measurement_series.items():
        for o, ts in msc.object_map.items():
            diffs = ts.df['time'].sort_values().diff()[1:].map(pd.Timedelta.total_seconds)
            series: pd.Series
            if use_hz:
                series = 1 / diffs[diffs != 0]
            else:
                series = diffs * 1000
            if len(diffs) > 0:
                zero_fraction = diffs[diffs == 0].count() / len(diffs)
                if zero_fraction > 0:
                    print(f'Overlapping timestamps: {100 * zero_fraction:.2f}%')
            b = go.Box(x=[m] * len(series), y=series, name=o, marker=dict(color=color_dict[o]),
                       boxpoints='suspectedoutliers',
                       boxmean=True, legendgroup=o, showlegend=False, offsetgroup=o)

            fig.add_trace(b)

    for o in objs:
        # dummy traces for legend
        fig.add_trace(
            go.Scatter(x=[None], y=[None], marker=dict(color=color_dict[o]), mode='markers', name=o,
                       line={'color': 'rgba(0, 0, 0, 0)'}, legendgroup=o, showlegend=True, hoverinfo='none'))
    fig.update_layout(title_text='Empirical Frequency of Measurement Types per Object',
                      yaxis_title=('[Hz]' if use_hz else '[ms]'),
                      xaxis_title='Measurement Type', legend_title='Objects', boxmode='group')
    return fig
