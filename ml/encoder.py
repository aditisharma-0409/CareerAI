from sklearn.preprocessing import LabelEncoder

def encode_labels(df):

    encoder = LabelEncoder()

    categorical_columns= [
        "ExtracurricularActivities",
        "PlacementTraining",
        "PlacementStatus"

    ]
    for column in categorical_columns:
        df[column] = encoder.fit_transform(df[column])
    
    return df