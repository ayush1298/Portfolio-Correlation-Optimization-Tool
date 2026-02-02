
import React from 'react';
import CorrelationHeatmap from './CorrelationHeatmap';
import Plot from 'react-plotly.js';

const Dashboard = ({ data, onReset }) => {
    if (!data) return null;

    const { tickers, correlation_matrix, volatility, current_performance, optimized_weights, llm_advice } = data;

    // Prepare Optimization Data for Chart
    const mvoData = optimized_weights.mvo;
    const hrpData = optimized_weights.hrp;

    const mvoX = Object.keys(mvoData);
    const mvoY = Object.values(mvoData);

    return (
        <div className="p-6 space-y-6 bg-slate-50 min-h-screen">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-slate-800">Portfolio Analytics</h1>
                <button onClick={onReset} className="px-4 py-2 bg-slate-200 hover:bg-slate-300 rounded text-sm font-medium">
                    Upload New File
                </button>
            </div>

            {/* Metrics Row */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white p-4 rounded shadow border border-slate-100">
                    <p className="text-sm text-slate-500">Exp. Annual Return</p>
                    <p className="text-2xl font-bold text-green-600">{(current_performance.return * 100).toFixed(2)}%</p>
                </div>
                <div className="bg-white p-4 rounded shadow border border-slate-100">
                    <p className="text-sm text-slate-500">Annual Volatility</p>
                    <p className="text-2xl font-bold text-red-500">{(current_performance.volatility * 100).toFixed(2)}%</p>
                </div>
                <div className="bg-white p-4 rounded shadow border border-slate-100">
                    <p className="text-sm text-slate-500">Sharpe Ratio</p>
                    <p className="text-2xl font-bold text-blue-600">{current_performance.sharpe.toFixed(2)}</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <CorrelationHeatmap data={correlation_matrix} />

                {/* Optimization Weights Chart */}
                <div className="bg-white p-4 rounded shadow border border-slate-100">
                    <h3 className="text-lg font-semibold mb-2">Optimized Allocation (MVO)</h3>
                    <div className="h-96">
                        <Plot
                            data={[{
                                x: mvoX,
                                y: mvoY,
                                type: 'bar',
                                marker: { color: '#6366f1' }
                            }]}
                            layout={{ autosize: true, margin: { t: 20, b: 40 } }}
                            useResizeHandler={true}
                            style={{ width: '100%', height: '100%' }}
                        />
                    </div>
                </div>
            </div>

            {/* LLM Advice Section */}
            <div className="bg-white p-6 rounded shadow border border-indigo-100">
                <h3 className="text-lg font-semibold mb-4 text-indigo-900">AI Investment Insights</h3>
                <div className="prose prose-sm max-w-none text-slate-700 whitespace-pre-line">
                    {llm_advice}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
