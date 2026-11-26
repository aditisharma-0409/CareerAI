from sklearn.linear_model import LogisticRegression

def train_logistic_regression(X_train ,y_train):


    model = LogisticRegression(max_iter=1000)

    model.fit(X_train ,y_train)

    return model
    

from sklearn.tree import DecisionTreeClassifier


def train_decision_tree(X_train, y_train):
    """
    Train a Decision Tree Classifier.
    """

    model = DecisionTreeClassifier(
        random_state=42,
        max_depth=5
    )

    model.fit(X_train, y_train)

    return model

from sklearn.ensemble import RandomForestClassifier

def train_random_forest(X_train, y_train):
    """
    Train a Random Forest Classifier.
    """

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    return model