# Spam Email Classifier

A modern full-stack spam email classification application with FastAPI backend and React frontend.

## 🚀 Features

- **Direct Email Prediction**: Classify individual emails as Spam or Ham
- **MBOX Batch Processing**: Upload and process entire MBOX files
- **Modern UI**: Professional, responsive design
- **Fast API**: Async FastAPI with auto-generated docs
- **ML Pipeline**: Scikit-learn based classification

## 📋 Tech Stack

**Backend:**
- FastAPI 0.115.6
- Python 3.10+
- scikit-learn
- pandas
- BeautifulSoup4

**Frontend:**
- React 18.3.1
- Vite 6.0.5
- Vanilla CSS

## 🛠️ Installation

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure models are in place:**
   - Model: `outputs/2025-12-25_14-02-05/models/SVM_model.pkl`
   - Vectorizer: `outputs/2025-12-25_14-02-05/models/vectorizer.pkl`

### Frontend Setup

1. **Install Node dependencies:**
   ```bash
   cd frontend
   npm install
   ```

## 🚀 Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
python main.py
```
Or:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Production Mode

**Backend:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Frontend:**
```bash
cd frontend
npm run build
# Serve the dist/ folder with nginx or similar
```

## 📁 Project Structure

```
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── src/
│   ├── pipeline/          # ML pipeline
│   ├── components/        # Data processing
│   ├── config/            # Configuration
│   └── utils/             # Utilities
├── frontend/              # React application
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # API client
│   │   └── ...
│   └── package.json
├── data/                  # Data and models
└── logs/                  # Application logs
```

## 🔌 API Endpoints

### Health Check
```
GET /api/health
```

### Single Email Prediction
```
POST /api/predict
Content-Type: application/json

{
  "email_body": "Your email content here",
  "subject": "Optional subject",
  "recipients": "Optional recipients"
}
```

### MBOX File Upload
```
POST /api/predict-mbox
Content-Type: multipart/form-data

file: <mbox file>
```

### Download Results
```
GET /api/download/{filename}
```

## 🔒 Security

- CORS configured for localhost (update for production)
- Input validation with Pydantic
- File type validation for uploads
- Error handling and logging

## 📊 Model Information

- **Type**: Binary Classification
- **Labels**: 0 = Spam, 1 = Ham
- **Features**: TF-IDF vectorization
- **Algorithm**: SVM (Support Vector Machine)

## 🚀 Deployment

See [Production Report](production_report.md) for detailed deployment instructions.

**Quick Deploy Options:**
- Railway
- Render
- Fly.io
- AWS/GCP/Azure

## 📝 License

[Your License Here]

## 👥 Contributors

[Your Name]

## 🐛 Issues

Report issues at: [Your GitHub Issues URL]
