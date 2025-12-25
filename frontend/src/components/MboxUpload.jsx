import { useState, useRef } from 'react';
import { predictMbox, downloadPredictions } from '../services/api';
import './MboxUpload.css';

function MboxUpload() {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [dragActive, setDragActive] = useState(false);
    const fileInputRef = useRef(null);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFileChange(e.dataTransfer.files[0]);
        }
    };

    const handleFileChange = (selectedFile) => {
        if (selectedFile) {
            // Check if file has .mbox extension
            if (!selectedFile.name.endsWith('.mbox')) {
                setError('Please select a valid MBOX file (.mbox extension)');
                setFile(null);
                return;
            }
            setFile(selectedFile);
            setError(null);
            setResult(null);
        }
    };

    const handleFileInputChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFileChange(e.target.files[0]);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!file) {
            setError('Please select an MBOX file');
            return;
        }

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const data = await predictMbox(file);
            setResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleDownload = () => {
        if (result && result.download_url) {
            const filename = result.download_url.split('/').pop();
            downloadPredictions(filename);
        }
    };

    const handleClear = () => {
        setFile(null);
        setResult(null);
        setError(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    return (
        <div className="mbox-upload">
            <div className="upload-header">
                <h2>📁 MBOX File Upload</h2>
                <p>Upload your MBOX file to analyze multiple emails at once</p>
            </div>

            <form onSubmit={handleSubmit} className="upload-form">
                <div
                    className={`drop-zone ${dragActive ? 'active' : ''} ${file ? 'has-file' : ''}`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                    onClick={() => fileInputRef.current?.click()}
                >
                    <input
                        ref={fileInputRef}
                        type="file"
                        accept=".mbox"
                        onChange={handleFileInputChange}
                        style={{ display: 'none' }}
                        disabled={loading}
                    />

                    {file ? (
                        <div className="file-info">
                            <span className="file-icon">📧</span>
                            <div className="file-details">
                                <p className="file-name">{file.name}</p>
                                <p className="file-size">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                            </div>
                            <button
                                type="button"
                                className="remove-file"
                                onClick={(e) => {
                                    e.stopPropagation();
                                    handleClear();
                                }}
                                disabled={loading}
                            >
                                ✕
                            </button>
                        </div>
                    ) : (
                        <div className="drop-zone-content">
                            <span className="upload-icon">📤</span>
                            <p className="drop-text">
                                <strong>Click to upload</strong> or drag and drop
                            </p>
                            <p className="drop-hint">MBOX files only</p>
                        </div>
                    )}
                </div>

                <div className="button-group">
                    <button type="submit" className="btn btn-primary" disabled={loading || !file}>
                        {loading ? (
                            <>
                                <span className="spinner"></span>
                                Processing...
                            </>
                        ) : (
                            <>
                                <span>🚀</span>
                                Analyze MBOX
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

            {result && (
                <div className="result-summary">
                    <div className="summary-card">
                        <div className="summary-header">
                            <span className="summary-icon">📊</span>
                            <h3>Analysis Complete</h3>
                        </div>

                        <div className="summary-stats">
                            <div className="stat-item">
                                <span className="stat-label">Total Emails</span>
                                <span className="stat-value">{result.total_emails}</span>
                            </div>

                            {result.predictions && Object.entries(result.predictions).map(([category, count]) => (
                                <div key={category} className="stat-item">
                                    <span className="stat-label">{category}</span>
                                    <span className={`stat-value ${category.toLowerCase() === 'spam' ? 'spam-count' : 'safe-count'}`}>
                                        {count}
                                    </span>
                                </div>
                            ))}
                        </div>

                        <button className="btn btn-download" onClick={handleDownload}>
                            <span>⬇️</span>
                            Download Results (CSV)
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default MboxUpload;
