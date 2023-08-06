import datetime
ITEM_COLUMN_NAME = "item"
STORE_COLUMN_NAME = "store"
SALES_COLUMN_NAME = "sales"
DATE_COLUMN_NAME = "date"
ITEM_STORE_COLUMN_NAME = "item, store"
ITEM_STORE_COLUMN_NAME_LIST = ["item", "store"]
ID_COLUMN_NAME = "id"
SKU_COLUMN_NAME = "sku"
LIST_FREQ = ["D", "W-Mon", "M", "Y"]
START_DATE_CUMULATIVE_FEATURES = "2018-01-01"
tomorrow_date = str(datetime.datetime.now(datetime.timezone.utc).date()+datetime.timedelta(days=1))


DEFAULT_MARKETING_PLAN_FEATURES = {'project_name': 'examples',
                                   'task_name': 'marketing_plan_feature',
                                   'task_id': '630578192a1f432bb58240782f47a0d6',
                                   'artifact_name': 'marketing_plan_feature',
                                   }

DEFAULT_ITEM_SALE_ENCODED_FEATURES = {'project_name': 'examples',
                                     'task_name': 'mytest_item_store_sales_encoders_for_daily_preprocess',
                                     'task_id': 'b8e7efbdb4cc4aedb4da34512eccc30c',
                                     'artifact_name': 'item_encoders'}

DEFAULT_STORE_SALE_ENCODED_FEATURES = {'project_name': 'examples',
                                       'task_name': 'mytest_item_store_sales_encoders_for_daily_preprocess',
                                       'task_id': 'b8e7efbdb4cc4aedb4da34512eccc30c',
                                       'artifact_name': 'store_encoders'}

DEFAULT_EVENT_DATASET = {'dataset_project': 'palmers/datasets',
                         'dataset_name': 'fix_events',
                         'dataset_file_name': 'events_new_fix.csv',
                         'dataset_version': None,
                         'dataset_tags': None}

PCA_ENCODER_ARTIFACT_NAME='pca_dict'
COLUMNS_INTERACTIONS_ENCODER_ARTIFACT_NAME='columns_interactions_encoder'
APPLY_ENCODINGS_DICT_ARTIFACT_NAME='apply_encodings_dict'
APPLY_ENCODINGS_AT_ONCE_ARTIFACT_NAME='apply_encodings_at_once'


DEFAULT_EVENT_ENCODING_FEATURES = {'project_name': 'examples',
                                   'task_name': 'event_feature_fit',
                                   'task_id' : '8078f92691a54427b5123bc375efdd11',
                                   'artifacts_names': [APPLY_ENCODINGS_AT_ONCE_ARTIFACT_NAME, APPLY_ENCODINGS_DICT_ARTIFACT_NAME,
                                                       COLUMNS_INTERACTIONS_ENCODER_ARTIFACT_NAME, PCA_ENCODER_ARTIFACT_NAME]
                                   }



DEFAULT_HOLIDAYS_DATASET = {'dataset_project': 'palmers/datasets',
                            'dataset_name': 'events_holidays_raw',
                            'dataset_file_name': 'Holidays - holidays.csv',
                            'dataset_version': None,
                            'dataset_tags': None}

DEFAULT_STORE_LOCATION_DATASET = {'dataset_project': 'palmers/datasets',
                                  'dataset_name': 'stores_location',
                                  'dataset_file_name': 'store_location_df.csv',
                                  'dataset_version': None,
                                  'dataset_tags': None}

DEFAULT_EVENT_HANDLER_VARIABLES = {
    'max_date': 'max_date',
    'min_date': 'min_date',
    'date_min_col_list': "min_date_list",
    'target_col': 'sales',
    'date_col': 'date',
    'start_date': "2018-01-01",
    'holiday_col': "holiday_name",
    'holiday_col_type': "type",
    'duration_list_col': "duration_list",
    'event_num': 'num_event_id_list',
    'event_col_even': "event_id_list",
    'trend_col': 'rolling_7_mean',
    'window_size_list': list(range(1, 31)),
    'lags_list': list(range(1, 31)),
    'event_col_list': ["event_id_list", "sub_event_id_list"],
    'type_functions': ["mean", "std", "median"],
    'duration_list_cols': ['duration_list_mean_event', 'duration_list_median_event'],
    'weekend_col': "is_weekend",
    'year_forecast': None,  # 2022, not relevant to daily inference
    'pca_num': 2,
    'column_list_map_id': ['event_id', 'duration', 'min_date', 'sub_event_id', 'is_old', "max_date"],
    'cols_to_encode': ["type_holiday_name", "num_sub_event_id_list", "cumulative_sum_sales", "PC1", "PC2", "comments",
                  "fft_real", "fft_imag", "num_event_id_list", "duration_list_mean_event",
                  "duration_list_median_event",
                  "duration_list_std_event", 'is_weekend',
                  "ind_change_combo_event", 'is_sunday','is_tomorrow_event',"is_2_days_event"],

    'cols_to_encode_at_once':  ["num_sub_event_id_list", "num_event_id_list", "PC1",
                          "PC2", "fft_real", "fft_imag", "cumulative_sum_sales", "duration_list_mean_event",
                          "duration_list_std_event",
                          "duration_list_median_event",'is_tomorrow_event',"is_2_days_event"],
    'cols_days_for_ineraction' :['day_of_week', 'week_of_year', 'quarter', 'is_weekend', "ind_change_combo_event",
                            'is_sunday', "is_holday"],
    'type_encoder_list': ["MEstimateEncoder", "CatBoostEncoder"],
    'list_col_add': ["date"]
}

OUTLETS_SDATTA = [3, 18, 22, 28, 29, 44, 51, 57, 63, 73, 74, 76, 79, 88, 89, 91, 96, 100, 117, 119, 123, 130, 133, 135, 136, 141, 143, 144, 149, 150, 152, 162, 164, 166, 167, 168, 171, 172, 175, 179, 181, 184, 185, 186, 188, 189, 202, 214, 216, 217, 226, 3005, 3202, 3205, 3208, 4104, 4123, 4129, 4134, 4803, 4805,4904,4906]

OUTLETS_ALL = [3, 18, 22, 28, 44, 50, 55, 57, 68, 73, 74, 76, 79, 82, 88, 91, 96, 99, 100, 119, 123, 130, 133, 141, 144,
               149, 152, 162, 164, 166, 167, 168, 171, 173, 175, 180, 181, 184, 185, 186, 188, 189, 202, 203, 214, 216,
               218, 221, 226, 3005, 3202, 3205, 3208, 3290, 4104, 4123, 4129, 4132, 4133, 4134, 4803, 4805, 4904, 4906,
               4, 5, 7, 8, 10, 11, 15, 21, 26, 27, 29, 35, 36, 37, 42, 43, 45, 46, 47, 51, 52, 56, 61, 63, 64, 67, 69,
               81, 84, 85, 89, 90, 95, 104, 105, 106, 109, 114, 117, 121, 122, 135, 136, 143, 147, 150, 156, 159, 160,
               163, 170, 172, 174, 179, 182, 183, 201, 213, 215, 217, 219, 220, 225, 3245]
