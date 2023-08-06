import numpy as np
import pandas as pd

from .. import config as global_config
from . import config as config

store_col_str = global_config.STORE_COLUMN_NAME
item_col_str = global_config.ITEM_COLUMN_NAME
date_col_str = global_config.DATE_COLUMN_NAME
sales_col_str = global_config.SALES_COLUMN_NAME
id_col_str = global_config.ID_COLUMN_NAME
item_store_col_str = global_config.ITEM_STORE_COLUMN_NAME


class LagFeatureGenerator:
    def __init__(self, daily_lags_back=config.DAILY_LAGS_BACK,
                 daily_windows=config.DAILY_WINDOWS,
                 daily_diff_lags=config.DAILY_DIFF_LAGS,
                 daily_ewms=config.DAILY_EWMS):
        self.daily_lags_back = daily_lags_back
        self.daily_windows = daily_windows
        self.daily_diff_lags = daily_diff_lags
        self.daily_ewms = daily_ewms

    def add_lags_and_rolling_averages_and_diffs_and_ewms(self, df: pd.DataFrame, base_column_name: str):
        """
        This function creates lags, rolling averages, diffs and ewms for a given column
        Args:
            df: dataframe
            base_column_name: column name to create lags, rolling averages, diffs and ewms for

        Returns:
            dataframe with lags, rolling averages, diffs and ewms for a given column
        """
        for lag in self.daily_lags_back:
            df[f'{base_column_name}_sales_lag_{lag}'] = df[sales_col_str].shift(lag)
        for window in self.daily_windows:
            df[f'{base_column_name}_sales_rolling_{window}'] = df[sales_col_str].shift(1).rolling(window).mean()
        for diff_lag in self.daily_diff_lags:
            df[f'{base_column_name}_sales_diff_{diff_lag}'] = df[sales_col_str].shift(1) - df[sales_col_str].shift(
                diff_lag)
        for ewm in self.daily_ewms:
            df[f'{base_column_name}_sales_ewm_{ewm}'] = df[sales_col_str].shift(1).ewm(alpha=ewm).mean()
        return df


class StoreLagFeatureGenerator(LagFeatureGenerator):
    def __init__(self):
        super().__init__()

    def create_all_stores_lags(self, store_data_df: pd.DataFrame, predict_date: str):
        """
        This function creates groupby by date and sum of sales for all stores
        and then creates lags, rolling averages, diffs and ewms for the sum of sales
        Args:
            store_data_df: dataframe with store data
            predict_date: date to filter the dataframe

        Returns:
            dataframe with lags, rolling averages, diffs and ewms for the sum of sales
        """
        store_df = store_data_df.groupby(date_col_str).sum(numeric_only=True).reset_index()[
            [date_col_str, sales_col_str]]
        store_df = store_df.set_index(date_col_str)
        store_df = self.add_lags_and_rolling_averages_and_diffs_and_ewms(df=store_df[[sales_col_str]],
                                                                         base_column_name=store_col_str)
        store_df = store_df.drop(columns=[sales_col_str]).reset_index()
        store_df = store_df[store_df[date_col_str] == pd.to_datetime(predict_date)]

        return store_df


class ItemLagFeatureGenerator(LagFeatureGenerator):
    def __init__(self):
        super().__init__()

    def create_all_item_lags(self, regular_data_df: str, predict_date: str):
        """
        This function creates groupby by date and sum of sales for all items and then creates lags, rolling averages,
        diffs and ewms for the sum of sales for each item
        Args:
            regular_data_df: dataframe with regular data
            predict_date: date to filter the dataframe

        Returns:
            dataframe with lags, rolling averages, diffs and ewms for the sum of sales for each item
        """
        all_item_lags = pd.DataFrame()
        for item in regular_data_df[item_col_str].unique():
            item_data = regular_data_df[regular_data_df[item_col_str] == item].groupby(date_col_str).sum(
                numeric_only=True).reset_index()[
                [date_col_str, sales_col_str]]
            item_data = item_data.set_index(date_col_str)
            item_data = self.add_lags_and_rolling_averages_and_diffs_and_ewms(item_data[[sales_col_str]], item_col_str)
            item_data = item_data.drop(columns=[sales_col_str]).reset_index()
            item_data[item_col_str] = np.int64(item)
            all_item_lags = pd.concat([all_item_lags, item_data], ignore_index=True)
        all_item_lags = all_item_lags[all_item_lags[date_col_str] == pd.to_datetime(predict_date)]
        return all_item_lags


class IDLagFeatureGenerator(LagFeatureGenerator):
    def __init__(self):
        super().__init__()

    def create_id_lags(self, id_data_df: pd.DataFrame, item, store, predict_date: str):
        """
        This function creates lags, rolling averages, diffs and ewms for a given item and store
        Args:
            id_data_df:     dataframe with data for a given item and store
            item:        item id
            store:     store id
            predict_date:   date to filter the dataframe

        Returns:
            dataframe with lags, rolling averages, diffs and ewms for a given item and store

        """
        id_data_df = self.add_lags_and_rolling_averages_and_diffs_and_ewms(
            id_data_df.set_index(date_col_str)[[sales_col_str]], id_col_str).reset_index()
        id_data_df[item_col_str] = np.int64(item)
        id_data_df[store_col_str] = np.int32(store)
        id_data_df = id_data_df[id_data_df[date_col_str] == pd.to_datetime(predict_date)]
        return id_data_df
