from datetime import datetime

import pandas as pd


def derive_categoricals(df, cols):
    return {c: pd.CategoricalDtype(df[c].unique(), ordered=False) for c in cols}


def set_artificial_dt_index(df: pd.DataFrame):
    dr = create_artificial_daterange(df)
    df.index = dr
    return df


def create_artificial_daterange(df):
    return pd.date_range(start=datetime(1970, 1, 1), freq='S', periods=len(df))
