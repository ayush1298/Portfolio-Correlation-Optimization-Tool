
import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import Dashboard from './components/Dashboard';

function App() {
  const [data, setData] = useState(null);

  return (
    <div className="min-h-screen bg-slate-50">
      {!data ? (
        <div className="flex flex-col items-center justify-center min-h-screen">
          <h1 className="text-3xl font-bold text-slate-800 mb-8">Portfolio Correlation & Optimization</h1>
          <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-xl">
            <FileUpload onDataLoaded={setData} />
          </div>
        </div>
      ) : (
        <Dashboard data={data} onReset={() => setData(null)} />
      )}
    </div>
  );
}

export default App;
