from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import tempfile
import os
import pandas as pd
from datetime import datetime

from src.pipeline.prediction_pipeline import PredictionPipeline
from src.utils.logger import get_logger

app = FastAPI(title="Spam Email Classifier API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("FRONTEND_URL", "http://localhost:3000"),
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = get_logger(__name__)

pipeline = PredictionPipeline(load_models=True)

# Request/Response models
class EmailPredictionRequest(BaseModel):
    email_body: str

class EmailPredictionResponse(BaseModel):
    prediction: str
    confidence: float | None
    email_body: str

class MboxPredictionResponse(BaseModel):
    total_emails: int
    predictions: dict
    download_url: str


@app.post("/api/predict", response_model=EmailPredictionResponse)
async def predict_email(request: EmailPredictionRequest):
    """
    Predict spam classification for a single email body
    """
    try:
        email_body = request.email_body
        
        if not email_body or not email_body.strip():
            raise HTTPException(status_code=400, detail="Email body cannot be empty")
        
        # Use prediction pipeline (only body is needed)
        result = pipeline.predict_single_email(email_body=email_body)
        
        logger.info(f"Prediction made: {result['prediction']}")
        
        return EmailPredictionResponse(
            prediction=result['prediction'],
            confidence=result['confidence'],
            email_body=email_body[:200] + '...' if len(email_body) > 200 else email_body
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in predict_email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/api/predict-mbox", response_model=MboxPredictionResponse)
async def predict_mbox(file: UploadFile = File(...)):
    """
    Process MBOX file and return predictions for all emails
    """
    try:
        if not file.filename.endswith('.mbox'):
            raise HTTPException(status_code=400, detail="File must be an MBOX file")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mbox') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            logger.info(f"Processing MBOX file: {file.filename}")
            
            # Use prediction pipeline
            df = pipeline.predict_mbox_file(tmp_path)
            
            # Save results to CSV
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"predictions_{timestamp}.csv"
            output_path = os.path.join(tempfile.gettempdir(), output_filename)
            df.to_csv(output_path, index=False)
            
            logger.info(f"Processed {len(df)} emails from MBOX file")
            
            # Return summary
            return MboxPredictionResponse(
                total_emails=len(df),
                predictions=df['Prediction'].value_counts().to_dict(),
                download_url=f'/api/download/{output_filename}'
            )
            
        finally:
            # Clean up temporary MBOX file
            if os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception as e:
                    logger.warning(f"Could not delete temporary file {tmp_path}: {str(e)}")
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in predict_mbox: {str(e)}")
        raise HTTPException(status_code=500, detail=f"MBOX processing failed: {str(e)}")

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """
    Download the generated predictions CSV file
    """
    try:
        file_path = os.path.join(tempfile.gettempdir(), filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=file_path,
            media_type='text/csv',
            filename=filename
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in download_file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
