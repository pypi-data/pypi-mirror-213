import pandas as pd
from . import config as global_config
from .features.event_features import EventFeaturesGenerator
from .features.future_features import FarFutureFeaturesGenerator
from .features.lags_features import ItemLagFeatureGenerator, StoreLagFeatureGenerator, IDLagFeatureGenerator
from .features.weather_features import WeatherFeatureGenerator
# from .regular_data_handler import RegularDataLoader
from .utils import parse_regular_data_columns,daily_sales_to_weekly_mean_sales
from .features.cumulative_features import CumulativeFeatureGenerator


class Preprocessor:
    def __init__(self):
        pass

    @classmethod
    def get_future_rows(cls, regular_data_df: pd.DataFrame, begin_date: str, end_date: str):
        """
        Creates the future rows for prediction as a dataframe
        Args:
            regular_data_df: regular data dataframe
            begin_date: begin date of prediction
            end_date: end date of prediction

        Returns:
            dataframe with future rows
        notes:
        1) The names of the input columns must be the same as the global_config
        2) for now the begin_date and end_date must be the same as the prediction date but for future it can be an iterative process
        """
        unique_ids = regular_data_df[global_config.ITEM_STORE_COLUMN_NAME].unique()

        dfs = []
        for date in pd.date_range(begin_date, end_date):
            df = pd.DataFrame(
                {global_config.ITEM_STORE_COLUMN_NAME: unique_ids, global_config.DATE_COLUMN_NAME: date})
            df[[global_config.ITEM_COLUMN_NAME, global_config.STORE_COLUMN_NAME]] = df[
                global_config.ITEM_STORE_COLUMN_NAME].str.split(", ", expand=True)
            dfs.append(df)

        # future_df = pd.DataFrame(
        #     {global_config.ITEM_STORE_COLUMN_NAME: unique_ids, global_config.DATE_COLUMN_NAME: begin_date})
        # future_df[[global_config.ITEM_COLUMN_NAME, global_config.STORE_COLUMN_NAME]] = future_df[
        #     global_config.ITEM_STORE_COLUMN_NAME].str.split(", ", expand=True)

        return pd.concat(dfs)

    @classmethod
    def create_store_id_dict(cls, regular_data_df: pd.DataFrame):
        """
        Create a dictionary with store as key and list of items as value
        Args:
            regular_data_df:    regular data dataframe

        Returns:
            dictionary with store as key and list of items as value

        """
        item_store_dict = regular_data_df.groupby(global_config.STORE_COLUMN_NAME)[
            global_config.ITEM_STORE_COLUMN_NAME].unique().apply(list).to_dict()
        return item_store_dict

    @classmethod
    def preprocess(cls, stores_list: list[int] = global_config.OUTLETS_SDATTA, marketing_plan: pd.DataFrame = None,
                   item_encoders = None, store_encoders = None, store_location_df: pd.DataFrame = None,
                   begin_predict_dates: str = global_config.tomorrow_date, event_encoders: dict = None,
                   regular_data_df: pd.DataFrame = None, event_df: pd.DataFrame = None,
                   holiday_df: pd.DataFrame = None):
        """
        Preprocess data for prediction and return a dataframe with all features:
        1) event features
        2) weather features
        3) lag features
        4) cumulative features

        Args:
            stores_list: list of stores to predict
            begin_predict_dates: date to predict
            regular_data_df: regular data dataframe
            event_df: event dataframe
            holiday_df: holiday dataframe

        :return:
            dataframe with all features

        Notes:
        dataframe must have the following columns:
        1) date
        2) item
        3) store
        4) item_store
        """
        if pd.to_datetime(begin_predict_dates).strftime("%A") == "Sunday":
            print("predict_date is Sunday, no need to predict")
            return

        # if need to load regular data
        # if regular_data_df is None:
        #     regular_data_df = RegularDataLoader().load()

        # TODO: seperate the two days being added for events
        future_df = cls.get_future_rows(regular_data_df, begin_predict_dates, begin_predict_dates)
        regular_data_df = parse_regular_data_columns(pd.concat([regular_data_df, future_df], ignore_index=True))
        regular_data_df = daily_sales_to_weekly_mean_sales(regular_data_df)
        final_event_features_df = EventFeaturesGenerator().generate(regular_data_df, event_df, holiday_df,
                                                                    event_encoders,
                                                                    begin_predict_dates=begin_predict_dates)
        # TODO: first load store_location_here, then call weather prediction someplace else.
        # store_location_df = StoreLocationLoader().load() # on all stores
        cumulative_features_df = CumulativeFeatureGenerator().run_pipline_cumulative(regular_data_df)
        item_lags_features_df = ItemLagFeatureGenerator().create_all_item_lags(regular_data_df, begin_predict_dates)
        # TODO: after the sku_lags, we can filter the regular data (Check this!!!!!)
        regular_data_df = regular_data_df[regular_data_df[global_config.STORE_COLUMN_NAME].isin(stores_list)]
        store_id_dict = cls.create_store_id_dict(regular_data_df)
        far_future_features_df = FarFutureFeaturesGenerator().far_future_features_preprocess_of_several_stores(
            marketing_plan=marketing_plan, item_encoders=item_encoders, store_encoders=store_encoders,
            store_batch_dict=store_id_dict, begin_predict_dates=begin_predict_dates)
        all_ids_data_for_predict_date = pd.DataFrame()

        for store in stores_list:
            all_id_data_in_store = pd.DataFrame()
            store_data_df = regular_data_df[regular_data_df[global_config.STORE_COLUMN_NAME] == store]
            store_future_features = far_future_features_df[store]  # feature
            store_lags_df = StoreLagFeatureGenerator().create_all_stores_lags(store_data_df,
                                                                              predict_date=begin_predict_dates)  # feature
            stores_weather_df = WeatherFeatureGenerator().generate(store_location_df=store_location_df, store_id=store,
                                                                   start_predict_date=begin_predict_dates,
                                                                   end_predict_date=begin_predict_dates)

            for item in store_data_df[global_config.ITEM_COLUMN_NAME].unique():
                _id = str(item) + ", " + str(store)
                id_data_df = store_data_df[store_data_df[global_config.ITEM_STORE_COLUMN_NAME] == _id]

                id_data_df = IDLagFeatureGenerator().create_id_lags(id_data_df=id_data_df, item=item, store=store,
                                                                    predict_date=begin_predict_dates)  # feature
                # id_data_df[global_config.ITEM_STORE_COLUMN_NAME] = _id
                all_id_data_in_store = pd.concat([all_id_data_in_store, id_data_df])

            all_id_data_in_store = all_id_data_in_store.merge(store_future_features,
                                                              on=[global_config.DATE_COLUMN_NAME,
                                                                  global_config.ITEM_COLUMN_NAME,
                                                                  global_config.STORE_COLUMN_NAME],
                                                              how="left")

            all_id_data_in_store = all_id_data_in_store.merge(store_lags_df,
                                                              on=[global_config.DATE_COLUMN_NAME],
                                                              how="left")
            all_id_data_in_store = all_id_data_in_store.merge(stores_weather_df, on=[global_config.DATE_COLUMN_NAME,
                                                                                     global_config.STORE_COLUMN_NAME],
                                                              how="left")

            all_id_data_in_store = all_id_data_in_store.merge(cumulative_features_df,
                                                              on=[global_config.DATE_COLUMN_NAME,
                                                                  global_config.ITEM_COLUMN_NAME,
                                                                  global_config.STORE_COLUMN_NAME], how="left")

            all_ids_data_for_predict_date = pd.concat([all_ids_data_for_predict_date, all_id_data_in_store])

        all_ids_data_for_predict_date = all_ids_data_for_predict_date.merge(item_lags_features_df,
                                                                            on=[global_config.DATE_COLUMN_NAME,
                                                                                global_config.ITEM_COLUMN_NAME,
                                                                                ],
                                                                            how="left")
        all_ids_data_for_predict_date = all_ids_data_for_predict_date.merge(final_event_features_df,
                                                                            on=[global_config.DATE_COLUMN_NAME],
                                                                            how="left")
        all_ids_data_for_predict_date.columns = all_ids_data_for_predict_date.columns.str.replace(':', '')
        cols_to_drop = [col for col in all_ids_data_for_predict_date.columns if 'MEST_all_time' in col
                        or 'months_5_6_7' in col or col == 'index']
        all_ids_data_for_predict_date.drop(cols_to_drop, axis=1, inplace=True)
        return all_ids_data_for_predict_date
