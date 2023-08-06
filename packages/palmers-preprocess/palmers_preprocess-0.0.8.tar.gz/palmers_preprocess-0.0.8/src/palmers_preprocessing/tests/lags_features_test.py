import sys

from src.palmers_preprocessing.preprocessor import Preprocessor

sys.path.append('../..')
from src.palmers_preprocessing.features.lags_features import StoreLagFeatureGenerator, SKULagFeatureGenerator, \
    IDLagFeatureGenerator


def test_store_lags():
    preprocessor = Preprocessor()
    predict_date = '2023-01-01'
    df = preprocessor.get_regular_data_of_store_and_add_future_date_and_filter_to_428_dates(store_id='109', predict_date=predict_date)
    df2 = StoreLagFeatureGenerator().create_all_stores_lags(store_data_df=df, predict_date=predict_date)

    print(df2)
    print(df2.info())


def test_sku_lags():
    preprocessor = Preprocessor()
    predict_date = '2023-01-01'
    df = preprocessor.get_regular_data_of_store_and_add_future_date_and_filter_to_428_dates(store_id=None, predict_date=predict_date)
    skus = df['sku'].unique()[0:5]
    df = df[df['sku'].isin(skus)]
    print(df.info())
    df2 = SKULagFeatureGenerator().create_all_sku_lags(regular_data_df=df, predict_date=predict_date)

    print(df2)
    print(df2.info())

def test_id_lags():
    preprocessor = Preprocessor()
    predict_date = '2023-01-01'
    df = preprocessor.get_regular_data_of_store_and_add_future_date_and_filter_to_428_dates(store_id='4906',
                                                                                     predict_date=predict_date)
    sku = 100002999000001
    df=df[df['sku']==sku]

    df2 = IDLagFeatureGenerator().create_id_lags(id_data_df=df, sku=sku, store=4906, predict_date=predict_date)

    print(df2)


#test_store_lags()
#test_sku_lags()
test_id_lags()
