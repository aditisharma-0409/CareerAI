from sklearn.metrics import (accuracy_score,confusion_matrix,classification_report)

def evaluate_model(model,X_test,y_test):
    y_pred = model.predict(X_test)
    accuracy= accuracy_score(y_test,y_pred)
    print("\n========== MODEL ACCURACY ==========")
    print(f"Accuracy : {accuracy:.4f}")

    # Confusion Matrix
    print("\n========== CONFUSION MATRIX ==========")
    print(confusion_matrix(y_test, y_pred))

    # Classification Report
    print("\n========== CLASSIFICATION REPORT ==========")
    print(classification_report(y_test, y_pred))
