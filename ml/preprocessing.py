import pandas as pd


def check_missing_values(df):
    """
    Display missing values in each column.
    """
    print("\n===== Missing Values =====\n")
    print(df.isnull().sum())


def check_duplicates(df):
    """
    Display the number of duplicate rows.
    """
    print("\n===== Duplicate Rows =====\n")
    print(df.duplicated().sum())


def check_data_types(df):
    """
    Display data types of all columns.
    """
    print("\n===== Data Types =====\n")
    print(df.dtypes)