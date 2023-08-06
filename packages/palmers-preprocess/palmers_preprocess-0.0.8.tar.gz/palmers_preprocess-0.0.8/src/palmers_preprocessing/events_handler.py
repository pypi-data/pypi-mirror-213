from typing import List
import pandas as pd
import numpy as np
from scipy.fftpack import fft
from scipy.signal import argrelextrema
from sklearn.decomposition import PCA
from category_encoders import GLMMEncoder, MEstimateEncoder, CatBoostEncoder
from . import config


# TODO: speak to yotam
def run_pipline_event(data_event, data_sales, data_hol, date_col=config.DEFAULT_EVENT_HANDLER_VARIABLES['date_col'],
                      start_date=config.DEFAULT_EVENT_HANDLER_VARIABLES['start_date'],
                      target_col=config.DEFAULT_EVENT_HANDLER_VARIABLES['target_col'],
                      max_date=config.DEFAULT_EVENT_HANDLER_VARIABLES['max_date'],
                      min_date=config.DEFAULT_EVENT_HANDLER_VARIABLES['min_date'],
                      duration_list_col=config.DEFAULT_EVENT_HANDLER_VARIABLES['duration_list_col'],
                      column_list_map_id=config.DEFAULT_EVENT_HANDLER_VARIABLES['column_list_map_id'],
                      event_num=config.DEFAULT_EVENT_HANDLER_VARIABLES['event_num'],
                      event_col_list=config.DEFAULT_EVENT_HANDLER_VARIABLES['event_col_list'],
                      event_col_even=config.DEFAULT_EVENT_HANDLER_VARIABLES['event_col_even'],
                      date_min_col_list=config.DEFAULT_EVENT_HANDLER_VARIABLES['date_min_col_list'],
                      holiday_col=config.DEFAULT_EVENT_HANDLER_VARIABLES['holiday_col'],
                      holiday_col_type=config.DEFAULT_EVENT_HANDLER_VARIABLES['holiday_col_type'],
                      weekend_col=config.DEFAULT_EVENT_HANDLER_VARIABLES['weekend_col'],
                      year_forecast=config.DEFAULT_EVENT_HANDLER_VARIABLES['year_forecast'],
                      pca_num=config.DEFAULT_EVENT_HANDLER_VARIABLES['pca_num'],
                      type_encoder_list=config.DEFAULT_EVENT_HANDLER_VARIABLES['type_encoder_list'],
                      cols_to_encode=config.DEFAULT_EVENT_HANDLER_VARIABLES['cols_to_encode'],
                      cols_to_encode_at_once=config.DEFAULT_EVENT_HANDLER_VARIABLES['cols_to_encode_at_once'],
                      cols_days_for_interaction=config.DEFAULT_EVENT_HANDLER_VARIABLES['cols_days_for_ineraction'],
                      list_col_add=config.DEFAULT_EVENT_HANDLER_VARIABLES['list_col_add']):
    event_preprocess = EventFeatureGenerator()
    # event_preprocess.change_columns_names_in_dataframe_by_dict(data_sales, column_dict)
    data_sales0 = event_preprocess.filter_data_by_date(data_sales, date_col, start_date)
    data_sales_process = event_preprocess.aggregate_data(data_sales0, target_col)
    data_sales_process1 = event_preprocess.process_date_column(data_sales_process, date_col)
    data_event_process = event_preprocess.calculate_duration(data_event, max_date, min_date)
    data_sales_process2 = event_preprocess.identify_event(data_event_process, data_sales_process1, date_col, min_date,
                                                          max_date)
    data_sales_process3 = event_preprocess.map_event_to_list(data_sales_process2, data_event_process, max_date,
                                                             min_date, column_list_map_id, date_col)
    data_sales_process4 = event_preprocess.add_stat_duartions(data_sales_process3, duration_list_col)
    data_sales_process5 = event_preprocess.length_list_event(data_sales_process4, event_col_list)
    data_sales_process6 = event_preprocess.diff_col(data_sales_process5, target_col, date_col)
    data_sales_process7 = event_preprocess.event_frequency(data_sales_process6, date_col, event_num)
    data_sales_process8 = event_preprocess.indicate_event_combination_change(data_sales_process7, event_col_even)
    # data_sales_process9 = event_preprocess.std_on_list(data_sales_process8, event_col_discount_type)
    data_sales_process10 = event_preprocess.log_col(data_sales_process8, target_col)
    data_sales_process11 = event_preprocess.caculate_amount_days_pass_from_start_of_event(data_sales_process10,
                                                                                          date_col, date_min_col_list)
    data_sales_process12 = event_preprocess.caculate_amount_days_pass_from_start_of_event_most_new(data_sales_process11,
                                                                                                   date_min_col_list,
                                                                                                   date_col)
    data_sales_process13 = event_preprocess.merge_df(data_sales_process12, data_hol, date_col)
    data_sales_process14 = event_preprocess.identify_date_occasion(data_sales_process13, holiday_col, date_col)
    data_sales_process15 = event_preprocess.feature_combine_str(data_sales_process14, holiday_col_type, holiday_col)
    data_sales_process16 = event_preprocess.add_cumulative_sum_column_for_targe(data_sales_process15, target_col)
    data_sales_process17 = event_preprocess.fft_features(data_sales_process16, target_col)
    data_sales_process18 = event_preprocess.time_series_shape_features(data_sales_process17, target_col)
    data_sales_process21 = event_preprocess.convert_str_indicator(data_sales_process18, weekend_col)

    # data_sales_process22 = event_preprocess.extract_features_pca(data_sales_process21, date_col, year_forecast, pca_num,
    #                                                              target_col, task=task)
    #
    data_sales_process23 = event_preprocess.process_next_days_events(data_sales_process21, target_col)

    return data_sales_process23


def finalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Finalize data for model removing unnecessary columns
    Args:
        df: data event features

    Returns:
        df
    """
    event_preprocess = EventFeatureGenerator()
    data_sales_process27 = event_preprocess.remove_expand_dates(df)
    data_final_event = data_sales_process27.copy()
    return data_final_event


class EventFeatureGenerator:
    @classmethod
    def aggregate_data(cls, df_sales: pd.DataFrame, target_col: str) -> pd.DataFrame:
        """
        Aggregate data by date
        Args:
            target_col:     name of target column
            df_sales:      pandas DataFrame

        Returns:   aggregate by target_col pandas DataFrame

        """
        df_sales[target_col] = df_sales[target_col].astype(np.float64)
        return df_sales.groupby(['date'])[target_col].sum(numeric_only=True).reset_index()

    @classmethod
    def filter_data_by_date(cls, df_sales: pd.DataFrame, date_col: str, start_date: str) -> pd.DataFrame:
        """
        Filter data by date
        Args:
            df_sales:      pandas DataFrame
            start_date:    start date
            end_date:      end date

        Returns:   filtered pandas DataFrame

        """
        df_sales = df_sales[df_sales[date_col] >= start_date]
        return df_sales

    @classmethod
    def process_date_column(cls, df_sales: pd.DataFrame, date_col: str) -> pd.DataFrame:
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
        return df_sales

    @classmethod
    def calculate_duration(cls, df_event: pd.DataFrame, max_date: str, min_date: str) -> pd.DataFrame:
        """
        Calculate the duration between two dates in a DataFrame of events.
        Args:
            df_event: A pandas DataFrame containing the event dates.
            max_date (str): The name of the column containing the latest date.
            min_date (str): The name of the column containing the earliest date.

        Returns:
            A pandas DataFrame with a new 'duration' column containing the duration between the two dates.
        """
        df_event = df_event[(df_event['event_id'] != -1)]
        df_event[max_date], df_event[min_date] = pd.to_datetime(df_event[max_date]), pd.to_datetime(df_event[min_date])
        df_event['duration'] = df_event[max_date] - df_event[min_date]
        return df_event

    @classmethod
    def identify_event(cls, df_event: pd.DataFrame, df_sales: pd.DataFrame, date_col: str, min_date: str,
                       max_date: str) -> pd.DataFrame:
        """
        Identify event dates in sales data and create an is_event column in sales DataFrame.

        Args:
        df_event (pd.DataFrame): DataFrame containing the event dates.
        df_sales (pd.DataFrame): DataFrame containing the sales data.
        date_col (str): Column name for date in df_sales.
        min_date (str): Column name for start event date in df_event.
        end_event_date (str): Column name for end event date in df_event.

        Returns:
        A pandas DataFrame containing the sales data with an is_event column added.
        """
        df_sales['is_event'] = 0
        for index, event in df_event.iterrows():
            mask = df_sales[date_col].isin(pd.date_range(start=event[min_date], end=event[max_date]))
            df_sales.loc[mask, 'is_event'] = 1
        return df_sales

    @staticmethod
    def get_event_id_list(df_temp: pd.DataFrame, row: pd.Series, col: str, date_col: str) -> List[str]:
        """
        Get list of event ids for a given date and event type.
        Args:
            df_temp:
            row:
            col:

        Returns:

        """
        df_event_row = df_temp[df_temp[date_col] == row[date_col]][f"{col}_list"].tolist()
        return df_event_row

    @classmethod
    def map_event_to_list(cls, df_sales: pd.DataFrame, df_event: pd.DataFrame, max_date: str, min_date: str,
                          column_list_map_id: List[str], date_col: str) -> pd.DataFrame:
        """
        Map event to list of event ids for a given date and event type.
        Args:
            df_sales:   DataFrame containing the sales data.
            df_event:   DataFrame containing the event dates.
            max_date:   Column name for end event date in df_event.
            min_date:   Column name for start event date in df_event.
            column_list_map_id: List of columns to map to list.

        Returns:

        """
        for col in column_list_map_id:
            temp_list = []
            for index, event in df_event.iterrows():
                dates = pd.date_range(start=event[min_date], end=event[max_date])
                for date in dates:
                    temp_list.append({date_col: date, f"{col}_list": event[col]})
            df_temp = pd.DataFrame(temp_list)
            df_sales[f"{col}_list"] = df_sales.apply(
                lambda row: EventFeatureGenerator.get_event_id_list(df_temp, row, col, date_col), axis=1)
            del temp_list
        return df_sales

    @classmethod
    def add_stat_duartions(cls, df_sales: pd.DataFrame, duration_list_col: str) -> pd.DataFrame:
        """
        Adds statistical measures of the durations of events in a column of a pandas DataFrame.

        Args:
            df (pd.DataFrame): The pandas DataFrame containing the event column.
            duration_list_col (str): The name of the column representing the events -> "duration_list"

        Returns:
            pd.DataFrame: DataFrame with three new columns:
                - '{event_col}_mean_event': the mean duration of events in the event column, for each row in the DataFrame.
                - '{event_col}_median_event': the median duration of events in the event column, for each row in the DataFrame.
                - '{event_col}_std_event': the standard deviation of the duration of events in the event column, for each row in the DataFrame.
        """
        df_sales[f"{duration_list_col}_mean_event"] = df_sales.apply(lambda x: np.mean(x[duration_list_col]), axis=1)
        df_sales[f"{duration_list_col}_mean_event"] = df_sales[f"{duration_list_col}_mean_event"].dt.days
        df_sales[f"{duration_list_col}_median_event"] = df_sales.apply(lambda x: np.median(x[duration_list_col]),
                                                                       axis=1)
        df_sales[f"{duration_list_col}_median_event"] = df_sales[f"{duration_list_col}_median_event"].dt.days
        df_sales[f"{duration_list_col}_std_event"] = df_sales.apply(
            lambda x: np.std([d.total_seconds() for d in x[duration_list_col]]), axis=1)
        return df_sales

    @classmethod
    def length_list_event(cls, df_sales: pd.DataFrame, event_col_list: List[str]) -> pd.DataFrame:
        """
        Calculates the length of each list in a column of a pandas DataFrame, for a specified list of columns.

        Args:
            df (pd.DataFrame): The pandas DataFrame containing the event columns.
            event_col_list (List[str]): The list of names of columns representing the events -> ["event_id_list","sub_event_id_list"]

        Returns:
            pd.DataFrame: DataFrame with a new column called 'num_{col}' for each column in event_col_list.
            These columns represent the length of each list in the corresponding event column, for each row in the DataFrame.
        """
        for col in event_col_list:
            df_sales[f"num_{col}"] = df_sales.apply(lambda x: len(x[col]), axis=1)
        return df_sales

    @classmethod
    def diff_col(cls, df_sales: pd.DataFrame, target_col: str, date_col: str) -> pd.DataFrame:
        """
        Calculates the rate of change in a column of a pandas DataFrame over time, based on a date column.

        Args:
            df (pd.DataFrame): The pandas DataFrame containing the target and date columns.
            target_col (str): The name of the column representing the target variable.
            date_col (str): The name of the column representing the dates.

        Returns:
            pd.DataFrame: DataFrame with a new column called '{target_col}_diff'.
            This column represents the rate of change in the target column over time, based on the day-to-day difference
            in the target variable and the number of days between each row in the date column.
            :param df_sales:
        """
        diff = df_sales[target_col].astype(np.int64).diff().dropna()
        days_diff = pd.to_datetime(df_sales[date_col]).dt.day.diff().dropna()
        rate_of_change = diff / days_diff
        df_sales[f"{target_col}_diff"] = rate_of_change.shift()
        df_sales[f"{target_col}_diff"] = df_sales[f"{target_col}_diff"].replace([np.inf, -np.inf], 0)
        return df_sales

    @classmethod
    def event_frequency(cls, df_sales: pd.DataFrame, date_col: str, event_num: str) -> pd.DataFrame:
        """
        Calculates the frequency of events in a pandas DataFrame, based on a specified date column and event count column.

        Args:
            df (pd.DataFrame): The pandas DataFrame containing the date and event count columns.
            date_col (str): The name of the column representing the dates.
            event_num (str): The name of the column representing the event counts ->'num_event_id_list'

        Returns:
            pd.DataFrame: DataFrame with a new column called 'event_frequency'.
            This column represents the average number of events per week, based on the event count and number of weeks in the date column.
        """

        df_sales['event_frequency'] = (
                df_sales[event_num] / df_sales[date_col].dt.isocalendar().week.nunique()).shift(1).fillna(0)
        return df_sales

    @classmethod
    def indicate_event_combination_change(cls, df_sales: pd.DataFrame, event_col_even: str) -> pd.DataFrame:
        """
        Indicates whether the combination of events has changed from the previous row in a pandas DataFrame.

        Args:
            df (pd.DataFrame): The pandas DataFrame containing the event column.
            event_col_even (str): The name of the column representing the events.

        Returns:
            pd.DataFrame: DataFrame with a new column called 'ind_change_combo_event'.
            This column represents whether the combination of events in the current row is different from the previous row (1),
            or not (0).
        """
        df_sales["ind_change_combo_event"] = np.where(df_sales[event_col_even].shift() != df_sales[event_col_even], 1,
                                                      0)
        df_sales.loc[0, "ind_change_combo_event"] = 0
        return df_sales

    # def std_on_list(self, df_sales: pd.DataFrame, event_col_discount_type: str) -> pd.DataFrame:
    #     """
    #     Calculates the standard deviation of a list of values in a column of a pandas DataFrame.
    #
    #     Args:
    #         df (pd.DataFrame): The pandas DataFrame containing the column of lists.
    #         event_col_discount_type (str): The name of the column containing the lists -> "discount_type_list"
    #
    #     Returns:
    #         pd.DataFrame: DataFrame with a new column called '{event_col}_std'.
    #         This column represents the standard deviation of the values in the list in the specified event column,
    #         for each row in the DataFrame.
    #         [0.0,1.0,1.0]
    #     """
    #
    #     df_sales[event_col_discount_type] = df_sales[event_col_discount_type].apply(lambda x: [int(i) for i in x] if isinstance(x, (list, tuple)) else x)
    #     df_sales[f"{event_col_discount_type}_std"] = df_sales.apply(
    #         lambda x: np.std([d for d in x[event_col_discount_type]]) if isinstance(x[event_col_discount_type],
    #                                                                                 (list, tuple)) else np.nan,
    #         axis=1)
    #     return df_sales

    @classmethod
    def log_col(cls, df_sales: pd.DataFrame, target_col: str) -> pd.DataFrame:
        """
        Applies the natural logarithm to a specified column in a pandas DataFrame.
        but skips the operation for any zero values.

        Args:
            df (pd.DataFrame): The pandas DataFrame containing the target column.
            target_col (str): The name of the column to apply the logarithm to.

        Returns:
            pd.DataFrame:DataFrame with a new column called '{target_col}_log'.
            This column represents the natural logarithm of the specified target column,
            except for any zero values which are left unchanged.
        """
        df_sales[f"{target_col}_log"] = np.where(df_sales[target_col] == 0, 0, np.log(df_sales[target_col]))
        df_sales[f"{target_col}_log"] = df_sales[f"{target_col}_log"].shift(1).fillna(0)
        return df_sales

    @classmethod
    def caculate_amount_days_pass_from_start_of_event(cls, df_sales: pd.DataFrame, date_col: str,
                                                      date_min_col_list: str) -> pd.DataFrame:
        """
        Calculates the number of days that have passed since the start of an event in a pandas DataFrame.

        Args:
            df (pd.DataFrame): The pandas DataFrame containing the event and date columns.
            date_min_col_list (str): The name of the column representing the start of the event     -> "date_min_list"
            date_col (str): The name of the column representing the dates.

        Returns:
            pd.DataFrame: DataFrame with a new column called 'amount_of_days_pass_from_start_of_event'.
            This column represents the number of days that have passed since the start of the event, for each row in the DataFrame.
        """
        df_sales["amount_of_days_pass_from_start_of_event"] = df_sales.apply(
            lambda x: np.abs(pd.to_datetime(x[date_col]) - pd.to_datetime(x[date_min_col_list])), axis=1)
        return df_sales

    @classmethod
    def caculate_amount_days_pass_from_start_of_event_most_new(cls, df_sales: pd.DataFrame, event_col: str,
                                                               date_col: str) -> pd.DataFrame:
        """
        Calculates the number of days that have passed since the start of an event, for the most recent event in a pandas DataFrame.

        Args:
            df (pd.DataFrame): The pandas DataFrame containing the event and date columns.
            event_col (str): The name of the column representing the events -> "min_date_list"
            date_col (str): The name of the column representing the dates.

        Returns:
            pd.DataFrame: DataFrame with a new column called 'amount_of_days_pass_from_start_of_event_most_new'.
            This column represents the number of days that have passed since the start of the most recent event, for each row in the DataFrame.
        """
        df_sales["amount_of_days_pass_from_start_of_event_most_new"] = df_sales.apply(
            lambda x: np.min(pd.to_datetime(x[date_col]) - pd.to_datetime(x[event_col])), axis=1)
        df_sales["amount_of_days_pass_from_start_of_event_most_new"] = pd.to_timedelta(
            df_sales["amount_of_days_pass_from_start_of_event_most_new"]).dt.days
        return df_sales

    @classmethod
    def merge_df(cls, df_sales: pd.DataFrame, df_holiday: pd.DataFrame, key: str) -> pd.DataFrame:
        """
        Merges two pandas DataFrames based on a common key.
        1: df1 = df_sales
        2: df2 = df_holidays
        key: 'date'

        Args:
            df1 (pd.DataFrame): The first pandas DataFrame to merge.
            df2 (pd.DataFrame): The second pandas DataFrame to merge.
            key (str): The name of the key column to merge on.

        Returns:
            df_merge    pd.DataFrame: A new DataFrame that contains all columns from both input DataFrames, merged
            on the specified key. The merge type is left join (i.e., all rows from df1 are retained, and
            matching rows from df2 are included where available).
        """
        df_sales[key] = pd.to_datetime(df_sales[key])
        df_holiday[key] = pd.to_datetime(df_holiday[key], format="%d/%m/%Y")
        df_sales = df_sales.merge(df_holiday, on=key, how="left")
        return df_sales

    @classmethod
    def identify_date_occasion(cls, df_sales: pd.DataFrame, holiday_col: str, date_col: str) -> pd.DataFrame:
        """
        Identifies holidays in a pandas DataFrame based on a specified column.

        Args:
            df (pd.DataFrame): The pandas DataFrame containing the holiday column.
            holiday_col (str): The name of the column representing the holidays -> "holiday_name"
            date_col (str): The name of the column representing the dates -> "date"

        Returns:
            pd.DataFrame: DataFrame with a new column called 'is_holiday'. This column
            represents whether each row is a holiday (1) or not (0), based on whether the holiday column
            is null or not.
        """
        df_sales["is_holday"] = np.where(df_sales[holiday_col].isnull(), 0, 1)
        df_sales["is_sunday"] = np.where(df_sales[date_col].dt.day_name() == "Sunday", 1, 0)
        return df_sales

    @classmethod
    def feature_combine_str(cls, df_sales: pd.DataFrame, holiday_col_type: str, holiday_col: str) -> pd.DataFrame:
        """
        Combines the values of two columns in a pandas DataFrame into a new column as a string.
        col1='type',col2='holiday_name' -> 'type_holiday_name'
        Args:
            df (pd.DataFrame): The pandas DataFrame containing the two columns to combine.
            holiday_col_type (str): The name of the first column to combine -> "holiday_type"
            holiday_col (str): The name of the second column to combine -> "holiday_name"

        Returns:
            pd.DataFrame: DataFrame with a new column called '{col1}_{col2}'. This column
            represents the concatenation of the values of col1 and col2 as strings, separated by an underscore.
        """
        df_sales[f"{holiday_col_type}_{holiday_col}"] = df_sales[holiday_col_type].map(str) + "_" + df_sales[
            holiday_col].map(str)
        return df_sales

    @classmethod
    def calculate_rolling_functions(cls, df_sales: pd.DataFrame, target_col: str, window_size_list: List[int],
                                    type_functions: List[str]) -> pd.DataFrame:
        """
        Calculates the moving average trend for a specified column in a pandas DataFrame.

        Args:
            df (pd.DataFrame): The pandas DataFrame containing the target column.
            target_col (str): The name of the column for which to calculate the trend.
            window_size_list (int): list size of the rolling window to use when calculating the trend.
            type_functions (List[str]): The type of trend to calculate. This can be any function
                from the numpy library that can be applied to a rolling window.

        Returns:
            pd.DataFrame: DataFrame with a new column called 'trend'. This column represents
            the moving average trend of the specified target column over the rolling window.
        """
        for type_function in type_functions:
            for window_size in window_size_list:
                df_sales[f'rolling_{window_size}_{type_functions}'] = df_sales[target_col].rolling(
                    window=window_size).apply(
                    getattr(np, type_function)).shift(1).fillna(0)
        return df_sales

    @classmethod
    def add_cumulative_sum_column_for_targe(cls, df_sales: pd.DataFrame, col: str) -> pd.DataFrame:
        """
        Adds a cumulative sum column to a pandas DataFrame.
        Args:
            df (pd.DataFrame): The pandas DataFrame to add the cumulative sum column to.
            col (str): The name of the column to calculate the cumulative sum for.

        Returns:
            pd.DataFrame: DataFrame with a new column called 'cumulative_sum'. This column
            represents the cumulative sum of the specified column.
        """
        df_sales[f'cumulative_sum_{col}'] = df_sales[col].cumsum()
        df_sales[f'cumulative_sum_{col}'] = df_sales[f'cumulative_sum_{col}'].shift(1).fillna(0)
        return df_sales

    @classmethod
    def fft_features(cls, df_sales: pd.DataFrame, target_col: str) -> pd.DataFrame:
        """
        Extracts spectral analysis features using Fast Fourier Transform (FFT).

        Args:
            df (pd.DataFrame): The pandas DataFrame containing the target column.
            target_col (str): The name of the column representing the target variable.

        Returns:
            pd.DataFrame: DataFrame with two new columns: 'fft_real' and 'fft_imag'.
            These columns represent the real and imaginary parts of the FFT output, respectively.
        """
        df_temp = fft(df_sales[target_col].shift(1).fillna(0).values)
        df_sales['fft_real'] = np.real(df_temp)
        df_sales['fft_imag'] = np.imag(df_temp)
        return df_sales

    @classmethod
    def extract_trend_change(cls, df_sales: pd.DataFrame, trend_col: str) -> pd.DataFrame:
        """
        Extracts trend changes in a pandas DataFrame based on peaks in a specified trend column.

        Args:
            df (pd.DataFrame): The pandas DataFrame containing the trend column.
            trend_col (str): The name of the column representing the trend -> 'rolling_7_mean'

        Returns:
            pd.DataFrame: DataFrame with a new column called 'trend_change' indicating
            trend changes. If the value in the trend column is a local maximum (peak), the value in the
            'trend_change' column will be set to 1. Otherwise, it will be set to 0.
        """
        peaks_extract = argrelextrema(np.array(df_sales[trend_col].shift(1).fillna(0).values), np.greater)
        df_sales['trend_change'] = 0
        df_sales.loc[peaks_extract[0], 'trend_change'] = 1
        return df_sales

    @classmethod
    def time_series_shape_features(cls, df_sales: pd.DataFrame, target_col: str) -> pd.DataFrame:
        """
        Calculates shape-based features of a time series and adds them as columns to the input dataframe.

        Args:
            df (pd.DataFrame): The input time series data as a pandas dataframe.
            target_col (str): The name of the column in the input dataframe that contains the target variable.

        Returns:
            pd.DataFrame: A pandas dataframe with the same columns as the input dataframe, but with additional columns for the calculated shape-based features.
        """
        df_sales['skewness'] = df_sales[target_col].shift(1).fillna(0).skew()
        df_sales['kurtosis'] = df_sales[target_col].shift(1).fillna(0).kurt()
        df_sales['slope'] = np.polyfit(df_sales.index, df_sales[target_col].shift(1).fillna(0).values, 1)[0]
        return df_sales

    @classmethod
    def add_lagged_feature_to_time_series_of_column(cls, df_sales: pd.DataFrame, cols: list[str],
                                                    lags_list: List[int]) -> pd.DataFrame:
        """
        Add a lagged feature to a time series dataframe.

        Args:
            df: The dataframe to add the lagged feature to.
                assumed to be in time series format
            col: The column to add the lagged feature to.
            lag: The lag to add to the dataframe.

        Returns:
            The dataframe with the lagged feature added.


        """

        for col in cols:
            for lag in lags_list:
                df_sales[f'{col}_lag_{lag}'] = df_sales[col].shift(lag)
        return df_sales

    @classmethod
    def convert_str_indicator(cls, df_sales: pd.DataFrame, weekend_col: list[str]) -> pd.DataFrame:
        """
        Converts boolean columns in a pandas DataFrame to binary integer columns (0 or 1).
        Args:
            df: The input DataFrame.
            weekend_cols: A list of column names to be converted.

        Returns:
            The input DataFrame with the specified columns converted to binary integer format.
        """

        df_sales[weekend_col] = np.where(df_sales[weekend_col] is True, 1, 0)
        return df_sales

    @classmethod
    def extract_features_pca(cls, df_sales: pd.DataFrame, date_col: str,
                             pca_num: int, year_forecast: int = None) -> pd.DataFrame:
        """
        Perform Principal Component Analysis (PCA) on a subset of numerical columns in a DataFrame, and append the resulting
        principal components to the original DataFrame.

        Args:
            df (pd.DataFrame): The input DataFrame.
            year_forecast (int): The year after which to exclude data from PCA analysis.
            pca_num (int): The number of principal components to retain.

        Returns:
            pd.DataFrame: The input DataFrame with additional columns corresponding to the retained principal components.
        """

        ##### NOT FOR INFERENCE
        if year_forecast is None:
            df_pca = df_sales
        else:
            df_pca = df_sales[df_sales[date_col].dt.year < year_forecast].copy()

        df_numeric = df_pca.select_dtypes(include=[np.number])
        df_numeric = df_numeric.drop(columns=df_numeric.select_dtypes(include='timedelta64').columns.tolist())
        df_numeric_imputed = df_numeric.fillna(0)
        pca = PCA(n_components=pca_num)
        pca.fit(df_numeric_imputed)
        df_setup_process = df_sales.copy()
        pca_components = pca.transform(df_setup_process[df_numeric_imputed.columns].fillna(0))
        columns_pca = [f"PC{i}" for i in range(1, pca_num + 1)]
        pca_df = pd.DataFrame(pca_components, columns=columns_pca)
        df_sales[columns_pca] = pca_df
        return df_sales

    @classmethod
    def apply_encodings(cls, df_sales: pd.DataFrame, type_encoder_list: List[str], cols_to_encode: List[str],
                        target_col: str,
                        year_forecast: int, sigma=1, random_state=12) -> pd.DataFrame:
        """
        Applies a set of target encoders to specified columns in a pandas DataFrame.

        Args:
            target_col:
            df (pd.DataFrame): The input DataFrame.
            type_encoder_list (List[str]): A list of target encoders to apply to the specified columns. The encoder names should be strings and correspond to the name of the encoder class from the category_encoders package.
            ->["GLMMEncoder","MEstimateEncoder","CatBoostEncoder"]
            cols_to_encode (List[str]): A list of column names to encode.
            target (str): The name of the target column.
            year_forecast (int): The year until which to include data.
            sigma (float): The noise level added to the encoding.
            random_state (int): The random seed used for the encoding.

        Returns:
            pd.DataFrame: The encoded DataFrame.
        """
        ##### NOT FOR INFERENCE
        encoder_class_dict = {
            # "GLMMEncoder": GLMMEncoder,
            "MEstimateEncoder": MEstimateEncoder,
            "CatBoostEncoder": CatBoostEncoder
        }
        if year_forecast is None:
            df_filtered = df_sales
        else:
            df_filtered = df_sales[df_sales.date.dt.year < year_forecast].copy()

        for encoder_type in type_encoder_list:
            encoder_class = encoder_class_dict[encoder_type]
            for col in cols_to_encode:
                encoder = encoder_class(cols=[col], sigma=sigma, random_state=random_state)
                if encoder_type == "CatBoostEncoder":
                    encoder.fit(df_filtered[col].astype(str), df_filtered[target_col])
                    df_sales[f'{encoder_type}_of_{col}'] = encoder.transform(df_sales[col], df_sales[target_col])
                else:
                    encoder.fit(df_filtered[col], df_filtered[target_col])
                    df_sales[f'{encoder_type}_of_{col}'] = encoder.transform(df_sales[col], df_sales[target_col])
        return df_sales

    @classmethod
    def apply_encodings_at_once(cls, df_sales: pd.DataFrame, type_encoder_list: List[str], cols_to_encode: List[str],
                                target_col: str,
                                year_forecast: int, sigma=1, random_state: int = 12) -> pd.DataFrame:
        """
        Apply multiple category encoders to the same set of columns at once.

        Args:
            df (pd.DataFrame): The input dataframe to be encoded.
            type_encoder_list (List[str]): A list of category encoder types to be applied ->["GLMMEncoder","MEstimateEncoder","CatBoostEncoder"]
            cols (List[str]): A list of column names to be encoded.
            target (str): The name of the target column to encode against.
            year_forecast (int): The year forecast limit to use for training data.
            sigma (float): The regularization parameter for encoders that support it. Default is 1.
            random_state (int): The random seed to use. Default is 12.

        Returns:
            pd.DataFrame: A new dataframe with the encoded columns added.
        """
        ##### NOT FOR INFERENCE
        encoder_class_dict = {
            # "GLMMEncoder": GLMMEncoder,
            "MEstimateEncoder": MEstimateEncoder,
            "CatBoostEncoder": CatBoostEncoder
        }
        if year_forecast is None:
            df_filtered = df_sales
        else:
            df_filtered = df_sales[df_sales.date.dt.year < year_forecast].copy()

        for encoder_type in type_encoder_list:
            encoder_class = encoder_class_dict[encoder_type]
            encoder = encoder_class(cols=cols_to_encode, sigma=sigma, random_state=random_state)
            if encoder_type == "CatBoostEncoder":
                encoder.fit(df_filtered[cols_to_encode].astype(str), df_filtered[target_col])
                encoded_df = encoder.transform(df_sales[cols_to_encode], df_sales[target_col])
                for col in encoded_df.columns:
                    df_sales[f'{encoder_type}_of_all_{col}'] = encoded_df[col]
            else:
                encoder.fit(df_filtered[cols_to_encode], df_filtered[target_col])
                encoded_df = encoder.transform(df_sales[cols_to_encode], df_sales[target_col])
                for col in encoded_df.columns:
                    df_sales[f'{encoder_type}_of_all_{col}'] = encoded_df[col]
        return df_sales

    @classmethod
    def columns_interactions_encoder(cls, df_sales: pd.DataFrame, cols_to_encode_at_once: List[str],
                                     cols_days_for_interaction: List[str], target_col: str,
                                     type_encoder_list: List[str], year_forecast: int) -> pd.DataFrame:
        """
        Apply feature interaction encoding on specified columns and then encode the new columns using a list of categorical encoders.

        Args:
            df_sales (pd.DataFrame): The input dataframe to be encoded.
            cols_to_encode_at_once (List[str]): A list of columns to be encoded at once.
            cols_days_for_interaction (List[str]): A list of columns to be used for feature interaction.
            target_col (str): The name of the target column to encode against.
            type_encoder_list (List[str]): A list of category encoder types to be applied ->["GLMMEncoder","MEstimateEncoder","CatBoostEncoder"]
            year_forecast (int): The year forecast limit to use for training data.


        Returns:
            pd.DataFrame: A new DataFrame with feature interaction columns and encoded columns using specified categorical encoders.

        """
        interactions_columns = []
        for col1 in cols_to_encode_at_once:
            for col2 in cols_days_for_interaction:
                df_sales[f"{col1}_interactions_{col2}"] = df_sales[f"{col1}"] * df_sales[f"{col2}"]
                interactions_columns.append(f"{col1}_interactions_{col2}")

        df_sales = cls.apply_encodings_at_once(df_sales=df_sales, type_encoder_list=type_encoder_list,
                                               cols_to_encode=interactions_columns,
                                               target_col=target_col, year_forecast=year_forecast)
        return df_sales

    @classmethod
    def remove_expand_dates(cls, df_sales: pd.DataFrame):
        columns_to_check = ['year', 'month', 'day', 'day_of_week', 'week_of_year', 'quarter', 'is_weekend']
        if all(column in df_sales.columns for column in columns_to_check):
            df_sales = df_sales.drop(columns=columns_to_check)
            print("All specified columns have been dropped.")
        else:
            print("Not all specified columns are present in the DataFrame.")
        return df_sales

    @classmethod
    def filter_columns_by_correlation(cls, df_sales: pd.DataFrame, year_forecast: int, target_col: str,
                                      date_col: str) -> List[
        str]:
        """
        Filters the columns in the input dataframe based on their correlation with the target column.
        Args:
            df (pd.DataFrame): The input dataframe to be filtered.
            year_forecast (int): The year forecast limit to use for training data.
            target_col (str): The name of the target column to be used for correlation analysis.
            date_col (str): The name of the date column to be used for filtering based on the year forecast.

        Returns:
            List[str]: A list of column names that are highly correlated with the target column.
        """

        if year_forecast is None:
            corr = df_sales.corr()
        else:
            corr = df_sales[df_sales[date_col].dt.year < year_forecast].corr()

        corr_target = abs(corr[target_col])
        relevant_features = corr_target[(corr_target > 0.4) & (corr_target < 1)]
        selected_col_by_corr = relevant_features.index.tolist()
        return selected_col_by_corr

    @classmethod
    def add_back_feature(cls, df_sales: pd.DataFrame, list_col_add: List[str],
                         selected_col_by_corr: List[str]) -> pd.DataFrame:
        """
        Add a list of columns back to the dataframe.

        Args:
            df_sales:
            df (pd.DataFrame): The input dataframe.
            list_col_add (List[str]): A list of column names to add to the dataframe -> ["date",'target']
            selected_col_by_corr (List[str]): A list of column names to add to the dataframe selected by correlation.

        Returns:
            pd.DataFrame: A new dataframe with the added columns.
        """
        union_list = list_col_add + selected_col_by_corr
        df_union = df_sales[union_list]
        return df_union

    @classmethod
    def process_next_days_events(cls, df_sales: pd.DataFrame, target_col: str) -> pd.DataFrame:
        df_sales['is_tomorrow_event'] = df_sales['is_event'].shift(-1)
        df_sales['is_2_days_event'] = df_sales['is_event'].shift(-2)

        # this is only in inferring
        df_sales[target_col] = df_sales[target_col].shift(-1) + df_sales[target_col].shift(-2)
        y_prcoess = df_sales["is_2_days_event"].dropna()
        df_sales_next = df_sales.loc[y_prcoess.index]
        return df_sales_next


def create_interactions_columns(processed_event_features_df):
    cols_to_encode_at_once = config.DEFAULT_EVENT_HANDLER_VARIABLES['cols_to_encode_at_once']
    cols_days_for_interaction = config.DEFAULT_EVENT_HANDLER_VARIABLES['cols_days_for_ineraction']
    for col1 in cols_to_encode_at_once:
        for col2 in cols_days_for_interaction:
            processed_event_features_df[f"{col1}_interactions_{col2}"] = processed_event_features_df[f"{col1}"] * \
                                                                         processed_event_features_df[f"{col2}"]

    return processed_event_features_df
