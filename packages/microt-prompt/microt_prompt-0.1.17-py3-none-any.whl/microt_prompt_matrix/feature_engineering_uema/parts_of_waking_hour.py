import pandas as pd
import numpy as np
from datetime import datetime


def convert_time_str_to_datetime(time_str_series):
    converter = lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S") if (type(x) == str) else x
    time_datetime_list = [x.split(" ")[0] + " " + x.split(" ")[1].split(".")[0] if type(x) == str else x for x in
                          list(time_str_series)]

    time_datetime_list = pd.Series(map(converter, time_datetime_list))

    return time_datetime_list


def create_column(feature_df, parts_num):
    print("\n> start generating the feature: Parts of waking hours")
    wake_time_datetime_list = convert_time_str_to_datetime(feature_df["WAKE_TIME"])
    sleep_time_datetime_list = convert_time_str_to_datetime(feature_df["SLEEP_TIME"])
    prompt_time_datetime_list = feature_df["Actual_Prompt_Local_DateTime"]

    proximity_to_wake_time_column = [(y - x).total_seconds() / 60 if ((type(x) != float) and (type(y) != float)) else np.nan
                                     for x, y in zip(wake_time_datetime_list, prompt_time_datetime_list)]
    proximity_to_sleep_time_column = [(y - x).total_seconds() / 60 if ((type(x) != float) and (type(y) != float)) else np.nan
                                      for x, y in zip(prompt_time_datetime_list, sleep_time_datetime_list)]
    wake_duration = [(y - x).total_seconds() / 60 if ((type(x) != float) and (type(y) != float)) else np.nan for x, y in
                     zip(wake_time_datetime_list, sleep_time_datetime_list)]
    duration_per_part = [x // parts_num if x == x else x for x in wake_duration]
    parts_of_waking_hour_column = [y // x if ((x == x) and (y == y)) else np.nan for x, y in
                                   zip(duration_per_part, proximity_to_wake_time_column)]

    print("     --- success")

    return parts_of_waking_hour_column, proximity_to_wake_time_column, proximity_to_sleep_time_column