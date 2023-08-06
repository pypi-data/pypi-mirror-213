def get_min_diff(prompt_datetime, matched_datetime):
    min_diff = abs((prompt_datetime - matched_datetime).total_seconds() / 60.0)
    return min_diff