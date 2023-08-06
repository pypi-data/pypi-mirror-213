import os
from os import sep
from glob import glob
import pandas as pd
import numpy as np
import bisect
from datetime import datetime, timedelta
from microt_prompt_matrix import utils
from microt_prompt_matrix.utils.get_time_diff import *

target_file_pattern = 'phone_detected_activity_clean*.csv'
detected_activity_columns = ["IN_VEHICLE", "ON_BIKE", "ON_FOOT", "RUNNING", "STILL", "TILTING", "WALKING", "UNKNOWN"]


def validate_dates_before_after(intermediate_participant_path, date_in_study):
    validated_date_list = []

    # target date
    date_folder_path = intermediate_participant_path + sep + date_in_study
    target_date_log_paths = sorted(glob(os.path.join(date_folder_path, target_file_pattern)))  # file name
    if len(target_date_log_paths) == 0:
        print("No daily file of phone detected activity on {}".format(date_in_study))
    else:
        # 1 day before target date
        date_format = "%Y-%m-%d"
        one_date_before_datetime = datetime.strptime(date_in_study, date_format).date() - timedelta(days=1)
        one_date_before = one_date_before_datetime.strftime(date_format)
        date_folder_path = intermediate_participant_path + sep + one_date_before
        one_day_before_log_paths = sorted(glob(os.path.join(date_folder_path, target_file_pattern)))  # file name
        if len(one_day_before_log_paths) != 0:
            validated_date_list.append(one_date_before)

        # target date
        validated_date_list.append(date_in_study)

        # 1 day after target date
        date_format = "%Y-%m-%d"
        one_date_after_datetime = datetime.strptime(date_in_study, date_format).date() + timedelta(days=1)
        one_date_after = one_date_after_datetime.strftime(date_format)
        date_folder_path = intermediate_participant_path + sep + one_date_after
        one_day_after_log_paths = sorted(glob(os.path.join(date_folder_path, target_file_pattern)))  # file name
        if len(one_day_after_log_paths) != 0:
            validated_date_list.append(one_date_after)

    return validated_date_list


def clean_dataframe(df):
    df.reset_index(inplace=True, drop=True)
    dropped_rows = []
    for idx in df.index:
        local_time_str = df["LOG_TIME"][idx]
        if (local_time_str == "-1") or ("-1 " in local_time_str) or len(local_time_str.split(' ')) > 3 or len(
                local_time_str.split('-')[0]) > 4 or len(local_time_str.split(' ')) < 2:
            dropped_rows.append(idx)
    df = df.drop(dropped_rows)

    df.reset_index(inplace=True, drop=True)
    return df


def combine_intermediate_file(intermediate_participant_path, date_in_study):
    df_logs_combined = pd.DataFrame()
    participant_id = utils.extract_participant_id.extract_participant_id(intermediate_participant_path)

    # generate date range where date folder exists (sharable code in utils)
    validated_date_list = validate_dates_before_after(intermediate_participant_path, date_in_study)
    if len(validated_date_list) == 0:
        print("Cannot find logs file around {}".format(date_in_study))
        return df_logs_combined

    for date in validated_date_list:
        date_folder_path = intermediate_participant_path + sep + date
        csv_path_list = sorted(glob(os.path.join(date_folder_path, target_file_pattern)))  # file name

        csv_path = csv_path_list[0]
        try:
            df_day = pd.read_csv(csv_path)
        except pd.errors.EmptyDataError:
            raise Exception("pandas.errors.EmptyDataError (phone detected activity) : " + csv_path)

        if df_day.shape[0] > 0:
            df_day['Participant_ID'] = [participant_id] * df_day.shape[0]
            df_logs_combined = pd.concat([df_logs_combined, df_day])

    converter = lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
    df_logs_combined = df_logs_combined.dropna(subset=['LOG_TIME'])
    df_logs_combined = clean_dataframe(df_logs_combined)

    try:
        df_logs_combined["Local_Time"] = [x.split(" ")[0] + " " + x.split(" ")[1] for x in
                                          list(df_logs_combined["LOG_TIME"])]

        # converter2 = lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
        df_logs_combined['Local_Timestamp'] = pd.Series(map(converter, df_logs_combined["Local_Time"]))
        # print(df_logs_combined['Local_Timestamp'])
        df_logs_combined['Date'] = df_logs_combined['Local_Timestamp'].dt.date
    except IndexError:
        raise Exception(
            "IndexError: list index out of range (phone detected activity) : " + intermediate_participant_path + sep + date_in_study + str(
                list(df_logs_combined["LOG_TIME"])))
    except Exception:
        raise Exception("Exception (phone detected activity) : " + intermediate_participant_path + sep + date_in_study)

    return df_logs_combined


def find_closest_time(prompt_time, subset_time_list):
    i = bisect.bisect_left(subset_time_list, prompt_time)
    closet_time = min(subset_time_list[max(0, i - 1): i + 2], key=lambda t: abs(prompt_time - t))
    return closet_time


def match_feature(prompt_local_datetime_series, df_logs_combined):
    print("     --- start matching")
    detected_activity_list = []
    matched_time_list = []

    for idx in prompt_local_datetime_series.index:
        prompt_time = prompt_local_datetime_series[idx]
        # prompt_date = prompt_time.date()

        if df_logs_combined.shape[0] == 0:
            detected_activity = "NF"
            closest_time = "NF"
        else:
            subset_time_list = list(df_logs_combined["Local_Timestamp"])

            closest_time = find_closest_time(prompt_time, subset_time_list)

            # check if matched time is 5 minutes away from prompt time
            # if get_min_diff(prompt_time, closest_time) < 5:
            df_closest = df_logs_combined[df_logs_combined['Local_Timestamp'] == closest_time][
                detected_activity_columns]
            #             detected_activity = list(df_closest.idxmax(axis=1))[0]
            detected_activity = \
            list(df_closest.eq(df_closest.max(1), axis=0).dot(df_closest.columns + ',').str.rstrip(','))[0]
            # else:
            #     detected_activity = "NF"

        matched_time_list.append(closest_time)
        detected_activity_list.append(detected_activity)

    return detected_activity_list, matched_time_list


def transform(battery_level_column):
    # return [1 if x >= 15 else 0 for x in battery_level_column]
    return battery_level_column


def create_column(prompt_local_datetime_series, intermediate_participant_path, date_in_study):
    print("\n> start generating the feature: phone detected activity ")

    # Read, parse and combine related intermediate file
    df_logs_combined = combine_intermediate_file(intermediate_participant_path, date_in_study)

    if df_logs_combined.shape[0] > 0:
        # Match the combined parsed intermediate file with prompt feature data frame
        detected_activity_column, match_time = match_feature(prompt_local_datetime_series, df_logs_combined)
    else:
        detected_activity_column = ["NF"] * len(prompt_local_datetime_series)
        match_time = ["NF"] * len(prompt_local_datetime_series)

    # transform feature
    phone_detected_activity_column_transformed = transform(detected_activity_column)
    print("     --- success")

    return phone_detected_activity_column_transformed, match_time
