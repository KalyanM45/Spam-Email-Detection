const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const predictEmail = async (emailBody) => {
    const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email_body: emailBody }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Prediction failed');
    }

    return response.json();
};

export const predictMbox = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/predict-mbox`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'MBOX processing failed');
    }

    return response.json();
};

export const downloadPredictions = (filename) => {
    window.open(`${API_BASE_URL}/download/${filename}`, '_blank');
};
