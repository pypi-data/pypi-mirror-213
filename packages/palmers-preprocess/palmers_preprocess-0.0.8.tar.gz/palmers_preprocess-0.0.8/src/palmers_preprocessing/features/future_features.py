import pandas as pd
from .. import config as global_config
from . import config
from ..utils import process_date_column, add_values_to_dict_mapper, map_encoders_columns_to_base_df

def clean_marketing(marketing_plan_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean marketing plan df from unnecessary columns and convert columns to int32
    Args:
        marketing_plan_df:

    Returns:

    """
    marketing_plan_df = marketing_plan_df.loc[:,
                        ~marketing_plan_df.columns.str.contains('Unnamed')]
    marketing_plan_df = marketing_plan_df.dropna()

    cols_to_convert = marketing_plan_df.columns.difference(['date'])
    marketing_plan_df[cols_to_convert] = marketing_plan_df[cols_to_convert].astype('int32')

    return marketing_plan_df


def clean_item_encoder(item_encoders):
    """
    Clean item encoder df from unnecessary columns and convert columns to int64
    Args:
        item_encoders:  item encoder df

    Returns:
        item_encoders
    """
    item_encoders = item_encoders.drop('Unnamed: 0', axis=1)
    item_encoders[global_config.ITEM_COLUMN_NAME] = item_encoders[global_config.ITEM_COLUMN_NAME].astype('int64')
    item_encoders = item_encoders.set_index(global_config.ITEM_COLUMN_NAME)
    item_encoders = item_encoders.astype('float')
    return item_encoders


def clean_store_encoder(store_encoders):
    """
    Clean store encoder df from unnecessary columns and convert columns to int32
    Args:
        store_encoders:     store encoder df

    Returns:
        store_encoders
    """
    store_encoders = store_encoders.drop('Unnamed: 0', axis=1)
    store_encoders[global_config.STORE_COLUMN_NAME] = store_encoders[global_config.STORE_COLUMN_NAME].astype(
        'int32')
    store_encoders = store_encoders.set_index(global_config.STORE_COLUMN_NAME)
    store_encoders = store_encoders.astype('float')
    return store_encoders


class FarFutureFeaturesGenerator:

    @classmethod
    def far_future_features_preprocess_of_store(cls, marketing_plan: pd.DataFrame, item_encoders , store_encoders, store_batch,
                                                begin_predict_dates: str) -> pd.DataFrame:
        """
        Preprocess of store for far future features generation
        following the steps:
        1) clean marketing plan df
        2) clean item encoder df
        3) clean store encoder df
        4) add values to dict mapper
        5) create future date range
        6) create future features df
        7) create future features df with store batch
        8) create future features df with store batch and begin predict dates
        9) create future features df with store batch and begin predict dates and marketing plan
        10) create future features df with store batch and begin predict dates and marketing plan and item encoders
        Args:
            marketing_plan:     marketing plan df
            item_encoders:    item encoder df
            store_encoders:     store encoder df
            store_batch:    store batch
            begin_predict_dates:    begin predict dates

        Returns:
            output_df : future features df with store batch and begin predict dates and marketing plan and item encoders
        """
        marketing_plan = clean_marketing(marketing_plan)
        item_encoders = clean_item_encoder(item_encoders)
        store_encoders = clean_store_encoder(store_encoders)

        dict_mapper = add_values_to_dict_mapper(config.DICT_MAPPER, item_encoders, global_config.ITEM_COLUMN_NAME,
                                                config.ENCODERS_NAME,
                                                config.DICT_OF_TIME_INTERVAL)

        dict_mapper = add_values_to_dict_mapper(dict_mapper, store_encoders, global_config.STORE_COLUMN_NAME,
                                                config.ENCODERS_NAME,
                                                config.DICT_OF_TIME_INTERVAL)

        future_date_range = pd.date_range(start=begin_predict_dates, end=begin_predict_dates, freq='D')

        output_df = pd.DataFrame()
        for _id in store_batch:
            item_store_id = _id
            item = int(item_store_id.split(',')[0])
            store = int(item_store_id.split(',')[1])
            id_data_future = pd.DataFrame({'date': future_date_range,
                                           'item, store': item_store_id,
                                           'item': item,
                                           'store': store})

            id_data_future = process_date_column(id_data_future, global_config.DATE_COLUMN_NAME, expanded=True)

            # Exclude Sunday
            # id_data_future = id_data_future[id_data_future['day_of_week'] != 6]

            marketing_plan[global_config.DATE_COLUMN_NAME] = pd.to_datetime(
                marketing_plan[global_config.DATE_COLUMN_NAME])

            id_data_future = pd.merge(id_data_future, marketing_plan, on=[global_config.DATE_COLUMN_NAME], how='left')

            id_data_future = map_encoders_columns_to_base_df(id_data_future, dict_mapper, config.ENCODERS_NAME)
            output_df = pd.concat([output_df, id_data_future])

        # output_df.drop('name_of_day', axis=1, inplace=True)
        return output_df

    @classmethod
    def far_future_features_preprocess_of_several_stores(cls, marketing_plan: pd.DataFrame, item_encoders, store_encoders, store_batch_dict, begin_predict_dates: str) -> pd.DataFrame:
        """
        Preprocess of store for far future features generation
        following the steps:
        1) clean marketing plan df
        2) clean item encoder df
        3) clean store encoder df
        4) add values to dict mapper
        5) create future date range
        6) create future features df
        7) create future features df with store batch
        8) create future features df with store batch and begin predict dates
        9) create future features df with store batch and begin predict dates and marketing plan
        10) create future features df with store batch and begin predict dates and marketing plan and item encoders
        Args:
            marketing_plan:     marketing plan df
            item_encoders:    item encoder df
            store_encoders:     store encoder df
            store_batch:    store batch
            begin_predict_dates:    begin predict dates

        Returns:
            output_df : future features df with store batch and begin predict dates and marketing plan and item encoders
        """

        marketing_plan = clean_marketing(marketing_plan)
        item_encoders = clean_item_encoder(item_encoders)
        store_encoders = clean_store_encoder(store_encoders)

        dict_mapper = add_values_to_dict_mapper(config.DICT_MAPPER, item_encoders, global_config.ITEM_COLUMN_NAME,
                                                config.ENCODERS_NAME,
                                                config.DICT_OF_TIME_INTERVAL)

        dict_mapper = add_values_to_dict_mapper(dict_mapper, store_encoders, global_config.STORE_COLUMN_NAME,
                                                config.ENCODERS_NAME,
                                                config.DICT_OF_TIME_INTERVAL)

        future_date_range = pd.date_range(start=begin_predict_dates, end=begin_predict_dates, freq='D')

        output_dfs = {}
        for store_id in list(store_batch_dict.keys()):
            output_df = pd.DataFrame()
            for _id in store_batch_dict[store_id]:
                item_store_id = _id
                item = int(item_store_id.split(',')[0])
                store = int(item_store_id.split(',')[1])
                id_data_future = pd.DataFrame({'date': future_date_range,
                                               'item, store': item_store_id,
                                               'item': item,
                                               'store': store})
                id_data_future = process_date_column(id_data_future, global_config.DATE_COLUMN_NAME, expanded=True)

                # Exclude Sunday
                # id_data_future = id_data_future[id_data_future['day_of_week'] != 6]

                marketing_plan[global_config.DATE_COLUMN_NAME] = pd.to_datetime(
                    marketing_plan[global_config.DATE_COLUMN_NAME])
                id_data_future = pd.merge(id_data_future, marketing_plan, on=[global_config.DATE_COLUMN_NAME],
                                          how='left')
                id_data_future = map_encoders_columns_to_base_df(id_data_future, dict_mapper, config.ENCODERS_NAME)
                output_df = pd.concat([output_df, id_data_future])

            # output_df.drop('name_of_day', axis=1, inplace=True)
            output_dfs[store_id] = output_df
        return output_dfs
