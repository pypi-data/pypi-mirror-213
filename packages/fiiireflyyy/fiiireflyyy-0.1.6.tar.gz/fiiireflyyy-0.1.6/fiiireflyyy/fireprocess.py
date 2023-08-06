import os
import re
import sys

import pandas as pd
import numpy as np
import fiiireflyyy.firefiles as ff
from pathlib import Path
import matplotlib.pyplot as plt


def floor_ceil_in_range(value, low_thresh: float == 0.0, high_thresh: float == 255.0):
    """
    Thresholds a value considering a minimum and maximum value.

        Parameters
        ----------
        value: int, float
            the value to floor or ceil.
        low_thresh: float, optional, default: 0.0
            The minimum limit to thresholds the value
        high_thresh: float, optional, default: 255.0
            The maximum limit to thresholds the value.

        Returns
        -------
        out: int, float
            The thresholded value.
    """
    if value > high_thresh:
        return high_thresh
    elif value < low_thresh:
        return low_thresh
    else:
        return value




def merge_all_columns_to_mean(df: pd.DataFrame, except_column=""):
    """
    average all the columns, except an optional specified one,
    in a dataframe into one. The average is done row-wise.

        Parameters
        ----------
        df: DataFrame
            the dataframe to average
        except_column: str, optional, default: ""
            the name of the column to exclude from the average.
            Will be included in the resulting dataset.

        Returns
        --------
        out: DataFrame
            Dataframe containing on column labeled 'mean', and
            an optional second column based on the
            except_column parameter
    """

    excepted_column = pd.DataFrame()
    if except_column:
        for col in df.columns:
            if except_column in col:
                except_column = col
        excepted_column = df[except_column]
        df.drop(except_column, axis=1, inplace=True)

    df_mean = pd.DataFrame(columns=["mean", ])
    df_mean['mean'] = df.mean(axis=1)

    if except_column != "":
        for col in df.columns:
            if except_column in col:
                except_column = col
        df_mean[except_column] = excepted_column

    return df_mean

def equal_samples(df, n):
    """
    cuts a DataFrame in n sub-DataFrame of same length.

        Parameters
        ----------
        df: DataFrame
            Object to cut, row-wise.
        n: int
            number of resulting samples.

        Returns
        -------
        out: list of DataFrame
            contains all the sub DataFrames.
    """
    step = int(len(df) / n)
    lower_limit = 0
    upper_limit = step
    samples = []
    while upper_limit <= len(df):
        samples.append(df[lower_limit:upper_limit])
        lower_limit = upper_limit
        upper_limit += step
    return samples

def discard_outliers_by_iqr(df: pd.DataFrame, **kwargs):
    """
    remove outliers from a dataframe using the interquartile range method.

        Parameters
        ----------
        df: pd.Dataframe
            the dataframe containing the data.
            Must contain a column 'label'.

        **kwargs: keyword arguments
            low_percentile : float, default: 0.25
                the low percentile for IQR outliers removal.
            high_percentile : float, default: 0.75
                the high percentile for IQR outliers removal.
            iqr_limit_factor : float, default: 1.5
                the factor used to determine when the point is
                an outlier compared to the percentiles.
            save: str, default: ""
                Where to save the resulting plot.
                If empty, the plot will not be saved.
                WARNING : may cause randomly 'Key error: 0'.
            mode: {'capping', }, default: capping
                The method used to discard the outliers.
                More to come.

        Returns
        -------
        out: pd.Dataframe
            the dataframe without the outliers
    """
    options = {"low_percentile": 0.25,
               "high_percentile": 0.75,
               "iqr_limit_factor": 1.5,
               "save": "",
               "mode": "capping"}
    options.update(kwargs)
    labels = df["label"].unique()
    labels_values = {}
    for n in range(len(labels)):
        labels_values[labels[n]] = n

    features = list(df.columns.values)
    features.remove('label')
    metrics = np.empty(shape=(len(labels), len(features)), dtype=object)

    # obtaining the metrics [lower_limit, upper_limit]
    for i_label in range(len(labels)):
        label = labels[i_label]
        sub_df = df.loc[df['label'] == label]
        for i_feat in range(len(features)):
            feat = features[i_feat]
            # finding the iqr
            low_percentile = sub_df[feat].quantile(options["low_percentile"])
            high_percentile = sub_df[feat].quantile(options["high_percentile"])
            iqr = high_percentile - low_percentile
            # finding upper and lower limit
            lower_limit = low_percentile - options["iqr_limit_factor"] * iqr
            upper_limit = high_percentile + options["iqr_limit_factor"] * iqr
            metrics[i_label][i_feat] = [lower_limit, upper_limit]

    discarded_df = pd.DataFrame(columns=features)
    discarded_labels = pd.DataFrame(columns=["label", ])

    for i in range(len(df.values)):
        discarded_row = []
        discarded_label = df['label'].iloc[i]
        for j in range(len(df.values[i]) - 1):
            lower_limit, upper_limit = metrics[labels_values[discarded_label], j]
            if options["mode"] == "capping":
                if df.iloc[i, j] > upper_limit:
                    discarded_row.append(upper_limit)
                elif df.iloc[i, j] < lower_limit:
                    discarded_row.append(lower_limit)
                else:
                    discarded_row.append(df.iloc[i, j])

        discarded_labels.loc[len(discarded_labels)] = discarded_label
        discarded_df.loc[len(discarded_df)] = discarded_row

    discarded_df["label"] = discarded_labels["label"]
    return discarded_df


def smoothing(data, n: int, mode='mean'):
    """
    Smoothen a signal down to n values, depending on the smoothing mode.

        Parameters
        ----------
        data: list of int, list of float
            contains the numerical data to smoothen.
        n: int
            number of points to down sample the data to.
        mode: str, optional, default: 'mean'
            the way to smoothen the data between the points.

        Returns
        -------
        out: list of floats
            the smoothened data.

    """
    if len(data.index) > n:
        step = int(len(data.index) / n)
        lower_limit = 0
        upper_limit = step
        ds_data = []
        if mode == 'mean':
            while upper_limit <= len(data):
                ds_data.append(np.mean(data[lower_limit:upper_limit]).round(3))
                lower_limit = upper_limit
                upper_limit += step
        excedent = len(ds_data) - n
        ds_data = ds_data[:-excedent or None]
        return ds_data
    else:
        raise Exception("smoothing: length of data " + str(len(data.index)) + "< n " + str(n))


def make_dataset_from_freq_files(parent_dir, **kwargs):
    """
    Use frequency files of format two columns (one column 'Frequencies [Hz]' and one column 'mean') to generate a
    dataset used for classification. Specialized for recording of electrical signal. The path tree has to be
    organised as such :
    base/condition (ej. drug addition)/recording time/target for classification (ej. infected/not
    infected)/sample number/my_freq_files.csv .

        Parameters
        ----------
        parent_dir: str.
            the parent directory where to look for all the
            frequency files.

        **kwargs: keyword arguments
            filename: str, optional. Default: ""
                the name of the resulting csv file if
                'savedir' is not empty.
            savedir: str, optional. Default: ""
                If empty, the resulting dataset will
                not be saved under a csv file. Else,
                is the path where to save the csv file.
            to_include: tuple of str, optional. Default: ()
                Allows to specify what sequences the file paths must
                contain. All the elements of this tuple must be
                present in the file path for it to be kept for the
                final dataset.
            to_exclude: tuple of str, optional. Default: ()
                Allows to specify what sequences the file paths must
                not contain. If the path contains any of the element
                of this tuple, the file will not be kept for the final
                dataset.
            freq_range: tuple of floats of length 2, optional. Default: ()
                If not empty, only the frequencies between the first
                element (min frequency) and the second element
                (max frequency) will be kept, looking at the column
                "Frequency [Hz]" of the frequency file.
            verbose: bool, optional. Default: False
                Whether to display more information in the console
                during the process or not.
            separate_samples: bool, optional. Default: False.
                Whether to give the different samples of a same
                condition different labels.
            select_sample: list of str, optional. Default: None
                If not None, keep only the frequency files that come
                from the specified samples.
            sample_parent_degree: int, optional. Default: 1
                In the path, the parenting degree that is referring
                to the sample number.
            target_parent_degree : int, optional. Default: 2
                In the path, the parenting degree that is referring
                to the target label.
            target_keys : dict, optional. Default: {'NI': 'NI', 'INF': 'INF'}
                The keys refer to how the target is labeled in the file path.
                The value is how the target will be labeled in the dataset.
            label_comment: str, optional. Default: ""
                Any str to add to the labels in the dataset.

        Returns
        -------
        out: pd.Dataframe
            the resulting dataset.

        Example
        -------
        >>> import fiiireflyyy.fireprocess as fp
        >>> mydf = fp.make_dataset_from_freq_files(parent_dir="my/parent/path/here",
                                             to_include=("freq_50hz_sample", "T=24H"),
                                             to_exclude=("TTX", "mydrug",),
                                             verbose=False,
                                             savedir=False,
                                             freq_range=(0, 400),
                                             select_samples=None,
                                             target_keys={"NI": "not infected", "INF": "infected"},
                                             separate_samples=False,
                                             label_comment="")

        will result in a dataset based on all the files containing both "freq_50hz_sample" and "T=24H",
        and that do contain neither "TTX" nor "mydrug". The dataset will be the result of the smoothing
        of all frequencies between 0 and 400 Hz, taking account of all the samples. In the path,
        the 'NI' condition will be labeled as 'not infected' in the dataset, same goes for 'INF' and
        'infected'. The dataset will not be saved on the system.
    """

    options = {"filename": "",
               "to_include": (),
               "to_exclude": (),
               "freq_range": (),
               "savedir": "",
               "verbose": False,
               "separate_samples": False,
               "select_samples": None,
               "sample_parent_degree": 1,
               "target_parent_degree": 2,
               "target_keys": {'NI': 'NI', 'INF': 'INF'},
               "label_comment": "", }
    options.update(**kwargs)

    if options["select_samples"] is None:
        options["select_samples"] = list(
            set(list(ff.get_all_parent_by_degree(parent_dir, options["sample_parent_degree"]))))

    files = ff.get_all_files(os.path.join(parent_dir))
    freq_files = []
    for f in files:
        if all(i in f for i in options["to_include"]) and (not any(e in f for e in options["to_exclude"])) and \
                os.path.basename(ff.nth_parent(f, options["sample_parent_degree"])) in options["select_samples"]:
            freq_files.append(f)
    if options["verbose"]:
        print("added: ", freq_files)
    columns = list(range(0, 300))
    dataset = pd.DataFrame(columns=columns)
    target_df = pd.DataFrame(columns=["label", ])

    n_processed_files = 0
    for f in freq_files:
        df = pd.read_csv(f)
        if options["freq_range"]:
            # selecting the frequencies range
            df = df.loc[
                (df["Frequency [Hz]"] >= options["freq_range"][0]) & (df["Frequency [Hz]"] <= options["freq_range"][1])]
        # smoothing by n values
        smooth_df = smoothing(df["mean"], 300, 'mean')

        # construct the dataset with n features
        dataset.loc[len(dataset)] = smooth_df

        path = Path(f)

        for target in options["target_keys"]:
            if target in os.path.basename(ff.nth_parent(f, options["target_parent_degree"])):
                if options["separate_samples"]:
                    target_df.loc[len(target_df)] = options["target_keys"][target] + str(
                        os.path.basename(path.parent)) + options["label_comment"]
                else:
                    target_df.loc[len(target_df)] = options["target_keys"][target] + options["label_comment"]

        if options["verbose"]:
            progress = int(np.ceil(n_processed_files / len(freq_files) * 100))
            sys.stdout.write(f"\rProgression of processing files: {progress}%")
            sys.stdout.flush()
            n_processed_files += 1
    dataset["label"] = target_df["label"]
    if options["verbose"]:
        print("\n")
    if options["savedir"]:
        dataset.to_csv(os.path.join(options["savedir"], options["filename"]), index=False)
    return dataset
