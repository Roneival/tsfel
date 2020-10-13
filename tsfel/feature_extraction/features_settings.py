import json
import tsfel
import numpy as np


def load_json(json_path):
    """Loads the json file given by filename.

    Parameters
    ----------
    json_path : string
        Json path

    Returns
    -------
    Dict
        Dictionary

    """

    return json.load(open(json_path))


def get_features_by_domain(domain=None, json_path=None):
    """Creates a dictionary with the features settings by domain.

    Parameters
    ----------
    domain : string
        Available domains: "statistical"; "spectral"; "temporal"
        If domain equals None, then the features settings from all domains are returned.
    json_path : string
        Directory of json file. Default: package features.json directory

    Returns
    -------
    Dict
        Dictionary with the features settings

    """

    if json_path is None:
        json_path = tsfel.__path__[0]+"/feature_extraction/features.json"

        if domain not in ['statistical', 'temporal', 'spectral', None]:
            raise SystemExit(
                'No valid domain. Choose: statistical, temporal, spectral or None (for all feature settings).')

    dict_features = load_json(json_path)
    if domain is None:
        return dict_features
    else:
        return {domain: dict_features[domain]}


def standard_statistical_features():
    stats_dict = {"Mean": tsfel.calc_mean, "Max": tsfel.calc_max, "Min": tsfel.calc_min, "Var": tsfel.calc_var,
                  "Std": tsfel.calc_std, "Median": tsfel.calc_median, "kurtosis": tsfel.kurtosis,
                  "skewness": tsfel.skewness, "iqr": tsfel.interq_range, "Mean-abs-dev": tsfel.mean_abs_deviation,
                  "rms": tsfel.rms}

    return stats_dict


def standard_temporal_features():
    temp_dict = {"autocorr": tsfel.autocorr, "Max peaks": tsfel.maxpeaks, "Mean abs diff": tsfel.mean_abs_diff,
                 "Mean diff": tsfel.mean_diff, "Min peaks": tsfel.minpeaks, "Slope": tsfel.slope,
                 "zero cross rate": tsfel.zero_cross, "Abs energy": tsfel.abs_energy}

    return temp_dict


def get_number_features(dict_features):
    """Count the total number of features based on input parameters of each feature

    Parameters
    ----------
    dict_features : dict
        Dictionary with features settings

    Returns
    -------
    int
        Feature vector size
    """
    number_features = 0
    for domain in dict_features:
        for feat in dict_features[domain]:
            if dict_features[domain][feat]["use"] == "no":
                continue
            n_feat = dict_features[domain][feat]["n_features"]

            if isinstance(n_feat, int):
                number_features += n_feat
            else:
                n_feat_param = dict_features[domain][feat]["parameters"][n_feat]
                if isinstance(n_feat_param, int):
                    number_features += n_feat_param
                else:
                    number_features += eval("len("+n_feat_param+")")

    return number_features

