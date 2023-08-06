"""
Functionality: This is the main script to generate a matrix of features of interest.

Arguments:
1) intermediate_participant_path
e.g., G:\...\intermediate_file\sharpnessnextpouch@timestudy_com

2) output_dir_path
e.g., C:\...\output_folder

3) date_in_study
e.g., 2021-01-01

4) decryption_password
eg., passwordpassword

Command line example:
python main.py [intermediate_participant_path] [output_dir_path] [date_in_study] [decryption_password]

Output: feature_mx_<date>.csv file that contains all features in the <output_dir_path> folder .
"""
import sys
import time
import os
import pandas as pd
from microt_prompt_matrix import utils
from microt_prompt_matrix import feature_engineering_uema


def compute_features_watch(intermediate_participant_path, output_dir_path, date_in_study, lsf_json_folder_path,
                           decryption_password):
    # Switch
    print_stats = False

    # Extract participant id from participant folder path
    participant_id = utils.extract_participant_id.extract_participant_id(intermediate_participant_path)

    # check if skip
    csv_file_name = "uema_feature_mx_{}".format(date_in_study) + ".csv"
    csv_save_path = os.path.join(output_dir_path, participant_id, csv_file_name)
    if os.path.exists(csv_save_path):
        print("Output exists. Skip uEMA for {}-{}".format(participant_id, date_in_study))
        return

    # Create output folder
    output_participant_path = os.path.join(output_dir_path, participant_id)
    if not os.path.exists(output_participant_path):
        try:
            os.makedirs(output_participant_path)
        except FileExistsError:
            pass

    # Parse prompt response file for the specific date
    df_prompt = feature_engineering_uema.prompt_response.preprocess_promptResponse_raw.clean_response_files(
        intermediate_participant_path, date_in_study, participant_id)

    # - Outcome variable: completion status
    completion_status_binary = feature_engineering_uema.compliance.create_column(df_prompt['Answer_Status'],
                                                                                print_stats)
    # - Feature matrix
    feature_df = df_prompt
    feature_df['Answer_Status'] = completion_status_binary

    # - Loading Participants Information
    info_dict = utils.load_participant_study_info.execute(intermediate_participant_path, output_dir_path, lsf_json_folder_path)

    # - feature 1: Day of the week
    feature1 = feature_engineering_uema.day_of_the_week.create_column(df_prompt['Actual_Prompt_Local_DateTime'], print_stats)
    feature_df['DAY_OF_THE_WEEK'] = feature1
    # - feature 2: Time of the day
    feature2 = feature_engineering_uema.time_of_the_day.create_column(df_prompt['Actual_Prompt_Local_DateTime'], print_stats)
    feature_df['TIME_OF_THE_DAY'] = feature2
    # - feature 3: Days in the study
    feature3 = feature_engineering_uema.days_in_study.create_column(df_prompt, info_dict, print_stats)
    feature_df['DAYS_IN_THE_STUDY'] = feature3

    # - feature 4: battery level
    feature5, feature6, match_time_battery = feature_engineering_uema.battery_level.create_column(
        df_prompt['Actual_Prompt_Local_DateTime'], intermediate_participant_path, date_in_study)
    feature_df['BATTERY_LEVEL'] = feature5
    feature_df['CHARGING_STATUS'] = feature6
    feature_df['match_time_battery'] = match_time_battery

    # - feature 5: GPS location
    feature7, match_time_location, feature7_1 = feature_engineering_uema.location.create_column(participant_id, df_prompt['Actual_Prompt_Local_DateTime'], info_dict,
                                                                                   intermediate_participant_path,
                                                                                   date_in_study, decryption_password)
    feature_df['LOCATION'] = feature7
    feature_df['match_time_location'] = match_time_location
    feature_df['DISTANCE_FROM_HOME'] = feature7_1

    # - feature 6: Location label
    feature8 = feature_engineering_uema.location_label.create_column(lsf_json_folder_path, participant_id, feature7)
    feature_df['LOCATION_LABEL'] = feature8

    # - feature 7: Screen Status
    feature9, match_time_screen = feature_engineering_uema.screen_status.create_column(
        df_prompt['Actual_Prompt_Local_DateTime'], intermediate_participant_path, date_in_study)
    feature_df['SCREEN_STATUS'] = feature9
    feature_df['match_time_screen'] = match_time_screen

    # - feature 10&11: wake and sleep hour
    feature10, feature11 = feature_engineering_uema.waking_hours.create_column(df_prompt['Actual_Prompt_Local_DateTime'],
                                                                              intermediate_participant_path,
                                                                              date_in_study)
    feature_df['WAKE_TIME'] = feature10
    feature_df['SLEEP_TIME'] = feature11

    # - feature 12: Phone lock status
    feature12, feature13, match_time_lock = feature_engineering_uema.phone_lock.create_column(
        df_prompt['Actual_Prompt_Local_DateTime'], intermediate_participant_path, date_in_study)
    feature_df['PHONE_LOCK'] = feature12
    feature_df['LAST_USAGE_DURATION'] = feature13
    feature_df['match_time_lock'] = match_time_lock

    # - feature 13: parts of waking hour
    parts_num = 4
    feature14, feature15, feature16 = feature_engineering_uema.parts_of_waking_hour.create_column(feature_df, parts_num)
    feature_df['PARTS_OF_WAKING_HOUR'] = feature14
    feature_df['PROXIMITY_TO_WAKE_TIME'] = feature15
    feature_df['PROXIMITY_TO_SLEEP_TIME'] = feature16

    # - feature 14: MIMS Summary
    df_mims = feature_engineering_uema.mims_summary.create_column(df_prompt['Actual_Prompt_Local_DateTime'],
                                                                 intermediate_participant_path, date_in_study)
    feature_df = pd.concat([feature_df, df_mims], axis=1)


    # save
    feature_df.to_csv(csv_save_path, index=False)

    return


if __name__ == "__main__":
    start = time.time()
    intermediate_participant_path = sys.argv[1]
    output_dir_path = sys.argv[2]
    date_in_study = sys.argv[3]
    lsf_json_folder_path = sys.argv[4]
    decryption_password = sys.argv[5]

    compute_features_watch(intermediate_participant_path, output_dir_path, date_in_study, lsf_json_folder_path,
                           decryption_password)
    end = time.time()
    print("Finished\n")
    print("Runtime : {} seconds".format(round(end - start, 2)))