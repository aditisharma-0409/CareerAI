"""
Data Quality Checks
"""

def check_missing_values(df):
    print("\n========== MISSING VALUES ==========")
    print(df.isnull().sum())


def check_duplicate_rows(df):
    print("\n========== DUPLICATE ROWS ==========")
    print(df.duplicated().sum())


def check_data_types(df):
    print("\n========== DATA TYPES ==========")
    print(df.dtypes)