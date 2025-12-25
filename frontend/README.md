# Spam Email Classifier - React Frontend

A modern React application for spam email classification with two main features:

## Features

### 1. Direct Email Prediction
- Paste email content directly into the interface
- Get instant spam classification results
- View confidence scores

### 2. MBOX File Upload
- Upload MBOX files containing multiple emails
- Batch process all emails in the file
- Download results as CSV

## Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+

### Installation

1. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Install Backend Dependencies**
   ```bash
   cd ..
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Flask Backend** (Terminal 1)
   ```bash
   python app.py
   ```
   Backend will run on `http://localhost:5000`

2. **Start the React Frontend** (Terminal 2)
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend will run on `http://localhost:3000`

3. **Open your browser** and navigate to `http://localhost:3000`

## Tech Stack

- **Frontend**: React, Vite
- **Backend**: Flask, Flask-CORS
- **ML**: scikit-learn, pandas
- **Styling**: Modern CSS with gradients and glassmorphism

## API Endpoints

- `POST /api/predict` - Predict single email
- `POST /api/predict-mbox` - Process MBOX file
- `GET /api/download/<filename>` - Download predictions CSV
- `GET /api/health` - Health check

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── DirectPredict.jsx
│   │   ├── DirectPredict.css
│   │   ├── MboxUpload.jsx
│   │   └── MboxUpload.css
│   ├── services/
│   │   └── api.js
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   └── index.css
├── index.html
├── package.json
└── vite.config.js
```
