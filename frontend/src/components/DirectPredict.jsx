import { useState } from 'react';
import { predictEmail } from '../services/api';
import './DirectPredict.css';

function DirectPredict() {
    const [emailBody, setEmailBody] = useState('');
    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!emailBody.trim()) {
            setError('Please enter email content');
            return;
        }

        setLoading(true);
        setError(null);
        setPrediction(null);

        try {
            const result = await predictEmail(emailBody);
            setPrediction(result);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleClear = () => {
        setEmailBody('');
        setPrediction(null);
        setError(null);
    };

    return (
        <div className="direct-predict">
            <div className="predict-header">
                <h2>📧 Direct Email Prediction</h2>
                <p>Paste your email content below to check if it's spam</p>
            </div>

            <form onSubmit={handleSubmit} className="predict-form">
                <div className="form-group">
                    <label htmlFor="email-body">Email Content</label>
                    <textarea
                        id="email-body"
                        value={emailBody}
                        onChange={(e) => setEmailBody(e.target.value)}
                        placeholder="Paste your email content here..."
                        rows={12}
                        disabled={loading}
                    />
                </div>

                <div className="button-group">
                    <button type="submit" className="btn btn-primary" disabled={loading}>
                        {loading ? (
                            <>
                                <span className="spinner"></span>
                                Analyzing...
                            </>
                        ) : (
                            <>
                                <span>🔍</span>
                                Predict
                            </>
                        )}
                    </button>
                    <button type="button" className="btn btn-secondary" onClick={handleClear} disabled={loading}>
                        Clear
                    </button>
                </div>
            </form>

            {error && (
                <div className="alert alert-error">
                    <span>⚠️</span>
                    <p>{error}</p>
                </div>
            )}

            {prediction && (
                <div className="prediction-result">
                    <div className={`result-card ${prediction.prediction.toLowerCase() === 'spam' ? 'spam' : 'not-spam'}`}>
                        <div className="result-header">
                            <span className="result-icon">
                                {prediction.prediction.toLowerCase() === 'spam' ? '🚫' : '✅'}
                            </span>
                            <h3>Prediction Result</h3>
                        </div>
                        <div className="result-body">
                            <div className="result-item">
                                <span className="label">Classification:</span>
                                <span className={`value ${prediction.prediction.toLowerCase() === 'spam' ? 'spam-text' : 'ham-text'}`}>
                                    {prediction.prediction}
                                </span>
                            </div>
                            {prediction.confidence && (
                                <div className="result-item">
                                    <span className="label">Confidence:</span>
                                    <span className="value">{prediction.confidence.toFixed(2)}%</span>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default DirectPredict;
