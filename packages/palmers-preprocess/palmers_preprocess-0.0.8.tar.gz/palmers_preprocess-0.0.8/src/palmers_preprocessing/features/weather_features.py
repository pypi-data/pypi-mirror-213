import pandas as pd
from ..clearml_data_handler import DatasetLoader
from .. import config as global_config
from . import config as config

import pandas as pd
from meteostat import Point, Daily
from datetime import datetime


# class StoreLocationLoader:
#
#     @classmethod
#     def load(cls, dataset_project=global_config.DEFAULT_STORE_LOCATION_DATASET['dataset_project'],
#              dataset_name=global_config.DEFAULT_STORE_LOCATION_DATASET['dataset_name'],
#              dataset_version=global_config.DEFAULT_STORE_LOCATION_DATASET['dataset_version'],
#              dataset_tags=global_config.DEFAULT_STORE_LOCATION_DATASET['dataset_tags'],
#              dataset_file_name=global_config.DEFAULT_STORE_LOCATION_DATASET['dataset_file_name']
#              ):
#         store_location_dfs = DatasetLoader().load_dfs_from_dataset(dataset_project=dataset_project,
#                                                                    dataset_name=dataset_name,
#                                                                    dataset_version=dataset_version,
#                                                                    dataset_tags=dataset_tags,
#                                                                    dataset_file_names=[dataset_file_name])
#         store_location_df = store_location_dfs[dataset_file_name]
#         store_location_df = store_location_df.drop('Unnamed: 0', axis=1)
#
#         return store_location_df


class WeatherFeatureGenerator:
    @classmethod
    def load(cls, store_location_df, store_id, start_date, end_date, weather_columns=config.WEATHER_COLUMNS):
        """
        Load weather data for specific store
        Args:
            store_location_df:  store location dataframe
            store_id:         store id
            start_date:     start date
            end_date:    end date
            weather_columns:    weather columns

        Returns:
            dataframe: dataframe with weather data for specific store
        """
        store_weather_df = cls.return_df_of_stores_weather(stores_location_df=store_location_df,
                                                          store_id=store_id,
                                                          start_date_str=start_date,
                                                          end_date_str=end_date,
                                                          weather_columns=weather_columns)

        return store_weather_df

    @classmethod
    def return_weather_daily_data_for_specific_location(cls, start_date, end_date, latitude, longitude):
        """
        Return weather data for specific location and time period
        Args:
            start_date:     start date
            end_date:   end date
            latitude:   latitude
            longitude:  longitude

        Returns:
            dataframe: dataframe with weather data for specific location and time period
        """
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        vienna = Point(float(latitude), float(longitude))
        data = Daily(vienna, start, end)
        data = data.fetch()
        if "tavg" in data.columns:
            data['tavg'].interpolate(method='linear', limit_area='outside', inplace=True)
        if "tmin" in data.columns:
            data['tmin'].interpolate(method='linear', limit_area='outside', inplace=True)
        if "tmax" in data.columns:
            data['tmax'].interpolate(method='linear', limit_area='outside', inplace=True)
        if 'pres' in data.columns:
            data['pres'].interpolate(method='linear', limit_area='outside', inplace=True)
        if 'prcp' in data.columns:
            data['prcp'].fillna(0, inplace=True)
        if 'snow' in data.columns:
            data['snow'].fillna(0, inplace=True)
        if 'wspd' in data.columns:
            data['wspd'].fillna(0, inplace=True)
        if data['pres'].isnull().values.any():
            data["pres"] = 0
        data.interpolate('linear', inplace=True)
        return data

    @classmethod
    def return_df_of_stores_weather(cls, stores_location_df, store_id, start_date_str, end_date_str, weather_columns,
                                    lat_vienna=48.2082,
                                    lon_vienna=16.3738):
        """
        Return weather data for specific store and time period and if not available for vienna
        Args:
            stores_location_df:     store location dataframe
            store_id:   store id
            start_date_str:     start date
            end_date_str:   end date
            weather_columns:    weather columns
            lat_vienna:     latitude_vienna
            lon_vienna:     longitude_vienna

        Returns:
            dataframe: dataframe with weather data for specific store and time period and if not available for vienna
        """

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        delta = end_date - start_date

        stores_location_df['store_id'] = stores_location_df['store_id'].astype(int)

        store_location = stores_location_df[stores_location_df['store_id'] == store_id]
        latitude = store_location['latitude'].values[0]
        longitude = store_location['longitude'].values[0]
        df_weather_of_store = \
            cls.return_weather_daily_data_for_specific_location(start_date_str,end_date_str, latitude,longitude)[weather_columns]
        if (len(df_weather_of_store) < delta.days) or (df_weather_of_store.isna().sum().sum() > 0) or len(
                df_weather_of_store) == 0:
            df_weather_of_store = \
                cls.return_weather_daily_data_for_specific_location(start_date_str,
                                                                    end_date_str, lat_vienna,
                                                                    lon_vienna)[
                    weather_columns]

        df_weather_of_store['store'] = store_id
        df_weather_of_store['store'] = df_weather_of_store['store'].astype(int)


        return df_weather_of_store.reset_index().rename(columns={"index": "date", "time": "date"})

    @classmethod
    def generate(cls, store_location_df, store_id, start_predict_date, end_predict_date, weather_columns=config.WEATHER_COLUMNS):
        """
        Generate weather data for specific store and time period
        Args:
            store_location_df:      store location dataframe
            store_id:     store id
            start_predict_date:     start date
            end_predict_date:   end date
            weather_columns:    weather columns

        Returns:
            dataframe: dataframe with weather data for specific store and time period
        """
        # store_location_df = StoreLocationLoader.load()
        store_weather_df = cls.load(store_location_df=store_location_df, store_id=store_id, start_date=start_predict_date, end_date=end_predict_date, weather_columns=weather_columns)
        return store_weather_df


