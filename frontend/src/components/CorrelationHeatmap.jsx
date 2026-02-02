
import React from 'react';
import Plot from 'react-plotly.js';

const CorrelationHeatmap = ({ data }) => {
    if (!data || Object.keys(data).length === 0) return null;

    const tickers = Object.keys(data);
    const zValues = tickers.map(t => Object.values(data[t]));

    return (
        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
            <h3 className="text-lg font-semibold mb-2">Correlation Matrix</h3>
            <div className="w-full h-96">
                <Plot
                    data={[
                        {
                            z: zValues,
                            x: tickers,
                            y: tickers,
                            type: 'heatmap',
                            colorscale: 'RdBu',
                            zmin: -1,
                            zmax: 1,
                        }
                    ]}
                    layout={{
                        autosize: true,
                        title: 'Asset Correlation',
                        margin: { t: 30, r: 30, l: 50, b: 50 }
                    }}
                    useResizeHandler={true}
                    style={{ width: '100%', height: '100%' }}
                />
            </div>
        </div>
    );
};

export default CorrelationHeatmap;
