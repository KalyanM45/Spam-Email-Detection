import { useState } from 'react';
import DirectPredict from './components/DirectPredict';
import MboxUpload from './components/MboxUpload';
import './App.css';

function App() {
    const [activeTab, setActiveTab] = useState('direct');

    return (
        <div className="app">
            <div className="app-background"></div>

            <div className="app-container">
                <header className="app-header">
                    <div className="header-content">
                        <h1 className="app-title">
                            <span className="title-icon">🛡️</span>
                            Spam Email Classifier
                        </h1>
                    </div>
                </header>

                <div className="tab-container">
                    <div className="tab-buttons">
                        <button
                            className={`tab-button ${activeTab === 'direct' ? 'active' : ''}`}
                            onClick={() => setActiveTab('direct')}
                        >
                            <span>📧</span>
                            Direct Prediction
                        </button>
                        <button
                            className={`tab-button ${activeTab === 'mbox' ? 'active' : ''}`}
                            onClick={() => setActiveTab('mbox')}
                        >
                            <span>📁</span>
                            MBOX Upload
                        </button>
                    </div>

                    <div className="tab-content">
                        {activeTab === 'direct' ? <DirectPredict /> : <MboxUpload />}
                    </div>
                </div>


            </div>
        </div>
    );
}

export default App;
