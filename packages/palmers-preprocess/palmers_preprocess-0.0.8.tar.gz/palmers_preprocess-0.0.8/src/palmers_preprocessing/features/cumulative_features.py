import numpy as np
from typing import List
import pandas as pd
from ..utils import parse_regular_data_columns
from .. import config


class CumulativeFeatureGenerator:
    @classmethod
    def filter_data_by_date(cls, df: pd.DataFrame, date_col: str, start_date: str) -> pd.DataFrame:
        """
        Filters the data by the start date.
        Args:
            df:     The dataframe to filter.
            date_col:   The name of the date column.
            start_date:     The start date.

        Returns:
            The filtered dataframe.
        """
        df = df[df[date_col] >= start_date]
        return df

    @classmethod
    def groupby_sum_item_store(cls, df: pd.DataFrame, target_col: str, item_store_col: List[str],
                               date_col: str) -> pd.DataFrame:
        """
        Groups the dataframe by item_store and date and sums the target column.
        Args:
            df:     The dataframe to group.
            target_col:     The name of the target column -> sales.
            item_store_col:     The name of the item_store column -> item_store.
            date_col:   The name of the date column.

        Returns:
            The grouped dataframe.
        """
        df[target_col] = df[target_col].astype(np.float64)
        return df.groupby(item_store_col + [date_col])[target_col].sum().reset_index()

    @classmethod
    def add_cumulative_sum_column_respect_time(cls, df: pd.DataFrame, target_col: str, item_store_col: List[str],
                                               list_freq: List[str], date_col: str) -> pd.DataFrame:
        """
        This function adds cumulative sum columns to the dataframe respect to the time.
        describe the following steps:
        1) Group the dataframe by item_store and date and sum the target column.
        2) Add cumulative sum columns to the dataframe respect to the time.
        3) Merge the dataframe with the cumulative sum columns to the original dataframe.
        4) Fill the cumulative sum columns with the previous values.
        Args:
            df:    The dataframe to group.
            target_col:    The name of the target column -> sales.
            item_store_col:   The name of the item_store column -> item_store.
            list_freq:  The list of frequencies to calculate the cumulative sum -> ["D", "W-Mon", "M", "Y"]
            date_col:   The name of the date column.

        Returns:
            The dataframe with the cumulative sum columns.

        """
        df[date_col] = pd.to_datetime(df[date_col])
        item_store_col_name = '_'.join(item_store_col)
        for freq in list_freq:
            df_grouped = df.groupby(item_store_col + [pd.Grouper(key=date_col, freq=freq)])[target_col].sum(
                numeric_only=True).reset_index()

            df_grouped[f"sales_cumulative_{item_store_col_name}_{freq}"] = df_grouped.groupby(item_store_col)[
                target_col].apply(lambda x: np.cumsum(x.shift(1).fillna(0)))

            df = df.merge(df_grouped.drop(columns=[target_col]), on=item_store_col + [date_col], how='left').fillna(0)
            df = df.drop_duplicates(subset=item_store_col + [date_col], keep='last')
        return df

    @classmethod
    def add_expected_value_column_respect_time(cls, df: pd.DataFrame, target_col: str, item_store_col: List[str],
                                               list_freq: List[str], date_col: str) -> pd.DataFrame:
        """
        This function adds expected value columns to the dataframe respect to the time.
        describe the following steps:
        1) Group the dataframe by item_store and date and sum the target column.
        2) Add expected value columns to the dataframe respect to the time.
        3) Merge the dataframe with the expected value columns to the original dataframe.
        4) Fill the expected value columns with the previous values.
        Args:
            df:     The dataframe to group.
            target_col:     The name of the target column -> sales.
            item_store_col:     The name of the item_store column -> item_store.
            list_freq:  The list of frequencies to calculate the expected value -> ["D", "W-Mon", "M", "Y"]
            date_col:   The name of the date column.

        Returns:
            The dataframe with the expected value columns.

        """
        item_store_col_name = '_'.join(item_store_col)
        df_expected = pd.DataFrame()
        df[target_col] = df[target_col].astype(np.float32)
        for freq in list_freq:
            df_temp = df.groupby(item_store_col + [pd.Grouper(key=date_col, freq=freq)])[target_col].sum(
                numeric_only=True).reset_index()
            df_temp[f"sales_expected_{item_store_col_name}_{freq}"] = df_temp.groupby(item_store_col)[
                target_col].transform(
                lambda x: x.mean()).shift(1).fillna(0)
            df_temp[f"sales_expected_{item_store_col_name}_{freq}"] = df_temp[
                f"sales_expected_{item_store_col_name}_{freq}"].replace(
                [np.inf, -np.inf], 0)
            df_expected = pd.concat(
                [df_expected, df_temp[[date_col] + item_store_col + [f"sales_expected_{item_store_col_name}_{freq}"]]])

        df = pd.merge(df, df_expected, on=[date_col] + item_store_col, how='left').fillna(0)
        df = df.drop_duplicates(subset=item_store_col + [date_col], keep='last')
        return df

    # TODO: fix item_store_col value to be unified across all project
    @classmethod
    def run_pipline_cumulative(cls, data_sales: pd.DataFrame, target_col: str = config.SALES_COLUMN_NAME,
                               item_store_col: list[str, str] = config.ITEM_STORE_COLUMN_NAME_LIST,
                               date_col: str = config.DATE_COLUMN_NAME,
                               list_freq: list[str, str, str, str] = config.LIST_FREQ,
                               start_date: str = config.START_DATE_CUMULATIVE_FEATURES):
        """
        This function runs the pipeline to create the cumulative features.
        following steps:
        1) Filter the data by date.
        2) Group the data by item_store and date and sum the target column.
        3) Add cumulative sum columns to the dataframe respect to the time.
        4) Add expected value columns to the dataframe respect to the time.
        5) Drop the target column.
        6) parse the data columns
        Args:
            data_sales:     The dataframe to group.
            target_col:     The name of the target column -> sales.
            item_store_col:     The name of the item_store column -> item_store.
            date_col:   The name of the date column.
            list_freq:  The list of frequencies to calculate the cumulative sum and expected value -> ["D", "W-Mon", "M", "Y"]
            start_date:     The start date to filter the data.

        Returns:
            The dataframe with the cumulative sum and expected value columns.
        """

        data_sales2 = cls.filter_data_by_date(data_sales, date_col, start_date)
        data_sales2 = cls.groupby_sum_item_store(data_sales2, target_col, item_store_col,
                                                 date_col)
        data_sales2 = cls.add_cumulative_sum_column_respect_time(data_sales2,
                                                                 target_col, item_store_col,
                                                                 list_freq,
                                                                 date_col)
        data_sales2 = cls.add_expected_value_column_respect_time(data_sales2, target_col,
                                                                 item_store_col,
                                                                 list_freq, date_col)

        data_sales2.drop(columns=[target_col], inplace=True)
        cumulative_features = parse_regular_data_columns(data_sales2)
        return cumulative_features
