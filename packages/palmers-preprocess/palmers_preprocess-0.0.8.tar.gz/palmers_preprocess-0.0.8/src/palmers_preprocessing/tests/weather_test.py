import sys
sys.path.append('../..')
from src.palmers_preprocessing.features.weather_features import WeatherFeatureGenerator, StoreLocationLoader


def test_weather_feature_generator():
    store_location_df = StoreLocationLoader.load()
    print(WeatherFeatureGenerator.load(store_location_df, store_id=100, start_date='2023-01-01', end_date='2023-01-01'))
    print(WeatherFeatureGenerator.load(store_location_df, store_id=109, start_date='2023-04-25', end_date='2023-05-25'))




def test_store_location_df():
    store_location_df = StoreLocationLoader.load()
    print(store_location_df)
    print(store_location_df.columns)

#test_store_location_df()
test_weather_feature_generator()
