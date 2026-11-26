"""
Dataset Loader
Loads the placement dataset into a Pandas DataFrame.
"""

import pandas as pd


def load_dataset():
    """
    Load the placement dataset.
    """

    file_path = "data/placementdata.csv"

    df = pd.read_csv(file_path)

    return df