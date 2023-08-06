"""
Functionality: Parse the content of .../logs-watch/PromptResponses.log.csv for individual participant into formatted
matrices day by day and save as csv file in the directory .../participant_id@timestudy_com/appended_response.

Usage: This script is intended mainly to be called by uema_all_features_dataframe.py.

Input: python preprocess_promptResponse_raw.py [PARTICIPANT_ID] [microT_root_path] [start_date]
e.g., python preprocess_promptResponse_raw.py aditya4_internal .../MICROT 2020-01-01

Output: csv file for each day of the participant, with each row indicating a prompted question and response
e.g., aditya4_internal_uEMA_****-**-**.csv in .../aditya4_internal@timestudy_com/appended_response
"""
import os
import sys
import numpy as np
import pandas.errors

from microt_prompt_matrix.utils.convert_timestamp import *
from glob import glob

columns_list = ["Participant_ID", "Initial_Prompt_Date", "Prompt_Type", "Study_Mode", "Initial_Prompt_Local_Time",
                "Initial_Prompt_UnixTime",
                "Initial_Prompt_UTC_Offset ",
                "Answer_Status", 'Question_Set_Completion_Local_Time', 'Question_Set_Completion_UnixTime',
                "Question_X_Answer_Unixtime"]

prompt_type_excluded = ['None_Sleep', 'None_Empty']


def extract_reprompt(df_pr_watch):
    prompt_arrays = []
    for idx in df_pr_watch.index:
        row = df_pr_watch.loc[idx]

        new_reprompt_row = []
        new_reprompt_row.append(row["Participant_ID"])
        new_reprompt_row.append(row["Initial_Prompt_Date"])
        new_reprompt_row.append(row["Prompt_Type"])
        new_reprompt_row.append(row["Study_Mode"])
        new_reprompt_row.append(row["Initial_Prompt_Local_Time"])
        new_reprompt_row.append(row["Answer_Status"])
        new_reprompt_row.append(row["Initial_Prompt_Local_Time"])
        new_reprompt_row.append(row["Question_X_Answer_Unixtime"])
        new_reprompt_row.append(row["Initial_Prompt_UTC_Offset "])
        new_reprompt_row.append(0)

        prompt_arrays.append(new_reprompt_row)

    df_prompt = pd.DataFrame(prompt_arrays)
    if df_prompt.shape[0] > 0:
        df_prompt.columns = ["Participant_ID", "Initial_Prompt_Date", "Prompt_Type", "Study_Mode",
                             "Initial_Prompt_Local_Time", "Answer_Status",
                             "Actual_Prompt_Local_Time", "First_Question_Completion_Unixtime", "UTC_Offset",
                             "Reprompt_Num"]

    return df_prompt


def clean_response_files(intermediate_participant_path, date_in_study, participant_id):
    # Check if date folder exists
    date_folder_path = os.path.join(intermediate_participant_path, date_in_study)
    # date_exist = validate_date(date_folder_path)
    # if not date_exist:
    #     print("Cannot find date folder for {}".format(date_in_study))
    #     raise Exception("Cannot find date folder for {}".format(date_in_study))

    # Check if phone_promptresponse file exists for this date
    csv_path = list(glob(os.path.join(date_folder_path, 'watch_promptresponse_clean*.csv')))
    if len(csv_path) == 0:
        print(date_folder_path)
        print("No intermediate watch prompt response csv file on {}".format(date_in_study))
        quit()

    # read and filter prompt type
    try:
        df_raw = pd.read_csv(csv_path[0])
    except pandas.errors.EmptyDataError:
        raise Exception("pandas.errors.EmptyDataError (watch prompt response) : " + csv_path[0])

    if df_raw.shape[0] == 0:
        print("Empty watch prompt response file : " + csv_path[0])
        quit()

    if "Question_X_Answer_Unixtime" not in df_raw:
        print("All watch prompts are never prompted {}".format(date_folder_path))
        quit()

    df_raw = df_raw[columns_list]

    df_raw = df_raw[~df_raw.Prompt_Type.isin(prompt_type_excluded)]
    df_raw = df_raw[df_raw['Initial_Prompt_UnixTime'] != -1]
    df_raw.reset_index(drop=True, inplace=True)

    # extract reprompts and treated them as separate prompts
    df_reprompt = extract_reprompt(df_raw)

    # add line number as prompt key. First prompt = 1.
    df_reprompt["Line"] = np.arange(1, len(df_reprompt) + 1)

    if df_reprompt.shape[0] == 0:
        print("Empty watch prompt response file after filtering : " + csv_path[0])
        quit()

    # add participant id column
    # df_reprompt.insert(loc=0, column='Participant_ID', value=participant_id)

    # time zone processing
    df_reprompt.reset_index(drop=True, inplace=True)
    Prompt_Local_Time_list = []
    for idx in df_reprompt.index:
        prompt_local_time_timezone = df_reprompt['Actual_Prompt_Local_Time'][idx]
        if type(prompt_local_time_timezone) == float:
            Prompt_Local_Time_list.append(prompt_local_time_timezone)
            print("float : {}".format(prompt_local_time_timezone))
            continue
        prompt_local_time_timezone_split = prompt_local_time_timezone.split(" ")
        prompt_local_time_timezone_split_len = len(prompt_local_time_timezone_split)
        if prompt_local_time_timezone_split_len == 3:
            Prompt_Local_Time_list.append(
                prompt_local_time_timezone_split[0] + " " + prompt_local_time_timezone_split[1])
        elif prompt_local_time_timezone_split_len == 6:
            b = [1, 2, 3, 5]
            subset_time = [prompt_local_time_timezone_split[i] for i in b]
            Prompt_Local_Time_list.append(" ".join(subset_time))
        else:
            print("Prompt response time zone error : " + intermediate_participant_path + "//" + date_in_study)
            raise Exception("Unable to parse Actual_Prompt_Local_Time")

    prompt_local_time_timezone = df_reprompt['Actual_Prompt_Local_Time'][0]
    prompt_local_time_timezone_split = prompt_local_time_timezone.split(" ")
    prompt_local_time_timezone_split_len = len(prompt_local_time_timezone_split)
    if prompt_local_time_timezone_split_len == 3:
        converter = lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S") if (type(x) != float) else np.nan
        prompt_dateobject_column = list(map(converter, Prompt_Local_Time_list))
    elif prompt_local_time_timezone_split_len == 6:
        converter = lambda x: datetime.strptime(x, "%b %d %H:%M:%S %Y") if (type(x) != float) else np.nan
        prompt_dateobject_column = list(map(converter, Prompt_Local_Time_list))
    else:
        raise Exception("Unable to parse Actual_Prompt_Local_Time")

    # drop float type in Actual_Prompt_Local_Time
    df_reprompt['Actual_Prompt_Local_DateTime'] = prompt_dateobject_column
    df_reprompt = df_reprompt[df_reprompt['Actual_Prompt_Local_DateTime'].notnull()]
    df_reprompt.reset_index(inplace=True, drop=True)

    return df_reprompt


if __name__ == "__main__":
    p_id = sys.argv[1]
    intermediate_root_path = sys.argv[2]
    feature_save_path = sys.argv[3]
    start_date = sys.argv[4]
    end_date = sys.argv[5]
    clean_response_files(p_id, intermediate_root_path, feature_save_path, start_date, end_date)
