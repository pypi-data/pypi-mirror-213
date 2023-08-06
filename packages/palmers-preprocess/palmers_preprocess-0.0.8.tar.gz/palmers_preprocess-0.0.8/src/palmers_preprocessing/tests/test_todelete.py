from src.palmers_preprocessing.regular_data_handler import RegularDataLoader


def test_function():
    reg = RegularDataLoader().load_specific()

    sku_store_dict = reg.groupby('store')['sku, store'].unique().apply(list).to_dict()
    # count the number of items in the entire dict:
    print(sku_store_dict)
    print(len(sku_store_dict))
    print(type(sku_store_dict))
    print(sum([len(v) for v in sku_store_dict.values()]))





test_function()