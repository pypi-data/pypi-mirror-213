import numpy as np
from scipy.stats import ttest_rel, wilcoxon
import pandas as pd
from scipy import stats
from brainsurf.cognitive.cognitive_indexes import calculate_arousal_index, calculate_band_power, calculate_engagement, calculate_neural_activity, calculate_pe
import pandas as pd
import scipy.stats as stats

import numpy as np

# def calculate_cognitive_indexes(data_before, data_after):
#     """
#     Calculate cognitive indexes from EEG data to assess attention, mental workload, or cognitive performance.
#     Examples of cognitive indexes include response time, error rates, or other relevant measures.

#     Args:
#     - data_before (pandas.DataFrame or dict): EEG data before meditation.
#     - data_after (pandas.DataFrame or dict): EEG data after meditation.

#     Returns:
#     - cognitive_indexes_before (numpy.ndarray): Cognitive indexes calculated from data_before.
#     - cognitive_indexes_after (numpy.ndarray): Cognitive indexes calculated from data_after.
#     """

#     # Convert data_before and data_after to pandas DataFrames if they are dictionaries
#     if isinstance(data_before, dict):
#         data_before = pd.DataFrame(data_before)
#     if isinstance(data_after, dict):
#         data_after = pd.DataFrame(data_after)

#     # Extract the necessary data columns from data_before
#     alpha_power_before = data_before[0]['alpha']
#     beta_power_before = data_before[0]['beta']
#     delta_power_before = data_before[0]['delta']
#     theta_power_before = data_before[0]['theta']

#     # Define the frequency bands for calculation
#     bands = {
#         'delta': (0.5, 4),
#         'theta': (4, 8),
#         'alpha': (8, 13),
#         'beta': (13, 30)
#     }
#     print(alpha_power_before, beta_power_before)
#     # Calculate cognitive indexes before meditation
#     pe_before = calculate_pe(alpha_power_before, beta_power_before)
#     ai_before = calculate_arousal_index(alpha_power_before, theta_power_before)
#     na_before = calculate_neural_activity(
#         delta_power_before, theta_power_before, alpha_power_before, beta_power_before
#     )
#     eng_before = calculate_engagement(alpha_power_before, theta_power_before, delta_power_before)

#     # Extract the necessary data columns from data_after
#     alpha_power_after = data_after[0]['alpha']
#     beta_power_after = data_after[0]['beta']
#     delta_power_after = data_after[0]['delta']
#     theta_power_after = data_after[0]['theta']
    
#     # Calculate cognitive indexes after meditation
#     pe_after = calculate_pe(alpha_power_after, beta_power_after)
#     ai_after = calculate_arousal_index(alpha_power_after, theta_power_after)
#     na_after = calculate_neural_activity(
#         delta_power_after, theta_power_after, alpha_power_after, beta_power_after
#     )
#     eng_after = calculate_engagement(alpha_power_after, theta_power_after, delta_power_after)

#     # Compare the cognitive indexes before and after meditation using paired t-test
#     cognitive_indexes_before = np.array([pe_before, ai_before, na_before, eng_before])
#     cognitive_indexes_after = np.array([pe_after, ai_after, na_after, eng_after])

#     # Perform the paired t-test
#     return cognitive_indexes_before, cognitive_indexes_after

def calculate_cognitive_indexes(data_before, data_after):
    """
    Calculate cognitive indexes from EEG data to assess attention, mental workload, or cognitive performance.
    Examples of cognitive indexes include response time, error rates, or other relevant measures.

    Args:
    - data_before (pandas.DataFrame): EEG data before meditation.
    - data_after (pandas.DataFrame): EEG data after meditation.

    Returns:
    - cognitive_indexes_before (numpy.ndarray): Cognitive indexes calculated from data_before.
    - cognitive_indexes_after (numpy.ndarray): Cognitive indexes calculated from data_after.
    """

    # Extract the necessary data columns from data_before
    freqs_before = data_before['sec']
    alpha_power_before = data_before['alpha']
    beta_power_before = data_before['beta']
    delta_power_before = data_before['delta']
    theta_power_before = data_before['theta']

    # Define the frequency bands for calculation
    bands = {
        'delta': (0.5, 4),
        'theta': (4, 8),
        'alpha': (8, 13),
        'beta': (13, 30)
    }

    # Calculate cognitive indexes before meditation
    pe_before = calculate_pe(alpha_power_before, beta_power_before)
    ai_before = calculate_arousal_index(alpha_power_before, theta_power_before)
    na_before = calculate_neural_activity(
        delta_power_before, theta_power_before, alpha_power_before, beta_power_before
    )
    eng_before = calculate_engagement(alpha_power_before, theta_power_before, delta_power_before)
    # Extract the necessary data columns from data_after
    freqs_after = data_after['sec']
    alpha_power_after = data_after['alpha']
    beta_power_after = data_after['beta']
    delta_power_after = data_after['delta']
    theta_power_after = data_after['theta']

    # Calculate band power for each frequency band after meditation
    band_power_after = calculate_band_power(freqs_after, alpha_power_after, bands)

    # Calculate cognitive indexes after meditation
    pe_after = calculate_pe(alpha_power_after,beta_power_after)
    ai_after = calculate_arousal_index(alpha_power_after,theta_power_after)
    na_after = calculate_neural_activity(
        delta_power_after, theta_power_after, alpha_power_after, beta_power_after
    )
    eng_after = calculate_engagement(alpha_power_after, theta_power_after, delta_power_after)

    # Compare the cognitive indexes before and after meditation using paired t-test
    cognitive_indexes_before = np.array([pe_before, ai_before, na_before, eng_before])
    cognitive_indexes_after = np.array([pe_after, ai_after, na_after, eng_after])
  
    # Perform the paired t-test
    return cognitive_indexes_before, cognitive_indexes_after



def compare_cognitive_indexes(cognitive_indexes_before, cognitive_indexes_after, test_type="paired_ttest"):
    """
    Compare cognitive indexes before and after meditation using appropriate statistical tests.

    Args:
    - cognitive_indexes_before (numpy.ndarray): Cognitive indexes before meditation.
    - cognitive_indexes_after (numpy.ndarray): Cognitive indexes after meditation.
    - test_type (str): Type of statistical test to perform. Options: "paired_ttest", "wilcoxon".

    Returns:
    - test_statistic (float): Test statistic value.
    - p_value (float): P-value indicating the statistical significance.
    """

    if test_type == "paired_ttest":
        # Perform paired t-test
        test_statistic, p_value = ttest_rel(cognitive_indexes_before, cognitive_indexes_after)
    elif test_type == "wilcoxon":
        # Perform Wilcoxon signed-rank test
        test_statistic, p_value = wilcoxon(cognitive_indexes_before, cognitive_indexes_after)
    else:
        raise ValueError("Invalid test_type. Options: 'paired_ttest', 'wilcoxon'")

    return test_statistic, p_value



# def compare_eeg_data_stats(pre_merged, post_merged):
#     # Extract the relevant feature columns
#     pre_eeg_raw = pre_merged['raw']
#     pre_alpha = pre_merged['alpha']
#     pre_beta = pre_merged['beta']
#     pre_theta = pre_merged['theta']
#     pre_delta = pre_merged['delta']

#     post_eeg_raw = post_merged['raw']
#     post_alpha = post_merged['alpha']
#     post_beta = post_merged['beta']
#     post_theta = post_merged['theta']
#     post_delta = post_merged['delta'] 
#     # Perform t-tests for each feature
#     t_statistic_raw, p_value_raw = stats.ttest_ind(pre_eeg_raw, post_eeg_raw)
#     t_statistic_alpha, p_value_alpha = stats.ttest_ind(pre_alpha, post_alpha)
#     t_statistic_beta, p_value_beta = stats.ttest_ind(pre_beta, post_beta)
#     t_statistic_theta, p_value_theta = stats.ttest_ind(pre_theta, post_theta)
#     t_statistic_delta, p_value_delta = stats.ttest_ind(pre_delta, post_delta)
#     # Perform ANOVA for each feature
#     f_statistic_raw, p_value_anova_raw = stats.f_oneway(pre_eeg_raw, post_eeg_raw)
#     f_statistic_alpha, p_value_anova_alpha = stats.f_oneway(pre_alpha, post_alpha)
#     f_statistic_beta, p_value_anova_beta = stats.f_oneway(pre_beta, post_beta)
#     f_statistic_theta, p_value_anova_theta = stats.f_oneway(pre_theta, post_theta)
#     f_statistic_delta, p_value_anova_delta = stats.f_oneway(pre_delta, post_delta)

#     # Calculate effect sizes (Cohen's d) for each feature
#     effect_size_raw = abs(pre_eeg_raw.mean() - post_eeg_raw.mean()) / pre_eeg_raw.std()
#     effect_size_alpha = abs(pre_alpha.mean() - post_alpha.mean()) / pre_alpha.std()
#     effect_size_beta = abs(pre_beta.mean() - post_beta.mean()) / pre_beta.std()
#     effect_size_theta = abs(pre_theta.mean() - post_theta.mean()) / pre_theta.std()
#     effect_size_delta = abs(pre_delta.mean() - post_delta.mean()) / pre_delta.std()

#     # Create a DataFrame to store the results
#     results = pd.DataFrame({
#         'Feature': ['EEG', 'Alpha', 'Beta', 'Theta', 'Delta'],
#         'T-Stat': [t_statistic_raw, t_statistic_alpha, t_statistic_beta, t_statistic_theta, t_statistic_delta],
#         'P-Value (T-Test)': [p_value_raw, p_value_alpha, p_value_beta, p_value_theta, p_value_delta],
#         'F-Stat': [f_statistic_raw, f_statistic_alpha, f_statistic_beta, f_statistic_theta, f_statistic_delta],
#         'P-Value (ANOVA)': [p_value_anova_raw, p_value_anova_alpha, p_value_anova_beta, p_value_anova_theta, p_value_anova_delta],
#         'Effect Size': [effect_size_raw, effect_size_alpha, effect_size_beta, effect_size_theta, effect_size_delta]
#     })
#     return results

import pandas as pd
from scipy import stats
import pandas as pd
from scipy import stats


def compare_eeg_data_stats(pre_merged, post_merged, feature_columns):
    results = pd.DataFrame(columns=['Feature', 'T-Stat', 'P-Value (T-Test)', 'F-Stat', 'P-Value (ANOVA)', 'Effect Size'])
    
    for feature in feature_columns:
        pre_data = pre_merged[feature]
        post_data = post_merged[feature]
        
        t_statistic, p_value_ttest = stats.ttest_ind(pre_data, post_data)
        f_statistic, p_value_anova = stats.f_oneway(pre_data, post_data)
        
        effect_size = abs(pre_data.mean() - post_data.mean()) / pre_data.std()
        
        result = pd.DataFrame({
            'Feature': [feature],
            'T-Stat': [t_statistic],
            'P-Value (T-Test)': [p_value_ttest],
            'F-Stat': [f_statistic],
            'P-Value (ANOVA)': [p_value_anova],
            'Effect Size': [effect_size]
        })
        
        results = pd.concat([results, result], ignore_index=True)
    
    return results




def perform_ttest(data_before, data_after):
    t_stat, p_value = stats.ttest_rel(data_before, data_after)
    return t_stat, p_value

def calculate_ttest_results(df):
    variables = ['Arousal Index', 'Neural Activity', 'Performance Index', 'Engagement']
    columns = ['t-statistic', 'p-value']
    results = []

    for variable in variables:
        data_before = df[f'{variable} Before']
        data_after = df[f'{variable} After']
        t_stat, p_value = perform_ttest(data_before, data_after)
        results.append([t_stat, p_value])

    ttest_results_df = pd.DataFrame(results, index=variables, columns=columns)
    return ttest_results_df

# # Example usage:
# ttest_results_df = calculate_ttest_results(df)


def analyze_stroop_data(data):
    # Convert the data to a pandas DataFrame for easier analysis
    df = pd.DataFrame(data, columns=["Color 1", "Color 2", "Congruent", "Response Time", "Accuracy", "Block", "Trial"])

    # Calculate average response time for congruent and incongruent trials
    congruent_rt = df[df["Congruent"] == 1]["Response Time"]
    incongruent_rt = df[df["Congruent"] == 0]["Response Time"]

    avg_congruent_rt = np.mean(congruent_rt)
    avg_incongruent_rt = np.mean(incongruent_rt)

    # Perform t-test for response times (without using scipy)
    t_value, p_value = independent_ttest(congruent_rt, incongruent_rt)

    # Calculate average accuracy for congruent and incongruent trials
    congruent_acc = df[df["Congruent"] == 1]["Accuracy"]
    incongruent_acc = df[df["Congruent"] == 0]["Accuracy"]

    avg_congruent_acc = np.mean(congruent_acc)
    avg_incongruent_acc = np.mean(incongruent_acc)

    # Perform t-test for accuracy (without using scipy)
    t_value_acc, p_value_acc = independent_ttest(congruent_acc, incongruent_acc)

    # Store the results in a dictionary
    results = {
        "Average Response Time - Congruent": avg_congruent_rt,
        "Average Response Time - Incongruent": avg_incongruent_rt,
        "T-Test - Response Time - t-value": t_value,
        "T-Test - Response Time - p-value": p_value,
        "Average Accuracy - Congruent": avg_congruent_acc,
        "Average Accuracy - Incongruent": avg_incongruent_acc,
        "T-Test - Accuracy - t-value": t_value_acc,
        "T-Test - Accuracy - p-value": p_value_acc
    }

    return results


def independent_ttest(x, y):
    # Calculate the t-value and p-value for two independent samples
    mean_diff = np.mean(x) - np.mean(y)
    var_x = np.var(x, ddof=1)
    var_y = np.var(y, ddof=1)
    n_x = len(x)
    n_y = len(y)

    pooled_var = ((n_x - 1) * var_x + (n_y - 1) * var_y) / (n_x + n_y - 2)
    se_diff = np.sqrt(pooled_var * (1 / n_x + 1 / n_y))
    t_value = mean_diff / se_diff

    df = n_x + n_y - 2
    p_value = 2 * (1 - t_cdf(abs(t_value), df))

    return t_value, p_value

def t_cdf(t, df):
    # Calculate the cumulative distribution function (CDF) of the t-distribution
    x = np.arange(0, t + 0.01, 0.01)
    pdf_vals = (1 / np.sqrt(df * np.pi)) * np.power(1 + np.square(x) / df, -((df + 1) / 2))
    cdf_vals = np.cumsum(pdf_vals) * 0.01

    return cdf_vals[-1]