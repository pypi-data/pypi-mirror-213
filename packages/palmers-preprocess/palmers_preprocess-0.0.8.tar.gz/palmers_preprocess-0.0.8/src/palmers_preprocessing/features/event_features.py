import pandas as pd

from .. import config as global_config
from .. import events_handler as eh
from ..utils import next_two_days_skip_sunday, parse_regular_data_columns



class EventFeaturesGenerator:
    @classmethod
    def apply_encoder(cls, df, encoder, columns, columns_after_apply, fillna=False):
        if fillna:
            df[columns_after_apply] = encoder.transform(df[columns].fillna(0))
        else:
            df[columns_after_apply] = encoder.transform(df[columns])

        return df

    @classmethod
    def perform_encoders(cls, processed_event_features_df, event_encoders):
        pca_dict = event_encoders[global_config.PCA_ENCODER_ARTIFACT_NAME]['pca_weights']
        cls.apply_encoder(df=processed_event_features_df,
                          encoder=pca_dict['pca'],
                          columns=pca_dict['columns'],
                          columns_after_apply=pca_dict['columns_after_apply'],
                          fillna=True)

        apply_encoding_dict = event_encoders[global_config.APPLY_ENCODINGS_DICT_ARTIFACT_NAME]
        for key in apply_encoding_dict.keys():
            encoder_dict = apply_encoding_dict[key]
            cls.apply_encoder(df=processed_event_features_df,
                              encoder=encoder_dict['encoder'],
                              columns=encoder_dict['columns'],
                              columns_after_apply=key)

        for encoder_name in ['MEstimateEncoder', 'CatBoostEncoder']:
            encoder_model = event_encoders[global_config.APPLY_ENCODINGS_AT_ONCE_ARTIFACT_NAME][encoder_name]
            cls.apply_encoder(df=processed_event_features_df,
                              encoder=encoder_model['encoder'],
                              columns=encoder_model['columns'],
                              columns_after_apply=encoder_model['columns_after_apply']
                              )

        processed_event_features_df = eh.create_interactions_columns(processed_event_features_df)
        for encoder_name in ['MEstimateEncoder', 'CatBoostEncoder']:
            encoder_model = event_encoders[global_config.COLUMNS_INTERACTIONS_ENCODER_ARTIFACT_NAME][encoder_name]
            cls.apply_encoder(df=processed_event_features_df,
                              encoder=encoder_model['encoder'],
                              columns=encoder_model['columns'],
                              columns_after_apply=encoder_model['columns_after_apply']
                              )
        return processed_event_features_df

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

        return pd.concat(dfs)

    @classmethod
    def generate_event_features(cls, regular_data_df, event_df, holiday_df,event_encoders, begin_predict_dates):
        """
        Generates the event features for the future rows by the following steps:
        1) start_date,end_date from next_two_days_skip_sunday
        2) get_future_rows: creates the future rows for prediction as a dataframe
        3) parse_regular_data_columns: parses the regular data columns
        4) run_pipline_event: runs the event pipeline from the event handler
        5) perform_encoders: performs the encoders on the event features
        6) finalize and remove columns: finalizes the event features and removes the columns that are not needed
        7) return the event features dataframe
        Args:
            regular_data_df:    regular data dataframe
            event_df:        event dataframe
            holiday_df:       holiday dataframe
            event_encoders:  event encoders
            begin_predict_dates:    begin predict dates

        Returns:
           processed_event_features_df : dataframe
        """

        start_date,end_date = next_two_days_skip_sunday(begin_predict_dates)[0]
        end_date = next_two_days_skip_sunday(begin_predict_dates)[-1]
        future_df = cls.get_future_rows(regular_data_df, start_date, end_date)
        df_with2days = pd.concat([regular_data_df, future_df], ignore_index=True)
        df_with2days = parse_regular_data_columns(df_with2days)
        processed_event_features_df = eh.run_pipline_event(data_event=event_df, data_sales=df_with2days,
                                                           data_hol=holiday_df)

        processed_event_features_df = cls.perform_encoders(processed_event_features_df, event_encoders)

        processed_event_features_df = eh.finalize_data(processed_event_features_df)

        df_final_event_features = processed_event_features_df.loc[:,
                                  ~processed_event_features_df.columns.str.contains('Unnamed')]

        df_final_event_features[global_config.DATE_COLUMN_NAME] = pd.to_datetime(
            df_final_event_features[global_config.DATE_COLUMN_NAME])
        df_final_event_features.set_index(global_config.DATE_COLUMN_NAME, inplace=True)

        df_final_event_features.fillna(0, inplace=True)
        df_final_event_features.reset_index(inplace=True)

        processed_event_features_df = processed_event_features_df[
            processed_event_features_df[global_config.DATE_COLUMN_NAME] == begin_predict_dates]
        return processed_event_features_df

    @classmethod
    def generate(cls, regular_data_df, event_df, holiday_df,event_encoders, begin_predict_dates):
        """
        Generates the event features for the future rows by the following steps:
        1) generate_event_features: generates the event features for the future rows
        2) filter date and columns: filters the date and columns
        Args:
            regular_data_df:    regular data dataframe
            event_df:     event dataframe
            holiday_df:   holiday dataframe
            event_encoders: event encoders
            begin_predict_dates:        begin predict dates

        Returns:
            processed_event_features_df: processed event features dataframe

        """

        processed_event_features_df = cls.generate_event_features(regular_data_df, event_df, holiday_df,event_encoders,
                                                                  begin_predict_dates=begin_predict_dates)
        processed_event_features_df = processed_event_features_df[
            processed_event_features_df[global_config.DATE_COLUMN_NAME] == begin_predict_dates]
        processed_event_features_df.drop(columns=[global_config.SALES_COLUMN_NAME], inplace=True)
        return processed_event_features_df
