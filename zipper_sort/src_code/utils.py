from pathlib import Path
import os
import pandas as pd


def which_data_to_analyze():
    # @audit add input sanitization
    idx = int(input("Are you running the analysis on the default-provided example data (0) or self-provided user data (1)?: Please input 0 (example) or 1 (user_data): "))
    options = ["example", "user_data"]
    return options[idx]


def get_data_file(default_or_user_input: str, type_: str):
    """Pulls into a pandas DataFrame the data imported from openalex's API and cleaned. Presumes file structure of this codebase stays the same when running pipeline. 


    Args:
        default_or_user_input (str): Can be either "default" or "user_data"
        type_ (str): can be either "raw" "preprocessed" or "processed"

    """
    print(f"Pulling the {type_} data from the {default_or_user_input} folder.")

    options = ["example", "user_data"]
    assert default_or_user_input in options, "Must be either 'example' or 'user_data'"
    data_path = Path(__file__).parent / "data" / default_or_user_input / type_

    files_in_dir = os.listdir(data_path)

    data_file_path = data_path / _get_correct_file(files_in_dir)
    return str(data_file_path)
    # df: pd.DataFrame = pd.read_pickle(str(data_file_path))
    # print(f"\nData pulled from {data_file_path.stem}")
    # return df


def _get_correct_file(files_in_dir: list):

    if len(files_in_dir) > 0:
        print("Detected at least one data file in the directory.")
        answer = input(
            f"The directory has the following files: {files_in_dir}. Type the index (starting from 0) of the file you want to pull. If none of these are the correct file, input '-1' and the script will exit.: ")
        try:
            answer = int(answer)
            if (0 <= answer < len(files_in_dir)):
                print(f"Returning {files_in_dir[answer]}")
                return files_in_dir[answer]
            else:
                if answer == -1:
                    exit()
                else:
                    raise ValueError
        except ValueError:
            print(
                "Please input a valid integer corresponding to the index of the data file that you wish to pull")
            return _get_correct_file(files_in_dir)
    else:
        print("Detected no files in the data directory. You may have deleted the file, or you may need to first run the processing step on the raw data if you are trying to access processed data. Exiting")
        exit()


def get_columns_from_data(df) -> tuple[pd.Series, pd.Series]:
    price_col = df.loc[:, "price"]
    rating_col = df.loc[:, "rating"]
    return price_col, rating_col


def clean_data(df) -> pd.DataFrame:
    df = df.dropna()
    df = df.drop_duplicates(subset=["Title"])
    price_col, rating_col = get_columns_from_data(df)
    df = df.drop(price_col[price_col == "--"].index)
    # Unclear if this ever occurs in the data, putting it for good measure
    df = df.drop(rating_col[rating_col == "--"].index)
    return df


def load_data(file_name: str) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    df = pd.read_csv(file_name,
                     usecols=["Title", "price", "rating"])
    df = clean_data(df)
    price_col, rating_col = get_columns_from_data(df)
    rating_col = rating_col.apply(float)
    price_col = price_col.apply(float)  # From string
    return df, price_col, rating_col


def reverse_order(series_) -> pd.Series:
    """By inverting the series's values, when combining later with another column through multiplication this effectively reverses the sort order
    """  # @audit for issues with interaction of min/max norm and ()^-1
    series_ = series_.apply(lambda x: x**-1)
    return series_


def get_smoothing_constant(normd_series_):
    _ = normd_series_.drop(normd_series_.idxmin())
    return _.min()*0.01  # @audit run tests for cases where this degenerates. Consider programmatic scaling factor instead of hard-coded constant


def add_add_one_smoothing(series_):
    add_one_smoothed_series_ = series_.apply(
        lambda x: 1 + ((x-series_.min())/(series_.max()-series_.min())))
    # breakpoint #@audit good stopping place for debugging add-one-smoothing
    return add_one_smoothed_series_


# @audit bookmark pane note
def add_smoothing(series_, smoothing_factor: float):
    smoothed_series_ = series_.apply(lambda x: (
        (x-series_.min()+smoothing_factor)/(series_.max()-series_.min())))
    return smoothed_series_


def min_max_normalize(series_, smoothing_type: str = "add small constant") -> pd.Series:
    """Normalizes the values to spread between 0 (lowest) and 1(highest).
    Requires conversion to float beforehand.
    """
    smoothing_factor: float = 0.0
    normd_series_ = series_.apply(lambda x: (
        (x-series_.min())/(series_.max()-series_.min())))
    match smoothing_type:
        case "none":
            return normd_series_
        case "add one smoothing":
            normd_smoothed_series_ = add_add_one_smoothing(series_)
        case "add small constant":
            smoothing_factor: float = get_smoothing_constant(normd_series_)
            normd_smoothed_series_ = add_smoothing(
                series_, smoothing_factor=smoothing_factor)
    return normd_smoothed_series_


def combine(series1, series2, smoothing_type: str) -> pd.Series:
    result = series1*series2
    match smoothing_type:
        case "add one smoothing":
            result_normd = result.apply(lambda x: (
                x-result.min()) / (result.max()-result.min()))
            return result_normd
        case _:
            return result


def get_smoothing_type():
    answer = int(input(
        "Which smoothing type would you like to use? input the index of the array corresponding to the element you'd like to choose (starting from 0): [None, add one smoothing, add a small constant smoothing]: "))  # @audit add input sanitization later
    return ["none", "add one smoothing", "add small constant"][answer]
