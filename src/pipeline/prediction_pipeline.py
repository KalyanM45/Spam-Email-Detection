import mailbox
import pickle
import time
import pandas as pd
from typing import Dict, List, Optional
from pathlib import Path

from src.utils.state import PredictionState
from src.utils.logger import get_logger
from src.config.config import Config
from src.utils.email_utils import extract_body, all_recipients, clean_text

logger = get_logger(__name__)

class PredictionPipeline:
    def __init__(self, load_models: bool = True):
        self.config = Config()
        self.mailbox = None
        self.feature_transformer = None
        self.model = None
        
        if load_models:
            self._load_models()
    
    def _load_models(self) -> None:

        logger.info("Loading models...")
        self.feature_transformer = pickle.load(open(self.config.feature_path, "rb"))
        self.model = pickle.load(open(self.config.model_path, "rb"))
        logger.info("Models loaded successfully")
    
    def predict_single_email(self, email_body: str) -> Dict:
        if self.model is None or self.feature_transformer is None:
            self._load_models()

        cleaned_body = clean_text(email_body)
        features = self.feature_transformer.transform([cleaned_body])
        prediction = self.model.predict(features)
        prediction_label = "Spam" if str(prediction[0]) == "0" else "Ham"
        
        try:
            prediction_proba = self.model.predict_proba(features)
            confidence = float(max(prediction_proba[0])) * 100
        except:
            confidence = None
        
        return {
            'prediction': prediction_label,
            'confidence': confidence,
            'raw_prediction': int(prediction[0])
        }

    def load_mailbox(self, mailbox_path: str) -> None:
        """Load MBOX file"""

        logger.info(f"Loading mailbox from {mailbox_path}")
        self.mailbox = mailbox.mbox(mailbox_path)
        logger.info(f"Loaded mailbox from {mailbox_path}")

    def process_mailbox(self, mailbox_path: Optional[str] = None) -> List[Dict]:
        if mailbox_path:
            self.load_mailbox(mailbox_path)
        
        if self.mailbox is None:
            raise ValueError("No mailbox loaded. Call load_mailbox() first.")
        
        logger.info("Processing mailbox")
        data = []
        
        for message in self.mailbox:
            labels = (message.get("X-Gmail-Labels") or "").lower()
            category = (
                "Spam" if "spam" in labels else
                "Promotions" if "category_promotions" in labels else
                "Social" if "category_social" in labels else
                "Updates" if "category_updates" in labels else
                "Inbox"
            )
            time_str = message.get("Date", "")
            recipients = clean_text(all_recipients(message))
            subject = clean_text(message.get("Subject", ""))
            body = clean_text(extract_body(message))
            direction = "Sent" if "Sent" in (message.get("X-Gmail-Labels") or "") else "Received"
            
            data.append({
                "Time": time_str,
                "Recipients": recipients,
                "Subject": subject,
                "Body": body,
                "Category": category,
                "Direction": direction
            })
        
        logger.info(f"Processed {len(data)} emails from mailbox")
        self.mailbox.close()
        
        return data
    
    def run_prediction(self, mail_data: List[Dict]) -> List[Dict]:
        if self.model is None or self.feature_transformer is None:
            self._load_models()
        
        start_time = time.time()
        logger.info("Running predictions")
        
        for mail in mail_data:
            body_text = mail.get('Body', '')
            features = self.feature_transformer.transform([body_text])
            prediction = self.model.predict(features)
            prediction_label = "Spam" if str(prediction[0]) == "0" else "Ham"
            mail["Prediction"] = prediction_label
        
        end_time = time.time()
        logger.info(f"Prediction completed in {end_time - start_time:.2f} seconds")
        
        return mail_data
    
    def predict_mbox_file(self, mailbox_path: str, output_path: Optional[str] = None) -> pd.DataFrame:
        mail_data = self.process_mailbox(mailbox_path)
        mail_data = self.run_prediction(mail_data)
        df = pd.DataFrame(mail_data)
        if output_path:
            df.to_csv(output_path, index=False)
            logger.info(f"Predictions saved to {output_path}")
        return df


def run_legacy_pipeline(state: PredictionState) -> None:
    pipeline = PredictionPipeline(load_models=False)
    pipeline.load_mailbox(state.mailbox_path)
    mail_data = pipeline.process_mailbox()
    state.mail_data = mail_data
    state.mail_data = pipeline.run_prediction(state.mail_data)
    df = pd.DataFrame(state.mail_data)
    df.to_csv("data/predictions.csv", index=False)