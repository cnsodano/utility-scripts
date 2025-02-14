## Explaining Processed Data
Results of the (as of 2-14-2025) zipper_sort/analysis.py script processing the raw data. The processing steps include dropping NaNs, duplicate items, min-max normalizing the price and rating column values, adding smoothing to account for issues when combining the last-place ranked value for either column, finally implementing the zipper sort and saving the resulting csv as a sorted dataframe according to the combination of the two column sort priorities.

Files: 

- processed_small_raw_data-2-13-2025.csv  = pipeline output when ran on first 15 results
- processed_large_raw_data-2-13-2025.csv  = pipeline output when ran on first 160 results
