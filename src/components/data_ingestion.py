import pandas as pd
from src.utils.logger import get_logger
from src.config.config import Config
from src.utils.state import TrainingState

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self):
        self.config = Config()
    
    def load_data(self, state: TrainingState) -> TrainingState:
        try:
            logger.info("Loading data")
            state.training_data = pd.read_csv(self.config.training_data_path)
            logger.info("Data loaded successfully")
            return state
        except Exception as e:
            logger.error(f"Failed to load data: {str(e)}")
            raise e
    