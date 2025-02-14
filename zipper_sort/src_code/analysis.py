"""
Simple proof of concept to test out 'zipper-sorting' a database by balancing two (or more) sorting criteria when sorting the results. Test case: sorting Amazon search results to fall in order not just of cheapest->priciest nor in order of highest rating->lowest rating, but to be a mixture of both.

"""

from zipper_sort.src_code.utils import which_data_to_analyze, get_data_file, load_data, reverse_order, get_smoothing_type, combine, min_max_normalize
import numpy as np
import pandas as pd

__author__ = "Christian N. Sodano"
__version__ = "0.1.0"

# @audit in future change to a general, programmatic method that accounts for any number of columns
DATA_PATH = "zipper_sort/data/"
SORT_ORDER_PRICE_COL = "descending"
SORT_ORDER_RATING_COL = "ascending"


def main():

    default_or_user_input = which_data_to_analyze()

    file = get_data_file(default_or_user_input, type_="raw")

    df, price_col, rating_col = load_data(file)

    if SORT_ORDER_PRICE_COL == "descending":
        price_col = reverse_order(price_col)
    if SORT_ORDER_RATING_COL == "descending":
        # Skipped in this example
        rating_col = reverse_order(rating_col)

    smoothing_type = get_smoothing_type()

    normd_rating_col = min_max_normalize(rating_col, smoothing_type)
    normd_price_col = min_max_normalize(price_col, smoothing_type)

    df["combined"] = combine(
        normd_price_col, normd_rating_col, smoothing_type)

    sorted_df = df.sort_values(by=["combined"], ascending=False)
    breakpoint()
    # @audit replace w/ relative-path "save_data" function
    sorted_df.to_csv(DATA_PATH + "example/processed/" +
                     input("save name? add .csv: "))


if __name__ == "__main__":
    main()
