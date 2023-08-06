import sys
import catboost

from src.palmers_preprocessing.regular_data_handler import RegularDataLoader
import pandas as pd
sys.path.append('../..')
from src.palmers_preprocessing.preprocessor import Preprocessor
from src.palmers_preprocessing.utils import convert_df_with_sku_to_df_with_item, daily_sales_to_weekly_mean_sales
from clearml import Model, InputModel, Task
import pickle

def test_prepreocessor():
    preprocessor = Preprocessor()
    stores = ['3']
    print("Loading data...")
    df = RegularDataLoader().load()
    print(df['store'].unique().tolist())
    print("Data loaded")
    df = df[df['store'].isin(stores)]
    print("Data filtered")
    print(df.head())
    print("Convert df with sku to df with item")
    df = convert_df_with_sku_to_df_with_item(df)
    print(df.info())

  #  items_1 = df[df['store'] == '100']['item'].unique()
  #  items_2 = df[df['store'] == '3']['item'].unique()
  #  df = df[df['item'].isin(items_1) | df['item'].isin(items_2)]
    print(df["item, store"].unique())
    print("Daily Sales to weekly mean sales")
    df = daily_sales_to_weekly_mean_sales(df)
    df = preprocessor.preprocess(stores_list=[3], begin_predict_dates='2023-05-23', regular_data_df=df)
    pd.set_option('display.max_rows', None)
    print(df.isnull().sum())
    print(df)
    print(df.columns.tolist())
    return df
# def test_cumulative_features():
#     preprocessor = Preprocessor()
#     df = preprocessor.get_regular_data_of_store(store_id='109', predict_date='2023-05-23')
#     cum_feat = preprocessor.get_cumulative_features(df)
#     print(cum_feat)


task = Task.init(project_name='test_predict_store_3', task_name='test_predict_store_3')
model_id = '3e2ac457fc644f39b4eb6d5a68e84dfb'  # Replace with your actual model ID
print("111")
models_store_3_path = Model(model_id).get_local_copy()
print("222")
with open(models_store_3_path, 'rb') as f:
     model_3 = pickle.load(f)['3']
print(model_3)
print("333")
df = test_prepreocessor()
for item_store in model_3.keys():
    model = model_3[item_store]['model']
    prediction = model.predict(df[df["item, store"] == item_store][model.feature_names_])[0]
    print("Item store: ", item_store, "prediction: ", prediction)


