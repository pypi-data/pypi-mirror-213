import pandas as pd
from .utils import parse_regular_data_columns
from . import config, clearml_data_handler as cdh

class RegularDataLoader:
    @classmethod
    def load(cls):
        # Load data
       return cls.load_specific()

    @classmethod
    def load_specific(cls):
        # Load data


        file_name = "not_sparse_data_gap_until_2023_05_22.csv"
        dataset_df_files = cdh.DatasetLoader().load_dfs_from_dataset(dataset_project='palmers/datasets',
                                                                     dataset_name="gap_filling_for_models_until_2023_05_22"
                                              , dataset_file_names=[file_name])
        regular_data_df = dataset_df_files[file_name]#.drop('Unnamed: 0', axis=1)
        return regular_data_df




class RegularDataProcessor:
    @classmethod
    def load(cls, predict_date):
        regular_data_df = RegularDataLoader().load()

        # process here regular data
        pass
