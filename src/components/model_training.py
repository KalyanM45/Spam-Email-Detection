import os
import time
import json
import pickle
from datetime import datetime

import numpy as np
import pandas as pd

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

from src.utils.logger import get_logger
from src.utils.state import TrainingState
from src.config.config import Config, ModelConfig

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self):
        self.config = Config()
        self.param_grids = ModelConfig.models
    
    def save_pickle_files(self, state: TrainingState):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_dir = os.path.join(self.config.OUTPUT_BASE_DIR, timestamp)
            models_dir = os.path.join(output_dir, "models")
            observations_dir = os.path.join(output_dir, "observations")
        
            os.makedirs(models_dir, exist_ok=True)
            os.makedirs(observations_dir, exist_ok=True)

            vectorizer_path = os.path.join(models_dir, "vectorizer.pkl")
            with open(vectorizer_path, 'wb') as f:
                pickle.dump(state.tfidf_vectorizer, f)
            logger.info(f"Saved TF-IDF vectorizer: {vectorizer_path}")
        
            best_model_path = os.path.join(models_dir, f"{state.best_model_name}_model.pkl")
            with open(best_model_path, 'wb') as f:
                pickle.dump(state.best_model, f)
            logger.info(f"Saved best model: {state.best_model_name}_model.pkl")
        
            metadata = {
                'timestamp': timestamp,
                'best_model_name': state.best_model_name,
                'best_model_params': str(state.best_params),
                'best_model_metrics': str(state.model_metrics[state.best_model_name]),
                'all_models': ', '.join(list(state.trained_models.keys())),
                'tfidf_features': state.X_train_tfidf.shape[1],
                'train_samples': len(state.y_train),
                'test_samples': len(state.y_test)
            }
            
            metadata_path = os.path.join(observations_dir, "model_metadata.csv")
            pd.DataFrame([metadata]).to_csv(metadata_path, index=False)
            logger.info(f"Saved metadata: {metadata_path}")
            
            return output_dir

        except Exception as e:
            logger.error(f"Failed to save pickle files: {str(e)}")
            raise
    
    def save_metrics_to_csv(self, state: TrainingState, output_dir: str):
        observations_dir = os.path.join(output_dir, "observations")
        os.makedirs(observations_dir, exist_ok=True)
        
        # 1. Model Comparison Summary
        # ----------------------------------------------------------------------
        metrics_data = []
        for model_name, metrics in state.model_metrics.items():
            metrics_data.append({
                'Model': model_name,
                'Accuracy': metrics['accuracy'],
                'Precision': metrics['precision'],
                'Recall': metrics['recall'],
                'F1_Score': metrics['f1_score'],
                'CV_Score': metrics.get('best_cv_score', 'N/A'),
                'Is_Best_Model': '1' if model_name == state.best_model_name else '0'
            })
        
        df_summary = pd.DataFrame(metrics_data)
        df_summary = df_summary.sort_values('Accuracy', ascending=False)
        summary_path = os.path.join(observations_dir, "model_comparison_summary.csv")
        df_summary.to_csv(summary_path, index=False)
        logger.info(f"Saved: model_comparison_summary.csv")
        
        # 2. Best Parameters for Each Model
        # ----------------------------------------------------------------------
        params_data = []
        for model_name, metrics in state.model_metrics.items():
            best_params = metrics.get('best_params', {})
            if isinstance(best_params, dict):
                params_str = json.dumps(best_params, indent=2)
            else:
                params_str = str(best_params)
            
            params_data.append({
                'Model': model_name,
                'Best_Parameters': params_str,
                'CV_Score': metrics.get('best_cv_score', 'N/A')
            })
        
        df_params = pd.DataFrame(params_data)
        params_path = os.path.join(observations_dir, "best_parameters.csv")
        df_params.to_csv(params_path, index=False)
        logger.info(f"Saved: best_parameters.csv")
        
        # 3. Cross-Validation Results Summary
        # ----------------------------------------------------------------------
        if state.cv_results:
            cv_summary = []
            for model_name, cv_data in state.cv_results.items():
                cv_summary.append({
                    'Model': model_name,
                    'Best_CV_Score': cv_data.get('best_score', 'N/A'),
                    'Best_Parameters': json.dumps(cv_data.get('best_params', {}))
                })
            
            df_cv = pd.DataFrame(cv_summary)
            cv_path = os.path.join(observations_dir, "cross_validation_summary.csv")
            df_cv.to_csv(cv_path, index=False)
            logger.info(f"Saved: cross_validation_summary.csv")
        
        # 4. Best Model Information
        # ----------------------------------------------------------------------
        best_model_info = {
            'Attribute': [
                'Best Model Name',
                'Accuracy',
                'Precision',
                'Recall',
                'F1-Score',
                'CV Score',
                'Best Parameters'
            ],
            'Value': [
                state.best_model_name,
                state.model_metrics[state.best_model_name]['accuracy'],
                state.model_metrics[state.best_model_name]['precision'],
                state.model_metrics[state.best_model_name]['recall'],
                state.model_metrics[state.best_model_name]['f1_score'],
                state.model_metrics[state.best_model_name].get('best_cv_score', 'N/A'),
                json.dumps(state.best_params, indent=2) if isinstance(state.best_params, dict) else str(state.best_params)
            ]
        }
        
        df_best = pd.DataFrame(best_model_info)
        best_path = os.path.join(observations_dir, "best_model_info.csv")
        df_best.to_csv(best_path, index=False)
        logger.info(f"Saved: best_model_info.csv")


    def train_models(self, state: TrainingState, cv_folds: int = 5) -> TrainingState:
        logger.info("Model training started")
        logger.info(f"Using GridSearchCV with {cv_folds}-fold CV")
        
        try:
            X_train = state.X_train_tfidf
            X_test = state.X_test_tfidf
            y_train = state.y_train
            y_test = state.y_test
            
            trained_models, model_metrics, cv_results = {}, {}, {}
            
            # Define model instances
            models = {
                'LogisticRegression': LogisticRegression(random_state=42),
                'DecisionTree': DecisionTreeClassifier(random_state=42),
                'SVM': SVC(random_state=42),
                'KNN': KNeighborsClassifier(),
                'RandomForest': RandomForestClassifier(random_state=42)
            }
            
            for model_name, model in models.items():
                start_time = time.time()
                logger.info(f"\n{'='*60}")
                logger.info(f"Training {model_name}...")
                
                param_grid = self.param_grids.get(model_name, {})
                
                search = GridSearchCV(model,
                                    param_grid=param_grid,
                                    cv=cv_folds,
                                    scoring='f1',
                                    n_jobs=-1
                                    )
                
                search.fit(X_train, y_train)
                best_model = search.best_estimator_
                
                y_pred = best_model.predict(X_test)
                
                metrics = {
                    'accuracy': accuracy_score(y_test, y_pred),
                    'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
                    'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
                    'f1_score': f1_score(y_test, y_pred, average='weighted', zero_division=0),
                    'best_params': search.best_params_,
                    'best_cv_score': search.best_score_
                }
                
                trained_models[model_name] = best_model
                model_metrics[model_name] = metrics
                cv_results[model_name] = {
                    'cv_scores': search.cv_results_,
                    'best_params': search.best_params_,
                    'best_score': search.best_score_
                }
                
                end_time = time.time()
                
                logger.info(f"{model_name} - Training time: {end_time - start_time:.2f} seconds")
                logger.info(f"{model_name} - Best Parameters: {search.best_params_}")
                logger.info(f"{model_name} - CV Score: {search.best_score_:.4f}")
                logger.info(f"{model_name} - Test Accuracy: {metrics['accuracy']:.4f}")
                logger.info(f"{model_name} - Test Precision: {metrics['precision']:.4f}")
                logger.info(f"{model_name} - Test Recall: {metrics['recall']:.4f}")
                logger.info(f"{model_name} - Test F1-Score: {metrics['f1_score']:.4f}")
            
            # Find best model based on F1-score
            best_model_name = max(model_metrics, key=lambda x: model_metrics[x]['f1_score'])
            best_model = trained_models[best_model_name]
            best_params = model_metrics[best_model_name]['best_params']
            
            logger.info(f"{'='*60}")
            logger.info(f"BEST MODEL: {best_model_name}")
            logger.info(f"Best F1-Score: {model_metrics[best_model_name]['f1_score']:.4f}")
            logger.info(f"Best Parameters: {best_params}")
            logger.info(f"{'='*60}")
            
            state.trained_models = trained_models
            state.model_metrics = model_metrics
            state.best_model_name = best_model_name
            state.best_model = best_model
            state.best_params = best_params
            state.cv_results = cv_results
            
            output_dir = self.save_pickle_files(state)
            self.save_metrics_to_csv(state, output_dir)
            logger.info("\nModel training completed successfully")
            logger.info(f"All outputs saved to: {output_dir}/")
            return state
            
        except Exception as e:
            logger.error(f"Failed to train models: {str(e)}")
            raise e