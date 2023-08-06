import pandas as pd
import json
from microt_prompt_matrix.utils.uncompress_file import *


def check_inside_bbox(location, bbox):
    isInside = False

    lat = location[0]
    lon = location[1]

    bbox[0] = bbox[0]
    bbox[1] = bbox[1]
    bbox[2] = bbox[2]
    bbox[3] = bbox[3]

    if (lat >= bbox[0]) & (lat <= bbox[1]) & (lon >= bbox[2]) & (lon <= bbox[3]):
        isInside = True

    return isInside


def read_json(json_path):
    with open(json_path) as f:
        data = json.load(f)
    return data


def transform(location_column):
    return location_column


def find_cluster_for_loc(loc, lsf_json):
    matched_clusters = []
    for clusterID in lsf_json['bbox']:
        isInside = check_inside_bbox(loc, lsf_json['bbox'][clusterID])
        if isInside:
            matched_clusters.append(clusterID)
    return matched_clusters


def find_label_for_cluster(matched_clusters, lsf_json):
    labels = lsf_json["label"]
    matched_loc_label = []
    for clusterID in matched_clusters:
        if clusterID not in labels:
            continue
        if len(labels[clusterID]) == 0:
            continue
        b_s = pd.Series(labels[clusterID])
        if len(b_s) > 0:
            b = b_s.value_counts().index[0]  # take the mode label
            matched_loc_label.append(b)
    return matched_loc_label


def create_column(lsf_json_folder_path, participant_id, location_list):
    print("\n> start generating the feature: Location Label")

    # Loading lsf json
    lsf_json_path = os.path.join(lsf_json_folder_path, participant_id, "lsf.json")
    if not os.path.exists(lsf_json_path):
        print("     --- failure : no json file found for {}".format(participant_id))
        return ["NF"] * len(location_list)
    else:
        lsf_json = read_json(lsf_json_path)

    if ("bbox" not in lsf_json) or ("label" not in lsf_json):
        print("     --- failure : incomplete json file found for {}".format(participant_id))
        return ["NF"] * len(location_list)

    # map loc to cluster
    location_label_column = []
    for loc in location_list:
        loc_label = "NF"
        if loc not in ["NF", "OB"]:
            matched_clusters = find_cluster_for_loc(loc, lsf_json)
            loc_label = find_label_for_cluster(matched_clusters, lsf_json)
            loc_label = list(set(loc_label))
        location_label_column.append(loc_label)

    # transform feature
    location_column_transformed = transform(location_label_column)
    print("     --- success")

    return location_column_transformed


if __name__ == "__main__":
    location_list = [[47.60958, -122.33052]]
    lsf_json_folder_path = r"C:\Users\Jixin\Documents\testing\compliance"
    participant_id = "cat"
    print(create_column(lsf_json_folder_path, participant_id, location_list))