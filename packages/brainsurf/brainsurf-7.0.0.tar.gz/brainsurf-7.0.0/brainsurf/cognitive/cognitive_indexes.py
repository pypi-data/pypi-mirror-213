import numpy as np

def calculate_band_power(freqs, power, bands):
    """
    Calculate band power from frequency power spectrum.

    Args:
        freqs (array-like): Array of frequencies.
        power (array-like): Array of power values corresponding to the frequencies.
        bands (dict): Dictionary containing frequency bands as keys and their corresponding frequency ranges as values.

    Returns:
        dict: Dictionary containing band power values for each frequency band.
    """
    band_power = {}
    for band, f_range in bands.items():
        idx = np.logical_and(freqs >= f_range[0], freqs <= f_range[1])
        band_power[band] = np.trapz(power[idx], freqs[idx])

    return band_power


def calculate_pe(alpha_power, beta_power):
    """
    Calculate the Peak-to-Excursion ratio (PE) as a measure of neural activity.

    Args:
        alpha_power (float): Power in the alpha frequency band.
        beta_power (float): Power in the beta frequency band.

    Returns:
        float: Peak-to-Excursion ratio (PE).
    """
    pe = beta_power / alpha_power
    return pe


def calculate_arousal_index(alpha_power, theta_power):
    """
    Calculate the Arousal Index (AI) as a measure of arousal level.

    Args:
        alpha_power (float): Power in the alpha frequency band.
        theta_power (float): Power in the theta frequency band.

    Returns:
        float: Arousal Index (AI).
    """
    ai = alpha_power / theta_power
    return ai


def calculate_neural_activity(delta_power, theta_power, alpha_power, beta_power):
    """
    Calculate the Neural Activity (NA) as a measure of overall neural activity.

    Args:
        delta_power (float): Power in the delta frequency band.
        theta_power (float): Power in the theta frequency band.
        alpha_power (float): Power in the alpha frequency band.
        beta_power (float): Power in the beta frequency band.

    Returns:
        float: Neural Activity (NA).
    """
    na = (delta_power + theta_power) / (alpha_power + beta_power)
    return na


def calculate_engagement(alpha_power, theta_power, delta_power):
    """
    Calculate the Engagement Index (ENG) as a measure of cognitive engagement.

    Args:
        alpha_power (float): Power in the alpha frequency band.
        theta_power (float): Power in the theta frequency band.
        delta_power (float): Power in the delta frequency band.

    Returns:
        float: Engagement Index (ENG).
    """
    eng = (alpha_power + theta_power) / delta_power
    return eng


def calculate_load_index(alpha_power, beta_power):
    """
    Calculate the Load Index (LI) as a measure of cognitive load.

    Args:
        alpha_power (float): Power in the alpha frequency band.
        beta_power (float): Power in the beta frequency band.

    Returns:
        float: Load Index (LI).
    """
    li = alpha_power / beta_power
    return li


def calculate_alertness(alpha_power, theta_power):
    """
    Calculate the Alertness Index (AL) as a measure of alertness level.

    Args:
        alpha_power (float): Power in the alpha frequency band.
        theta_power (float): Power in the theta frequency band.

    Returns:
        float: Alertness Index (AL).
    """
    al = alpha_power / (alpha_power + theta_power)
    return al


def calculate_load_index(alpha_power, beta_power):
    """
    Calculate the Load Index (LI) as a measure of cognitive load.

    Args:
        alpha_power (float): Power in the alpha frequency band.
        beta_power (float): Power in the beta frequency band.

    Returns:
        float: Load Index (LI).
    """
    li = alpha_power / beta_power
    return li


def calculate_alertness(alpha_power, theta_power):
    """
    Calculate the Alertness Index (AL) as a measure of alertness level.

    Args:
        alpha_power (float): Power in the alpha frequency band.
        theta_power (float): Power in the theta frequency band.

    Returns:
        float: Alertness Index (AL).
    """
    al = alpha_power / (alpha_power + theta_power)
    return al
