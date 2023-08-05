import numpy as np

def estimate_sampling_frequency(timestamps):
    time_diff = np.diff(timestamps)  # Calculate the time difference between consecutive samples
    sampling_freq = 1 / np.nanmean(time_diff) 
    return sampling_freq

def remove_null_columns(df):
    # Remove columns with all null values
    df_cleaned = df.dropna(axis=1, how='all')
    return df_cleaned

def merge_data(adarsh_pre_cog, adarsh_post_cog):
    min_len = min(len(adarsh_pre_cog), len(adarsh_post_cog))
    pre_merged_df = adarsh_pre_cog[:min_len]
    post_merged_df = adarsh_post_cog[:min_len]
    print(min_len)
    return pre_merged_df,post_merged_df
