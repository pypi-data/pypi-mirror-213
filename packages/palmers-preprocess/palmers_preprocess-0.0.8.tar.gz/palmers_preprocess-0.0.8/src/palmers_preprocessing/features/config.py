DICT_OF_TIME_INTERVAL = {"name_of_day":['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                  "month":[ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12],
                  "quarter": [1, 2, 3, 4],}

DICT_MAPPER = {"item": {"MEST": {"name_of_day":{} ,"month": {}, "quarter":{}},},
              "store": {"MEST": {"name_of_day":{} ,"month": {}, "quarter":{}},}}

ENCODERS_NAME = ["MEST"]

WEATHER_COLUMNS = ['tavg', 'tmin', 'tmax', 'prcp', 'snow', 'wspd', 'pres']


DAILY_LAGS_BACK = [1, 2, 3, 4, 5, 6, 7,12, 14, 18,21,24,312,313,364,365]
DAILY_WINDOWS = [1, 2, 3, 4, 5, 6, 7,12, 14, 18,21,24,312,313,364,365]
DAILY_DIFF_LAGS = [1, 2, 3, 4, 5, 6, 7,12, 14, 18,21,24,312,313,364,365]
DAILY_EWMS = [0.99, 0.95, 0.7, 0.1]