"""
Dataset Analysis
Basic analysis of the placement dataset.
"""


def dataset_shape(df):
    print("\n========== DATASET SHAPE ==========")
    print(df.shape)


def dataset_columns(df):
    print("\n========== COLUMN NAMES ==========")
    print(df.columns.tolist())


def dataset_info(df):
    print("\n========== DATASET INFO ==========")
    df.info()


def dataset_statistics(df):
    print("\n========== STATISTICAL SUMMARY ==========")
    print(df.describe())