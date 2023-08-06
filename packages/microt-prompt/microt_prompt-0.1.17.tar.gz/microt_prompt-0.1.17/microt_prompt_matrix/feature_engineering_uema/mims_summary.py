import os
from os import sep
from glob import glob
import pandas as pd
import numpy as np
import bisect
from datetime import datetime, timedelta
from microt_prompt_matrix import utils
from microt_prompt_matrix.utils.get_time_diff import *

target_file_pattern = 'watch_accelerometer_mims*.csv'


def combine_intermediate_file(intermediate_participant_path, date_in_study):
    df_logs_combined = pd.DataFrame()
    participant_id = utils.extract_participant_id.extract_participant_id(intermediate_participant_path)

    # generate date range where date folder exists (sharable code in utils)
    # validated_date_list = validate_dates_before_after(intermediate_participant_path, date_in_study)
    # if len(validated_date_list) == 0:
    #     print("Cannot find logs file around {}".format(date_in_study))
    #     return df_logs_combined

    for date in [date_in_study]:
        date_folder_path = intermediate_participant_path + sep + date
        csv_path_list = sorted(glob(os.path.join(date_folder_path, target_file_pattern)))  # file name
        if len(csv_path_list) == 0:
            print("Cannot find logs file around {}".format(date_in_study))
            return df_logs_combined

        csv_path = csv_path_list[0]

        try:
            df_day = pd.read_csv(csv_path)
            if df_day.shape[0] > 0:
                df_day['Participant_ID'] = [participant_id] * df_day.shape[0]
                df_logs_combined = pd.concat([df_logs_combined, df_day])
        except pd.errors.EmptyDataError:
            print("pandas.errors.EmptyDataError (phone mims) : " + csv_path)
            return df_logs_combined

    converter = lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f") if ("." in x) else datetime.strptime(x,
                                                                                                            "%Y-%m-%d %H:%M:%S")

    df_logs_combined = df_logs_combined.dropna(subset=['HEADER_TIME_STAMP'])
    df_logs_combined.reset_index(inplace=True, drop=True)
    df_logs_combined["HEADER_TIME_STAMP"] = [x.split(" ")[0] + " " + x.split(" ")[1] for x in
                                             list(df_logs_combined["HEADER_TIME_STAMP"])]

    df_logs_combined['TIME_DATETIME'] = pd.Series(map(converter, df_logs_combined["HEADER_TIME_STAMP"]))
    # df_logs_combined['Date'] = df_logs_combined['TIME_DATETIME'].dt.date

    return df_logs_combined


def find_closest_time(prompt_time, subset_time_list):
    pos = bisect.bisect_left(subset_time_list, prompt_time)
    # closet_time = min(subset_time_list[max(0, i - 1): i + 2], key=lambda t: -(prompt_time - t))

    return pos


def get_mims_summary(sec_before, prompt_time, closest_times, df_logs_combined):
    mims_summary = 0
    num_readings = 0
    start_time = None
    for matched_idx in closest_times:
        closest_time = df_logs_combined.loc[matched_idx, "TIME_DATETIME"]
        if get_min_diff(prompt_time, closest_time) <= (sec_before // 60 + 1):
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


def match_feature(prompt_local_datetime_series, df_logs_combined):
    print("     --- start matching")
    # Aggregating minutes before prompt time
    sec_before_list = [60 * x for x in list(range(1, 11))]

    mims_summary_list = []
    start_time_list = []
    readings_list = []

    for idx in prompt_local_datetime_series.index:
        matched_mims_summary_list = []
        matched_start_time_list = []
        matched_readings_list = []

        prompt_time = prompt_local_datetime_series[idx]
        # prompt_date = prompt_time.date()

        if df_logs_combined.shape[0] == 0:
            matched_mims_summary_list = [np.nan] * len(sec_before_list)
            matched_readings_list = [np.nan] * len(sec_before_list)
            matched_start_time_list = [np.nan] * len(sec_before_list)
        else:
            subset_time_list = list(df_logs_combined["TIME_DATETIME"])
            pos = find_closest_time(prompt_time, subset_time_list)

            for sec_before in sec_before_list:
                closest_times = []
                for i in range(sec_before):
                    closest_times.append(pos - 1 - i)
                closest_times = [x for x in closest_times if x >= 0]
                mims_summary, readings, start_time = get_mims_summary(sec_before, prompt_time, closest_times,
                                                                      df_logs_combined)
                matched_mims_summary_list.append(mims_summary)
                matched_readings_list.append(readings)
                matched_start_time_list.append(start_time)
        mims_summary_list.append(matched_mims_summary_list)
        readings_list.append(matched_readings_list)
        start_time_list.append(matched_start_time_list)

    mims_summary_df = pd.DataFrame(list(map(np.ravel, mims_summary_list)))
    readings_df = pd.DataFrame(list(map(np.ravel, readings_list)))
    start_time_df = pd.DataFrame(list(map(np.ravel, start_time_list)))

    df = pd.DataFrame()
    for sec_before in sec_before_list:
        col = int(sec_before // 60 - 1)
        df = pd.concat([df, mims_summary_df[col].rename("mims_summary_" + str(sec_before // 60) + "min")], axis=1)
        df = pd.concat([df, readings_df[col].rename("num_readings_" + str(sec_before // 60) + "min")], axis=1)
        df = pd.concat([df, start_time_df[col].rename("start_time_" + str(sec_before // 60) + "min")], axis=1)

    return df


def create_column(prompt_local_datetime_series, intermediate_participant_path, date_in_study):
    print("\n> start generating the feature: MIMS ")

    # Read, parse and combine related intermediate file
    df_logs_combined = combine_intermediate_file(intermediate_participant_path, date_in_study)

    # Match the combined parsed intermediate file with prompt feature data frame
    df = match_feature(prompt_local_datetime_series, df_logs_combined)

    return df


if __name__ == "__main__":
    pass
