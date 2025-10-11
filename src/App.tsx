import { useState, useEffect, useRef } from 'react';
import { Chart, registerables } from 'chart.js';

import SalesDrilldown from './SalesDrilldown';
import RiderDemographics from './RiderDemographics';

// This line just tells chartjs to load all its features
Chart.register(...registerables);


//reeusable component for the cards on our dashboard.
function Card({ title, children }: { title: string, children: React.ReactNode }) {
    return (
        <div className="bg-white shadow-lg rounded-xl p-6 border border-slate-200">
            <h2 className="text-2xl font-bold text-slate-800 mb-4">{title}</h2>
            {children}
        </div>
    );
}

export default function App() {

    const [etlStatus, setEtlStatus] = useState<Record<string, string>>({});
    const [groupBy, setGroupBy] = useState('month');

    const salesChartCanvas = useRef<HTMLCanvasElement>(null);

    const salesChartInstance = useRef<Chart | null>(null);



    //useeffect happens after rednering so usually it's used for fetch
    // the empty dependency array [] means this effect will only run ONCE, right after the component first mounts (is put on the screen).
    useEffect(() => {
        async function fetchEtlStatus() {
            console.log("Fetching ETL status...");
            try {
                //for equivalent sql statements, check server.ts
                const response = await fetch('http://localhost:3001/api/etl-status');
                const data = await response.json();

                setEtlStatus(data);
            } catch (error) {
                console.error('Failed to fetch ETL status:', error);
            }
        }
        fetchEtlStatus();
    }, []);


    useEffect(() => {
        async function renderSalesChart() {
            if (!salesChartCanvas.current) {
                return;
            }

            try {
                const response = await fetch(`http://localhost:3001/api/sales-rollup?groupBy=${groupBy}`);
                const data: Record<string, number> = await response.json();

                const labels = Object.keys(data);
                const values = Object.values(data);

                // destroy a chart first if it already exists.
                // If we don't, we get weird bugs where charts draw on top of each other.
                if (salesChartInstance.current) {
                    salesChartInstance.current.destroy();
                }
                salesChartInstance.current = new Chart(salesChartCanvas.current, {
                    type: 'bar', //bar ? can change
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Total Revenue',
                            data: values,
                            backgroundColor: 'rgba(59, 130, 246, 0.5)',
                            borderColor: 'rgba(59, 130, 246, 1)',
                            borderWidth: 1,
                            borderRadius: 4,
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });

            } catch (error) {
                console.error('Failed to render sales chart:', error);
            }
        }

        renderSalesChart();
    }, [groupBy]);


    return (
        <div className="bg-slate-50 min-h-screen font-sans">
            <div className="container mx-auto p-8">
                <header className="mb-8">
                    <h1 className="text-4xl font-black text-slate-900">OLAP Dashboard</h1>
                    <div className="text-sm text-slate-500 mt-2">
                        <strong>Last Data Load:</strong>
                        {Object.entries(etlStatus).map(([table, time]) => (
                            ` | ${table}: ${new Date(time).toLocaleString()}`
                        ))}
                    </div>
                </header>

                <main className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <Card title="Report 1: Sales Roll-up">
                        <div className="controls mb-4">
                            <label htmlFor="time-period-select" className="font-semibold text-slate-700 mr-2">View by:</label>
                            <select
                                id="time-period-select"
                                value={groupBy}
                                onChange={(e) => setGroupBy(e.target.value)}
                                className="border-slate-300 rounded-md shadow-sm"
                            >
                                <option value="day">Day</option>
                                <option value="month">Month</option>
                                <option value="quarter">Quarter</option>
                                <option value="year">Year</option>
                            </select>
                        </div>
                        <canvas ref={salesChartCanvas}></canvas>
                    </Card>

                    {/* Report 2 Card */}
                    <Card title="Report 2: Sales Drill-down">
                        <SalesDrilldown />
                    </Card>

                    {/* Report 3 Card. col span 2 to take up screen width*/}
                    <div className="lg:col-span-2">
                        <Card title="Report 3: Rider Demographics (Slice & Dice)">
                            <RiderDemographics />
                        </Card>
                    </div>
                </main>
            </div>
        </div>
    );
}