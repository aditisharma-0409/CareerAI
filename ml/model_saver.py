"""
Save and Load Machine Learning Models
"""

import joblib
import os


def save_model(model, filename="careerai_model.pkl"):
    """
    Save the trained model to disk.
    """

    os.makedirs("saved_models", exist_ok=True)

    filepath = os.path.join("saved_models", filename)

    joblib.dump(model, filepath)

    print(f"\n✅ Model saved successfully at: {filepath}")


def load_model(filename="careerai_model.pkl"):
    """
    Load a saved model from disk.
    """

    filepath = os.path.join("saved_models", filename)

    model = joblib.load(filepath)

    return model