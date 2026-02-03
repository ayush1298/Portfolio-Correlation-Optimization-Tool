
import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = ({ onDataLoaded }) => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [apiKey, setApiKey] = useState('');
    const [llmApiKey, setLlmApiKey] = useState('');

    const handleFileChange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setLoading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:8000/api/analyze', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'X-LLM-API-KEY': llmApiKey,
                },
            });
            onDataLoaded(response.data);
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.detail || "Failed to analyze portfolio. Ensure Backend is running.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center p-10 border-2 border-dashed border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            <h2 className="text-xl font-semibold mb-4 text-gray-700">Upload Portfolio</h2>

            <div className="w-full mb-6 space-y-3">
                <input
                    type="text"
                    placeholder="OpenAI API Key (Optional)"
                    value={llmApiKey}
                    onChange={(e) => setLlmApiKey(e.target.value)}
                    className="w-full px-4 py-2 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
            </div>

            <p className="text-sm text-gray-500 mb-6">Upload an Excel (.xlsx) or CSV file with a "Ticker" or "Company" column.</p>

            <input
                type="file"
                accept=".csv, .xlsx, .xls"
                onChange={handleFileChange}
                className="block w-full text-sm text-gray-500
          file:mr-4 file:py-2 file:px-4
          file:rounded-full file:border-0
          file:text-sm file:font-semibold
          file:bg-indigo-50 file:text-indigo-700
          hover:file:bg-indigo-100"
            />

            {loading && <div className="mt-4 text-indigo-600 animate-pulse">Analyzing Portfolio... (This may take a moment to fetch data)</div>}
            {error && <div className="mt-4 text-red-500 font-medium">{error}</div>}
        </div>
    );
};

export default FileUpload;
