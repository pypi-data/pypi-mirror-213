
import pandas as pd


class LagsRollingAverageDiffsEWMsFeaturesGenerator:
    def __init__(self, df_sales: pd.DataFrame, store_name: str, item_name: str, sales_name: str, date_name: str, end_date: str,
                 start_date_of_test: str, lags_back: list, windows: list, diff_lags: list, ewms: list):
        self.df_sales = df_sales
        self.store_name = store_name
        self.item_name = item_name
        self.sales_name = sales_name
        self.date_name = date_name
        self.end_date = end_date
        self.start_date_of_test = start_date_of_test
        self.lags_back = lags_back
        self.windows = windows
        self.diff_lags = diff_lags
        self.ewms = ewms


    def sum_agg_per_item_date_store(self, data):
        data = data.groupby([self.date_name, self.store_name, self.item_name]).sum(numeric_only=True)[self.sales_name].reset_index()
        data[self.item_name] = data[self.item_name].astype('category')
        data[self.store_name] = data[self.store_name].astype('category')
        return data

    def add_item_store_id_col(self, df):
        ''' Add a column with the item and store id.

            Args:
                    df: The dataframe to add the column to.
                    DEFAULT_item_NAME: The default name of the item column.
                    DEFAULT_STORE_NAME: The default name of the store column.

            Returns:
                    The dataframe with the new column.

            '''
        df['item, store'] = list(zip(df[self.item_name], df[self.store_name]))
        return df

    def take_more_then_0_sales_and_set_index_to_date(self, data):
        ''' Take only the rows with more then 0 sales and set the index to the date.

            Args:
                    data: The dataframe to take the rows from.
                    DEFAULT_DATE_NAME: The default name of the date column.
                    DEFAULT_SALES_NAME: The default name of the sales column.

            Returns:
                    The dataframe with the new index.

            '''
        data = data[data[self.sales_name] > 0]
        data = data.set_index(self.date_name)
        data.index = pd.to_datetime(data.index)
        return data

    def add_lags_and_rolling_averages_and_diffs_and_ewms(self, df1, item):
        for lag in self.lags_back:
            df1[f'{item}_sales_lag_{lag}'] = df1['sales'].shift(lag)
        for window in self.windows:
            df1[f'{item}_sales_rolling_{window}'] = df1['sales'].shift(1).rolling(window).mean()
        for diff_lag in self.diff_lags:
            df1[f'{item}_sales_diff_{diff_lag}'] = df1['sales'].shift(1) - df1['sales'].shift(diff_lag)
        for ewm in self.ewms:
            df1[f'{item}_sales_ewm_{ewm}'] = df1['sales'].shift(1).ewm(alpha=ewm).mean()
        return df1

    def fill_0_in_gaps_item_store_dates_until_end_date_df(self, df_of_item_store_sales):
        df_of_item_store_sales = df_of_item_store_sales.reindex(pd.date_range(min(df_of_item_store_sales.index), self.end_date))

        return df_of_item_store_sales

    def return_df_of_item_store_sales_with_lags_rolling_diff_ewm(self, data):
        df_of_item_store_sales = pd.DataFrame()
        i = 0
        for item_store in data["item, store"].unique():
            i += 1
            item_store_data = data[data["item, store"] == item_store]
            item_store_data['item, store'] = [item_store] * len(item_store_data)
            item_store_data = LagsRollingAverageDiffsEWMsFeaturesGenerator.add_lags_and_rolling_averages_and_diffs_and_ewms(self, item_store_data[['sales']], 'id')
            item_store_data['item, store'] = [item_store] * len(item_store_data)
            df_of_item_store_sales = pd.concat([item_store_data.reset_index().rename(columns={"index": "date"})])
        return df_of_item_store_sales


    def return_df_of_store_sales_with_lags_rolling_diff_ewm(self, data):
        df_of_store_sales = pd.DataFrame()
        i = 0
        for store in data["store"].unique():
            i += 1
            store_data = data[data["store"] == store].groupby("date").sum(numeric_only=True)
            store_data['store'] = store
            store_data = LagsRollingAverageDiffsEWMsFeaturesGenerator.add_lags_and_rolling_averages_and_diffs_and_ewms(self, store_data[['sales']], self.store_name)
            store_data['store'] = store
            df_of_store_sales = pd.concat([store_data.reset_index().rename(columns={"index": "date"})])
        return df_of_store_sales

    def return_df_of_item_sales_with_lags_rolling_diff_ewm(self, data):
        df_of_item_sales = pd.DataFrame()
        i = 0
        for item in data["item"].unique():
            i += 1
            item_data = data[data["item"] == item].groupby("date").sum(numeric_only=True)
            item_data['item'] = item
            item_data = LagsRollingAverageDiffsEWMsFeaturesGenerator.add_lags_and_rolling_averages_and_diffs_and_ewms(self, item_data[['sales']], self.item_name)
            item_data['item'] = item
            df_of_item_sales = pd.concat([item_data.reset_index().rename(columns={"index": "date"})])

        return df_of_item_sales