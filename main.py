from ml.dataset_loader import load_dataset
from ml.dataset_analysis import (
    dataset_shape,
    dataset_columns,
    dataset_info,
    dataset_statistics,
)
from ml.data_quality import (
    check_missing_values,
    check_duplicate_rows,
    check_data_types,
)

from ml.feature_engineering import split_features_target
from ml.train_test_splitter import split_dataset
from ml.model_training import (train_logistic_regression, train_decision_tree,train_random_forest)

from ml.encoder import encode_labels
from ml.evaluation import evaluate_model
from ml.model_saver import save_model
from ml.model_saver import load_model
from ml.prediction import predict_student
def main():
    df = load_dataset()
    df = encode_labels(df)
    # print("\n========== FIRST FIVE ROWS ==========")
    # print(df.head())

    # dataset_shape(df)
    # dataset_columns(df)
    # dataset_info(df)
    # dataset_statistics(df)

    # check_missing_values(df)
    # check_duplicate_rows(df)
    # check_data_types(df)
    
    
    X, y = split_features_target(df)

    
    X_train, X_test, y_train, y_test = split_dataset(X, y)

    # print("\n===== TRAINING DATA =====")
    # print(X_train.shape)

    # print("\n===== TESTING DATA =====")
    # print(X_test.shape)

    # print("\n===== TRAINING LABELS =====")
    # print(y_train.shape)

    # print("\n===== TESTING LABELS =====")
    # print(y_test.shape)

    # model = train_logistic_regression(X_train ,y_train)
    # save_model(model)

    # evaluate_model(model, X_test, y_test)

    print("\n" + "=" * 60)
    print("PLACEMENT PREDICTION")
    print("=" * 60)

    saved_model = load_model()

    predict_student(saved_model)
    

    # print("\n✅ Logistic Regression Model Trained Successfully!")
    # evaluate_model(model, X_test, y_test)
    # print("\n" + "="*60)
    # print("DECISION TREE MODEL")
    # print("="*60)

    # decision_tree_model = train_decision_tree(X_train, y_train)

    # evaluate_model(decision_tree_model, X_test, y_test)

    # print("\n" + "=" * 60)
    # print("RANDOM FOREST MODEL")
    # print("=" * 60)

    # random_forest_model = train_random_forest(X_train, y_train)

    # evaluate_model(random_forest_model, X_test, y_test)
    
    # print("\n========== FEATURES ==========")
    # print(X.head())

    # print("\n========== TARGET ==========")
    # print(y.head())
    
    # print("\n===== ENCODED DATA =====")
    # print(df.head())

if __name__ == "__main__":
    main()