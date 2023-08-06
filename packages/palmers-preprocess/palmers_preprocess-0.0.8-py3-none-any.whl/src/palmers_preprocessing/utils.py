from datetime import timedelta, datetime

import numpy as np
import pandas as pd
from . import config


def process_date_column(df_sales: pd.DataFrame, date_col: str, expanded: bool = False) -> pd.DataFrame:
    """
    Process date column
    Args:
        df_sales: pandas DataFrame
        date_col: name of date column
    Returns: pandas DataFrame
    """
    df_sales[date_col] = pd.to_datetime(df_sales[date_col])
    df_sales['year'] = df_sales[date_col].dt.year
    df_sales['month'] = df_sales[date_col].dt.month
    df_sales['day'] = df_sales[date_col].dt.day
    df_sales['day_of_week'] = df_sales[date_col].dt.dayofweek
    df_sales['week_of_year'] = df_sales[date_col].apply(lambda x: x.isocalendar()[1])
    df_sales['quarter'] = df_sales[date_col].dt.quarter
    df_sales['is_weekend'] = df_sales[date_col].dt.dayofweek.isin([5, 6]).astype(int)
    df_sales['name_of_day'] = df_sales[date_col].dt.strftime("%A")

    if expanded:
        df_sales['day_of_year'] = df_sales[date_col].dt.dayofyear
        df_sales['day_of_the_month'] = df_sales[date_col].dt.days_in_month
        df_sales['is_weekend_c'] = df_sales['day_of_week'].apply(lambda x: 1 if x in [5, 6] else 0)
        df_sales['is_weekend_j'] = df_sales['day_of_week'].apply(lambda x: 1 if x in [4, 5] else 0)

    return df_sales


def add_values_to_dict_mapper(dict_mapper: dict, df_encoders: pd.DataFrame, column_name: str, encoders_name: list,
                              dict_of_time_interval: dict) -> dict:
    """
    Adds the values of the encoders in the df_encoders dataframe to the dict_maper dictionary.

    Args:
        dict_mapper:     The dictionary that holds the encoded values.
        df_encoders:        The dataframe that holds the encoded values.
        column_name:    The name of the column in the df_encoders dataframe.
        encoders_name:  The names of the encoders in the df_encoders dataframe.
        dict_of_time_interval:  The dictionary that holds the time intervals.

    Returns:    The updated dict_maper dictionary.

    """
    item_encoders_with_item_index = df_encoders.rename_axis(column_name)
    for item in df_encoders.index:
        for time in dict_of_time_interval:
            for date in dict_of_time_interval[time]:
                for encoder in encoders_name:
                    if time == "months_5_6_7":
                        dict_mapper[column_name][encoder]["months_5_6_7"][(item, date)] = \
                            item_encoders_with_item_index.loc[item][encoder + "_months:5_6_7"]
                    elif time == "all":
                        dict_mapper[column_name][encoder]["all"][(item, date)] = \
                            item_encoders_with_item_index.loc[item][encoder + "_all_time:all_time"]
                    else:
                        dict_mapper[column_name][encoder][time][(item, date)] = \
                            item_encoders_with_item_index.loc[item][encoder + "_" + str(time) + ":" + str(date)]
    return dict_mapper


def map_encoders_columns_to_base_df(data: pd.DataFrame, dict_map: dict, encoders_name: list) -> pd.DataFrame:
    """
    Adds the encoded values to the data dataframe.
    Args:
        data:   The dataframe to add the encoded values to.
        dict_map:   The dictionary that holds the encoded values.
        encoders_name:  The names of the encoders in the df_encoders dataframe.

    Returns:    The updated data dataframe.

    """
    for encoder_name in encoders_name:
        data[encoder_name + "_day_store"] = data.apply(
            lambda x: dict_map[config.STORE_COLUMN_NAME][encoder_name]["name_of_day"][
                x[config.STORE_COLUMN_NAME], x["name_of_day"]], axis=1)
        data[encoder_name + "_day_item"] = data.apply(
            lambda x: dict_map[config.ITEM_COLUMN_NAME][encoder_name]["name_of_day"][
                x[config.ITEM_COLUMN_NAME], x["name_of_day"]], axis=1)
        data[encoder_name + "_month_store"] = data.apply(
            lambda x: dict_map[config.STORE_COLUMN_NAME][encoder_name]["month"][
                x[config.STORE_COLUMN_NAME], x["month"]], axis=1)
        data[encoder_name + "_month_item"] = data.apply(
            lambda x: dict_map[config.ITEM_COLUMN_NAME][encoder_name]["month"][x[config.ITEM_COLUMN_NAME], x["month"]],
            axis=1)
        data[encoder_name + "_quarter_store"] = data.apply(
            lambda x: dict_map[config.STORE_COLUMN_NAME][encoder_name]["quarter"][
                x[config.STORE_COLUMN_NAME], x["quarter"]], axis=1)
        data[encoder_name + "_quarter_item"] = data.apply(
            lambda x: dict_map[config.ITEM_COLUMN_NAME][encoder_name]["quarter"][
                x[config.ITEM_COLUMN_NAME], x["quarter"]], axis=1)

        data[encoder_name + "_day_store"] = data[encoder_name + "_day_store"].astype("float")
        data[encoder_name + "_day_item"] = data[encoder_name + "_day_item"].astype("float")
        data[encoder_name + "_month_store"] = data[encoder_name + "_month_store"].astype("float")
        data[encoder_name + "_month_item"] = data[encoder_name + "_month_item"].astype("float")
        data[encoder_name + "_quarter_store"] = data[encoder_name + "_quarter_store"].astype("float")
        data[encoder_name + "_quarter_item"] = data[encoder_name + "_quarter_item"].astype("float")

        return data


def parse_regular_data_columns(data: pd.DataFrame, item_col_str: str = config.ITEM_COLUMN_NAME,
                               store_col_str: str = config.STORE_COLUMN_NAME,
                               sales_col_str: str = config.SALES_COLUMN_NAME,
                               date_col_str: str = config.DATE_COLUMN_NAME,
                               item_store_col_str: str = config.ITEM_STORE_COLUMN_NAME) -> pd.DataFrame:
    """
    Parses the columns of the data dataframe to the correct data type.

    Args:
        data: The dataframe to parse.
        item_col_str: The name of the item column.
        store_col_str: The name of the store column.
        sales_col_str: The name of the sales column.
        date_col_str: The name of the date column.
        item_store_col_str: The name of the item_store column.

    Returns:
        The updated data dataframe.

    Notes:
    1) item_col_str -> np.int64
    2) store_col_str -> np.int32
    3) sales_col_str -> np.float32
    4) date_col_str -> pd.to_datetime
    5) item_store_col_str -> str
    """
    if item_col_str in data.columns:
        data[item_col_str] = data[item_col_str].astype(np.int64)
    if store_col_str in data.columns:
        data[store_col_str] = data[store_col_str].astype(np.int32)
    if sales_col_str in data.columns:
        data[sales_col_str] = data[sales_col_str].astype(np.float32)
    if date_col_str in data.columns:
        data[date_col_str] = pd.to_datetime(data[date_col_str])
    if item_store_col_str in data.columns:
        data[item_store_col_str] = data[item_store_col_str].astype(str)
    return data


def next_two_days_skip_sunday(start_date:str):
    """
    This function returns the next two days after the start date, skipping Sunday.

    Args:
        start_date: The start date

    Returns:
        A list of the next two days after the start date, skipping Sunday.

    """
    dates = []
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    for i in range(2):
        start_date += timedelta(days=1)
        if start_date.weekday() == 6:
            start_date += timedelta(days=1)
        dates.append(start_date)

    return dates


def convert_df_with_sku_to_df_with_item(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts a dataframe with sku to a dataframe with item and group by date, item, store and sales.
    Args:
        df:     The dataframe to convert.

    Returns:
        The converted dataframe.

    """
    df[config.ITEM_COLUMN_NAME] = df[config.SKU_COLUMN_NAME].str[:-3]
    df[config.SALES_COLUMN_NAME] = df[config.SALES_COLUMN_NAME].astype(float)
    df[config.ITEM_STORE_COLUMN_NAME] = df[config.ITEM_COLUMN_NAME] + ", " + df[config.STORE_COLUMN_NAME]
    df = df[[config.DATE_COLUMN_NAME, config.ITEM_STORE_COLUMN_NAME, config.ITEM_COLUMN_NAME, config.STORE_COLUMN_NAME,
             config.SALES_COLUMN_NAME]]
    df = df.groupby(
        [config.DATE_COLUMN_NAME, config.ITEM_STORE_COLUMN_NAME, config.ITEM_COLUMN_NAME, config.STORE_COLUMN_NAME])[
        config.SALES_COLUMN_NAME].sum().reset_index()
    return df


def daily_sales_to_weekly_mean_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function converts the daily sales to weekly mean sales.
    with groupby on item_store and rolling mean of 6 days - excluding the sunday.
    Args:
        df:     The dataframe to convert.

    Returns:
        The converted dataframe.
    """
    df_with_window_6_rolling = pd.DataFrame()
    grouped = df.groupby([config.ITEM_STORE_COLUMN_NAME])
    for name, group in grouped:
        group_rolling = group.groupby(config.DATE_COLUMN_NAME)[config.SALES_COLUMN_NAME].sum().rolling(6,
                                                                                                       min_periods=6).mean().reset_index()
        group_rolling[config.ITEM_STORE_COLUMN_NAME] = name
        group_rolling[config.ITEM_COLUMN_NAME] = name.split(", ")[0]
        group_rolling[config.STORE_COLUMN_NAME] = name.split(", ")[1]
        df_with_window_6_rolling = pd.concat([df_with_window_6_rolling, group_rolling])
    df_with_window_6_rolling.reset_index(drop=True, inplace=True)
    df_with_window_6_rolling = df_with_window_6_rolling.dropna(subset=[config.SALES_COLUMN_NAME])
    return df_with_window_6_rolling
