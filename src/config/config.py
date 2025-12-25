from dataclasses import dataclass

@dataclass
class Config:
    training_data_path: str = "data/dataset/dataset.csv"
    validation_data_path: str = "data/dataset/All_mail_Including_Spam_and_Trash.mbox"
    OUTPUT_BASE_DIR: str = "outputs"
    model_path: str = "outputs/2025-12-25_14-02-05/models/SVM_model.pkl"
    feature_path: str = "outputs/2025-12-25_14-02-05/models/vectorizer.pkl"

class ModelConfig:
    models = {
        'LogisticRegression': {
            'C': [0.01, 0.1, 1, 10, 100],
            'solver': ['lbfgs', 'liblinear'],
            'max_iter': [100, 200, 300]
        },
        'DecisionTree': {
            'criterion': ['gini', 'entropy'],
            'max_depth': [5, 10, 15, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        },
        'SVM': {
            'C': [0.1, 1, 10],
            'kernel': ['linear', 'rbf'],
            'gamma': ['scale', 'auto']
        },
        'KNN': {
            'n_neighbors': [3, 5, 7, 9, 11],
            'weights': ['uniform', 'distance'],
            'metric': ['euclidean', 'manhattan']
        },
        'RandomForest': {
            'n_estimators': [50, 100, 200],
            'max_depth': [10, 20, 30, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['sqrt', 'log2']
        }
    }