import sys
sys.path.append('../..')
from src.palmers_preprocessing.features.future_features import MarketingPlanFeatures, ItemSaleEncodedFeatures, \
    StoreSaleEncodedFeatures, FarFutureFeaturesGenerator
from src.palmers_preprocessing.clearml_data_handler import TaskLoader, ArtifactLoader


def test_marketing_plan_features():
    mpf = MarketingPlanFeatures()
    df = mpf.load()
    print(df)
    print(df.info())

def test_sku_sale_encoded_features():
    ssef = ItemSaleEncodedFeatures()
    df = ssef.load()
    print(df)
    print(df.info())


def test_store_sale_encoded_features():
    ssef = StoreSaleEncodedFeatures()
    df = ssef.load()
    print(df)
    print(df.info())


def test_task_loader():
    tl = ArtifactLoader()
    tt = tl.load_artifact_as_df(artifact_name='sku_sales_encoders',  project_name="examples",
                            task_name="sku_store_sales_encoders",
                            task_id="a313d610ce5a43f6936f50a103984096", tags=None
                        )
    print(tt)


def test_far_future_feature_generator():
    fffg = FarFutureFeaturesGenerator()
    import config_batch_dict as cbd
    d = fffg.far_future_features_preprocess_of_store(cbd.ids_batches['3'])
    print(d)
    print(d.info())



def test_far_future_feature_generator_2():
    fffg = FarFutureFeaturesGenerator()
    import config_batch_dict as cbd
    subdict = {k: v for k, v in cbd.ids_batches.items() if k in ['4906', '3']}

    a = fffg.far_future_features_preprocess_of_several_stores(subdict, begin_predict_dates='2023-05-01')
    print(a)
    print(a['4906'].columns.tolist())
    print(a['4906'].info())



#test_marketing_plan_features()
#test_sku_sale_encoded_features()
#test_store_sale_encoded_features()
#test_far_future_feature_generator()
test_far_future_feature_generator_2()