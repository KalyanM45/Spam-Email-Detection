from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_training import ModelTraining
from src.utils.state import TrainingState
from src.utils.logger import get_logger

logger = get_logger(__name__)

class TrainingPipeline:
    """Complete training pipeline for spam classification"""
    
    def __init__(self):
        self.state = TrainingState()
        
    def run_pipeline(self, cv_folds: int = 5):
        try:
            logger.info("Initiating training pipeline")
            ingestion = DataIngestion()
            self.state = ingestion.load_data(self.state)
            logger.info(f"Data loaded successfully: {self.state.training_data.shape}")
            logger.info(f"Columns: {self.state.training_data.columns.tolist()}")
            logger.info(f"Sample size: {len(self.state.training_data)} emails")

            transformation = DataTransformation()
            self.state = transformation.transform_data(self.state)
            logger.info(f"Data transformation completed")
            logger.info(f"Training set: {len(self.state.X_train)} samples")
            logger.info(f"Test set: {len(self.state.X_test)} samples")
            logger.info(f"TF-IDF features: {self.state.X_train_tfidf.shape[1]}")
            
            trainer = ModelTraining()
            self.state = trainer.train_models(
                self.state, 
                cv_folds=cv_folds
            )
            
            logger.info("\n" + "="*70)
            logger.info("Training pipeline completed successfully")
            logger.info("="*70)
            logger.info(f"All metrics saved to 'results/' directory")
            logger.info(f"Best model: {self.state.best_model_name}")
            logger.info(f"Best F1-Score: {self.state.model_metrics[self.state.best_model_name]['f1_score']:.4f}")
            
            return self.state
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            raise e

if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run_pipeline(cv_folds=5)