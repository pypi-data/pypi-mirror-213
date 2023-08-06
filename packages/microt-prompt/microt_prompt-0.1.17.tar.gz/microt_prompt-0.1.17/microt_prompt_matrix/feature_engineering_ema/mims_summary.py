import os
from os import sep
from glob import glob
import pandas as pd
import numpy as np
import bisect
from datetime import datetime, timedelta
from microt_prompt_matrix import utils
from microt_prompt_matrix.utils.get_time_diff import *

target_file_pattern_mims = 'watch_accelerometer_mims_clean*.csv'
target_file_pattern_mims_minute = 'watch_accelerometer_mims_minute*.csv'
target_file_pattern_swan_minute = 'watch_accelerometer_swan_minute*.csv'
mims_cutoff_list = {"sedentary": 10.558, "light": 15.047, "moderate": 19.614, "vigorous": 19.614}

def validate_dates_before_after(intermediate_participant_path, date_in_study, target_file_pattern):
    validated_date_list = []

    # target date
    date_folder_path = intermediate_participant_path + sep + date_in_study
    target_date_log_paths = sorted(glob(os.path.join(date_folder_path, target_file_pattern)))  # file name
    if len(target_date_log_paths) == 0:
        print("No battery daily file on {}".format(date_in_study))
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


def combine_intermediate_mims_file(intermediate_participant_path, date_in_study, target_file_pattern):
    df_logs_combined = pd.DataFrame()
    participant_id = utils.extract_participant_id.extract_participant_id(intermediate_participant_path)

    # generate date range where date folder exists (sharable code in utils)
    validated_date_list = validate_dates_before_after(intermediate_participant_path, date_in_study, target_file_pattern)
    if len(validated_date_list) == 0:
        print("Cannot find logs file around {}".format(date_in_study))
        return df_logs_combined

    for date in validated_date_list:
        date_folder_path = intermediate_participant_path + sep + date
        csv_path_list = sorted(glob(os.path.join(date_folder_path, target_file_pattern)))  # file name
        if len(csv_path_list) == 0:
            print("Cannot find logs file around {}".format(date))
            # return df_logs_combined
            continue

        csv_path = csv_path_list[0]

        try:
            df_day = pd.read_csv(csv_path)
            if df_day.shape[0] > 0:
                df_day['Participant_ID'] = [participant_id] * df_day.shape[0]
                df_logs_combined = pd.concat([df_logs_combined, df_day])
        except pd.errors.EmptyDataError:
            print("pandas.errors.EmptyDataError (phone mims) : " + csv_path)
            continue

    if len(df_logs_combined) > 0:
        converter = lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f") if ("." in x) else datetime.strptime(x,
                                                                                                                "%Y-%m-%d %H:%M:%S")

        df_logs_combined = df_logs_combined.dropna(subset=['HEADER_TIME_STAMP'])
        df_logs_combined.reset_index(inplace=True, drop=True)
        df_logs_combined["HEADER_TIME_STAMP"] = [x.split(" ")[0] + " " + x.split(" ")[1] for x in
                                                 list(df_logs_combined["HEADER_TIME_STAMP"])]

        df_logs_combined['TIME_DATETIME'] = pd.Series(map(converter, df_logs_combined["HEADER_TIME_STAMP"]))
    # df_logs_combined['Date'] = df_logs_combined['TIME_DATETIME'].dt.date

    return df_logs_combined


def combine_intermediate_mims_swan_minute_file(intermediate_participant_path, date_in_study, target_file_pattern):
    df_logs_combined = pd.DataFrame()
    participant_id = utils.extract_participant_id.extract_participant_id(intermediate_participant_path)

    # generate date range where date folder exists (sharable code in utils)
    validated_date_list = validate_dates_before_after(intermediate_participant_path, date_in_study, target_file_pattern)
    if len(validated_date_list) == 0:
        print("Cannot find logs file around {}".format(date_in_study))
        return df_logs_combined

    for date in validated_date_list:
        date_folder_path = intermediate_participant_path + sep + date
        csv_path_list = sorted(glob(os.path.join(date_folder_path, target_file_pattern)))  # file name
        if len(csv_path_list) == 0:
            print("Cannot find logs file around {}".format(date))
            # return df_logs_combined
            continue

        csv_path = csv_path_list[0]

        try:
            df_day = pd.read_csv(csv_path)
            if df_day.shape[0] > 0:
                df_day['Participant_ID'] = [participant_id] * df_day.shape[0]
                df_logs_combined = pd.concat([df_logs_combined, df_day])
        except pd.errors.EmptyDataError:
            print("pandas.errors.EmptyDataError (phone mims) : " + csv_path)
            continue

    return df_logs_combined


def find_closest_time(prompt_time, subset_time_list):
    pos = bisect.bisect_left(subset_time_list, prompt_time)
    # closet_time = min(subset_time_list[max(0, i - 1): i + 2], key=lambda t: -(prompt_time - t))

    return pos


def get_mims_summary_before_prompt(sec_before, prompt_time, closest_times, df_logs_combined):
    mims_summary = 0
    num_readings = 0
    start_time = None
    for matched_idx in closest_times:
        closest_time = df_logs_combined.loc[matched_idx, "TIME_DATETIME"]
        if get_min_diff(prompt_time, closest_time) <= (sec_before // 60 + 1):
            # the matched start time should be within the minute range. This may not be true when the mims logs have gaps and return "OB".
            # Ex. time of a mims log that is 10 minutes before the prompt should be within 10 minutes range of prompt time.
            mims_min = df_logs_combined.loc[matched_idx, "MIMS_UNIT"]
            if mims_min != -0.01:  # mims value -0.01 means cannot be computed
                mims_summary += mims_min
                num_readings += 1
            start_time = closest_time
        else:
            if start_time is None:
                mims_summary = "OB"
            break
    return mims_summary, num_readings, start_time


def get_mims_summary_after_prompt(sec_after, prompt_time, closest_times, df_logs_combined):
    mims_summary = 0
    num_readings = 0
    start_time = None
    for matched_idx in closest_times:
        closest_time = df_logs_combined.loc[matched_idx, "TIME_DATETIME"]
        if get_min_diff(prompt_time, closest_time) <= (sec_after // 60 + 1):
            # the matched start time should be within the minute range. This may not be true when the mims logs have gaps and return "OB".
            # Ex. time of a mims log that is 10 minutes before the prompt should be within 10 minutes range of prompt time.
            mims_min = df_logs_combined.loc[matched_idx, "MIMS_UNIT"]
            if mims_min != -0.01:  # mims value -0.01 means cannot be computed
                mims_summary += mims_min
                num_readings += 1
            start_time = closest_time
        else:
            if start_time is None:
                mims_summary = "OB"
            break
    return mims_summary, num_readings, start_time


def get_mims_summary_after_prompt_wearstate(wear_state, sec_after, prompt_time, df_mims_swan_minute_combined,
                                            date_in_study):
    mims_summary_wearstate = 0
    mims_wearstate_min = 0
    sedentary_activity_min = 0
    light_activity_min = 0
    moderate_activity_min = 0
    vigorous_activity_min = 0
    max_idx = len(df_mims_swan_minute_combined) - 1

    window_start_idices = df_mims_swan_minute_combined[
        (df_mims_swan_minute_combined.YEAR_MONTH_DAY == date_in_study) & (
                df_mims_swan_minute_combined.HOUR == prompt_time.hour) & (
                df_mims_swan_minute_combined.MINUTE == prompt_time.minute)].index
    if len(window_start_idices) > 0:
        window_start_idx = window_start_idices[0]
        min_num = sec_after // 60
        window_end_idx = window_start_idx + min_num
        if window_end_idx > max_idx:
            window_end_idx = max_idx
        for idx in range(window_start_idx+1, window_end_idx + 1):
            swan_pred = df_mims_swan_minute_combined.loc[idx, "SWAN_PREDICTION"]
            # print(swan_pred)
            if swan_pred != wear_state:
                continue
            mims_sample_num = df_mims_swan_minute_combined.loc[idx, "MIMS_SAMPLE_NUM"]
            if mims_sample_num > 0:
                mims_value = df_mims_swan_minute_combined.loc[idx, "MIMS_SUM"]
                mims_summary_wearstate += mims_value
                mims_wearstate_min += 1

                if wear_state == "Wear":
                    if mims_value < mims_cutoff_list["sedentary"]:
                        sedentary_activity_min += 1
                    elif mims_value >= mims_cutoff_list["sedentary"] and mims_value < mims_cutoff_list["light"]:
                        light_activity_min += 1
                    elif mims_value >= mims_cutoff_list["light"] and mims_value < mims_cutoff_list["moderate"]:
                        moderate_activity_min += 1
                    elif mims_value >= mims_cutoff_list["moderate"]:
                        vigorous_activity_min += 1
                    else:
                        pass
    else:
        mims_summary_wearstate = "NF"
        mims_wearstate_min = "NF"

    return mims_summary_wearstate, mims_wearstate_min, sedentary_activity_min, light_activity_min, moderate_activity_min, vigorous_activity_min


def match_feature(prompt_local_datetime_series, df_mims_combined, df_mims_swan_minute_combined, date_in_study):
    print("     --- start matching")
    # Aggregating minutes before prompt time
    sec_before_list = [60 * x for x in list(range(1, 11))]  # 1-10 minute before prompt time
    sec_after_list = [30 * 60 * x for x in list(range(1, 7))]  # 30, 60, 90, 120, 150, 180 minute after prompt time

    mims_summary_before_list = []
    window_start_time_before_list = []
    window_readings_before_list = []

    mims_summary_after_list = []
    window_start_time_after_list = []
    window_readings_after_list = []

    mims_summary_wearstate_after_list = []
    wearstate_min_after_list = []

    sedentary_activity_wear_after_list = []
    light_activity_wear_after_list = []
    moderate_activity_wear_after_list = []
    vigorous_activity_wear_after_list = []

    for idx in prompt_local_datetime_series.index:
        # print(idx)
        matched_mims_summary_before_list = []
        matched_window_start_time_before_list = []
        matched_window_readings_before_list = []

        matched_mims_summary_after_list = []
        matched_window_start_time_after_list = []
        matched_window_readings_after_list = []

        matched_mims_summary_wearstate_after_list = []
        matched_wearstate_min_after_list = []

        prompt_time = prompt_local_datetime_series[idx]
        # prompt_date = prompt_time.date()
        matched_sedentary_activity_wear_min_after_list = []
        matched_light_activity_wear_min_after_list = []
        matched_moderate_activity_wear_min_after_list = []
        matched_vigorous_activity_wear_min_after_list = []

        if df_mims_combined.shape[0] == 0:
            matched_mims_summary_before_list = [np.nan] * len(sec_before_list)
            matched_window_readings_before_list = [np.nan] * len(sec_before_list)
            matched_window_start_time_before_list = [np.nan] * len(sec_before_list)

            matched_mims_summary_after_list = [np.nan] * len(sec_after_list)
            matched_window_readings_after_list = [np.nan] * len(sec_after_list)
            matched_window_start_time_after_list = [np.nan] * len(sec_after_list)

            matched_mims_summary_wearstate_after_list = [np.nan] * len(sec_after_list)
            matched_wearstate_min_after_list = [np.nan] * len(sec_after_list)

            matched_sedentary_activity_wear_min_after_list = [np.nan] * len(sec_after_list)
            matched_light_activity_wear_min_after_list = [np.nan] * len(sec_after_list)
            matched_moderate_activity_wear_min_after_list = [np.nan] * len(sec_after_list)
            matched_vigorous_activity_wear_min_after_list = [np.nan] * len(sec_after_list)

        else:
            subset_time_list = list(df_mims_combined["TIME_DATETIME"])
            pos = find_closest_time(prompt_time, subset_time_list)
            max_pos = len(subset_time_list) - 1

            # window before prompt
            for sec_before in sec_before_list:
                closest_times = []
                for i in range(sec_before):
                    closest_times.append(pos - 1 - i)
                closest_times = [x for x in closest_times if x >= 0]
                mims_summary, readings, start_time = get_mims_summary_before_prompt(sec_before, prompt_time,
                                                                                    closest_times,
                                                                                    df_mims_combined)
                matched_mims_summary_before_list.append(mims_summary)
                matched_window_readings_before_list.append(readings)
                matched_window_start_time_before_list.append(start_time)

            # window after prompt
            for sec_after in sec_after_list:
                # print(sec_after)
                closest_times = []
                for i in range(sec_after):
                    closest_times.append(pos + 1 + i)
                closest_times = [x for x in closest_times if x <= max_pos]

                # overall mims summary and sample num
                mims_summary, readings, start_time = get_mims_summary_after_prompt(sec_after, prompt_time,
                                                                                   closest_times,
                                                                                   df_mims_combined)

                # mims summary and sample num of sleep, wear, nonwear
                for wear_state in ["Wear", "Sleep", "Nonwear"]:
                    mims_summary_wearstate, min_wearstate, sedentary_activity_min, light_activity_min, moderate_activity_min, vigorous_activity_min = get_mims_summary_after_prompt_wearstate(
                        wear_state,
                        sec_after,
                        prompt_time,
                        df_mims_swan_minute_combined, date_in_study)

                    matched_mims_summary_wearstate_after_list.append(mims_summary_wearstate)
                    matched_wearstate_min_after_list.append(min_wearstate)
                    if wear_state == "Wear":
                        matched_sedentary_activity_wear_min_after_list.append(sedentary_activity_min)
                        matched_light_activity_wear_min_after_list.append(light_activity_min)
                        matched_moderate_activity_wear_min_after_list.append(moderate_activity_min)
                        matched_vigorous_activity_wear_min_after_list.append(vigorous_activity_min)


                matched_mims_summary_after_list.append(mims_summary)
                matched_window_readings_after_list.append(readings)
                matched_window_start_time_after_list.append(start_time)

        mims_summary_before_list.append(matched_mims_summary_before_list)
        window_readings_before_list.append(matched_window_readings_before_list)
        window_start_time_before_list.append(matched_window_start_time_before_list)

        mims_summary_after_list.append(matched_mims_summary_after_list)
        window_readings_after_list.append(matched_window_readings_after_list)
        window_start_time_after_list.append(matched_window_start_time_after_list)

        mims_summary_wearstate_after_list.append(matched_mims_summary_wearstate_after_list)
        wearstate_min_after_list.append(matched_wearstate_min_after_list)

        sedentary_activity_wear_after_list.append(matched_sedentary_activity_wear_min_after_list)
        light_activity_wear_after_list.append(matched_light_activity_wear_min_after_list)
        moderate_activity_wear_after_list.append(matched_moderate_activity_wear_min_after_list)
        vigorous_activity_wear_after_list.append(matched_vigorous_activity_wear_min_after_list)


    mims_summary_before_df = pd.DataFrame(list(map(np.ravel, mims_summary_before_list)))
    window_readings_before_df = pd.DataFrame(list(map(np.ravel, window_readings_before_list)))
    window_start_time_before_df = pd.DataFrame(list(map(np.ravel, window_start_time_before_list)))

    mims_summary_after_df = pd.DataFrame(list(map(np.ravel, mims_summary_after_list)))
    window_readings_after_df = pd.DataFrame(list(map(np.ravel, window_readings_after_list)))
    window_start_time_after_df = pd.DataFrame(list(map(np.ravel, window_start_time_after_list)))

    mims_summary_wearstate_after_df = pd.DataFrame(list(map(np.ravel, mims_summary_wearstate_after_list)))
    wearstate_min_after_df = pd.DataFrame(list(map(np.ravel, wearstate_min_after_list)))

    sedentary_activity_wear_after_df = pd.DataFrame(list(map(np.ravel, sedentary_activity_wear_after_list)))
    light_activity_wear_after_df = pd.DataFrame(list(map(np.ravel, light_activity_wear_after_list)))
    moderate_activity_wear_after_df = pd.DataFrame(list(map(np.ravel, moderate_activity_wear_after_list)))
    vigorous_activity_wear_after_df = pd.DataFrame(list(map(np.ravel, vigorous_activity_wear_after_list)))

    df = pd.DataFrame()
    for sec_before in sec_before_list:
        col = int(sec_before // 60 - 1)
        df = pd.concat([df, mims_summary_before_df[col].rename("MIMS_SUMMARY_" + str(sec_before // 60) + "MIN_BEFORE")],
                       axis=1)
        df = pd.concat(
            [df, window_readings_before_df[col].rename("WINDOW_NUM_READINGS_" + str(sec_before // 60) + "MIN_BEFORE")],
            axis=1)
        df = pd.concat(
            [df, window_start_time_before_df[col].rename("WINDOW_STARTTIME_" + str(sec_before // 60) + "MIN_BEFORE")],
            axis=1)

    for sec_after in sec_after_list:
        col = int(sec_after // (30 * 60) - 1)
        # overall mims
        df = pd.concat([df, mims_summary_after_df[col].rename("MIMS_SUMMARY_" + str(sec_after // 60) + "MIN_AFTER")],
                       axis=1)
        df = pd.concat(
            [df, window_readings_after_df[col].rename("WINDOW_NUM_READINGS_" + str(sec_after // 60) + "MIN_AFTER")],
            axis=1)
        df = pd.concat(
            [df, window_start_time_after_df[col].rename("WINDOW_STARTTIME_" + str(sec_after // 60) + "MIN_AFTER")],
            axis=1)

        # mims in wear, sleep, nonwear
        df = pd.concat(
            [df, mims_summary_wearstate_after_df[col * 3 + 0].rename(
                "MIMS_SUMMARY_WEAR_" + str(sec_after // 60) + "MIN_AFTER")],
            axis=1)
        df = pd.concat(
            [df, wearstate_min_after_df[col * 3 + 0].rename("MIMS_WEAR_MIN_" + str(sec_after // 60) + "MIN_AFTER")],
            axis=1)

        df = pd.concat(
            [df, mims_summary_wearstate_after_df[col * 3 + 1].rename(
                "MIMS_SUMMARY_SLEEP_" + str(sec_after // 60) + "MIN_AFTER")],
            axis=1)
        df = pd.concat(
            [df, wearstate_min_after_df[col * 3 + 1].rename("MIMS_SLEEP_MIN_" + str(sec_after // 60) + "MIN_AFTER")],
            axis=1)

        df = pd.concat(
            [df, mims_summary_wearstate_after_df[col * 3 + 2].rename(
                "MIMS_SUMMARY_NONWEAR_" + str(sec_after // 60) + "MIN_AFTER")],
            axis=1)
        df = pd.concat(
            [df, wearstate_min_after_df[col * 3 + 2].rename("MIMS_NONWEAR_MIN_" + str(sec_after // 60) + "MIN_AFTER")],
            axis=1)

        # activity level (sedentary/light/moderate/vigorous) during wear time
        df = pd.concat([df, sedentary_activity_wear_after_df[col].rename("SEDENTARY_MIN_WEAR_" + str(sec_after // 60) + "MIN_AFTER")],
                       axis=1)
        df = pd.concat(
            [df, light_activity_wear_after_df[col].rename("LIGHT_MIN_WEAR_" + str(sec_after // 60) + "MIN_AFTER")],
            axis=1)
        df = pd.concat(
            [df, moderate_activity_wear_after_df[col].rename("MODERATE_MIN_WEAR_" + str(sec_after // 60) + "MIN_AFTER")],
            axis=1)
        df = pd.concat(
            [df, vigorous_activity_wear_after_df[col].rename("VIGOROUS_MIN_WEAR_" + str(sec_after // 60) + "MIN_AFTER")],
            axis=1)

    return df


def create_column(prompt_local_datetime_series, intermediate_participant_path, date_in_study):
    print("\n> start generating the feature: Location ")

    # Read, parse and combine related intermediate file
    df_mims_combined = combine_intermediate_mims_file(intermediate_participant_path, date_in_study,
                                                      target_file_pattern_mims)
    df_mims_minute_combined = combine_intermediate_mims_swan_minute_file(intermediate_participant_path, date_in_study,
                                                                         target_file_pattern_mims_minute)
    df_swan_minute_combined = combine_intermediate_mims_swan_minute_file(intermediate_participant_path, date_in_study,
                                                                         target_file_pattern_swan_minute)

    if len(df_mims_combined) == 0 or len(df_mims_minute_combined) == 0 or len(df_swan_minute_combined) == 0:
        sec_before_list = [60 * x for x in list(range(1, 11))]  # 1-10 minute before prompt time
        sec_after_list = [30 * 60 * x for x in list(range(1, 7))]  # 30, 60, 90, 120, 150, 180 minute after prompt time

        column_names = []
        array_count = 0
        for sec_before in sec_before_list:
            column_names.append("MIMS_SUMMARY_" + str(sec_before // 60) + "MIN_BEFORE")
            column_names.append("WINDOW_NUM_READINGS_" + str(sec_before // 60) + "MIN_BEFORE")
            column_names.append("WINDOW_STARTTIME_" + str(sec_before // 60) + "MIN_BEFORE")
            array_count += 3

        for sec_after in sec_after_list:
            column_names.append("MIMS_SUMMARY_" + str(sec_after // 60) + "MIN_AFTER")
            column_names.append("WINDOW_NUM_READINGS_" + str(sec_after // 60) + "MIN_AFTER")
            column_names.append("WINDOW_STARTTIME_" + str(sec_after // 60) + "MIN_AFTER")

            column_names.append("MIMS_SUMMARY_WEAR_" + str(sec_after // 60) + "MIN_AFTER")
            column_names.append("MIMS_WEAR_MIN_" + str(sec_after // 60) + "MIN_AFTER")

            column_names.append("MIMS_SUMMARY_SLEEP_" + str(sec_after // 60) + "MIN_AFTER")
            column_names.append("MIMS_SLEEP_MIN_" + str(sec_after // 60) + "MIN_AFTER")

            column_names.append("MIMS_SUMMARY_NONWEAR_" + str(sec_after // 60) + "MIN_AFTER")
            column_names.append("MIMS_NONWEAR_MIN_" + str(sec_after // 60) + "MIN_AFTER")

            column_names.append("SEDENTARY_MIN_WEAR_" + str(sec_after // 60) + "MIN_AFTER")
            column_names.append("LIGHT_MIN_WEAR_" + str(sec_after // 60) + "MIN_AFTER")
            column_names.append("MODERATE_MIN_WEAR_" + str(sec_after // 60) + "MIN_AFTER")
            column_names.append("VIGOROUS_MIN_WEAR_" + str(sec_after // 60) + "MIN_AFTER")

            array_count += 13

        df = pd.DataFrame([[np.nan] * len(prompt_local_datetime_series)] * array_count).T
        df.columns = column_names
        return df

    df_mims_swan_minute_combined = pd.merge(df_mims_minute_combined, df_swan_minute_combined, how='left',
                                            left_on=['YEAR_MONTH_DAY', 'HOUR', 'MINUTE'],
                                            right_on=['YEAR_MONTH_DAY', 'HOUR', 'MINUTE'])

    # Match the combined parsed intermediate file with prompt feature data frame
    df = match_feature(prompt_local_datetime_series, df_mims_combined, df_mims_swan_minute_combined, date_in_study)

    return df


if __name__ == "__main__":
    pass
