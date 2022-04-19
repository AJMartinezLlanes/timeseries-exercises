import pandas as pd
from datetime import timedelta, datetime
import numpy as np
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

from acquire import get_all_store_data, get_opsd_data



def prep_store_data(df):
    df.sale_date = df.sale_date.apply(lambda date: date[:-13])
    df.sale_date = pd.to_datetime(df.sale_date, format='%a, %d %b %Y')
    df = df.set_index('sale_date').sort_index()
    df['month'] = df.index.month_name()
    df['day_of_week'] = df.index.day_name()
    df['sales_total'] = df.sale_amount * df.item_price
    return df


def prep_opsd_data(df):
    df.columns = [column.lower() for column in df]
    df = df.rename(columns={'wind+solar': 'wind_plus_solar'})
    df.date = pd.to_datetime(df.date)
    df = df.set_index('date').sort_index()
    df['month'] = df.index.month_name()
    df['year'] = df.index.year
    df = df.fillna(0)
    df['wind_plus_solar'] = df['wind'] + df['solar']
    return df