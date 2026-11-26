"""
Feature Engineering
"""

def split_features_target(df):
    """
    Separate input features (X) and target (y).
    """

    X = df.drop(columns=["StudentID", "PlacementStatus"])

    y = df["PlacementStatus"]

    return X, y