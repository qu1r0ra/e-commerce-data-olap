import { useState, useEffect, useRef } from 'react';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);


export default function RiderDemographics() {

    const [couriers, setCouriers] = useState<string[]>([]);

    const [selectedCourier, setSelectedCourier] = useState<string>('');

    const chartCanvas = useRef<HTMLCanvasElement>(null);
    const chartInstance = useRef<Chart | null>(null);


    useEffect(() => {
        const fetchCouriers = async () => {
            try {
                const response = await fetch('http://localhost:3001/api/rider-demographics?query=couriers');

                const data = await response.json();
                setCouriers(data);
            } catch (error) {
                console.error('Failed to fetch couriers', error);
            }
        };

        fetchCouriers();
    }, []);

    useEffect(() => {
        const fetchDataAndRenderChart = async () => {
            if (!chartCanvas.current) return;

            // better check in server.ts for endpoints, if the courier selected is empty that equates to === all
            const endpoint = `http://localhost:3001/api/rider-demographics?courierName=${selectedCourier}`;
            const chartTitle = selectedCourier ? `Rider Breakdown for ${selectedCourier}` : 'Rider Breakdown (All Couriers)';

            try {
                const response = await fetch(endpoint);

                const data = await response.json();
                const labels = Object.keys(data).sort();
                const values = labels.map(label => data[label]);


                if (chartInstance.current) {
                    chartInstance.current.destroy();
                }

                chartInstance.current = new Chart(chartCanvas.current, {
                    type: 'bar',
                    data: {
                        labels,
                        datasets: [{
                            label: '# of Riders',
                            data: values,
                            backgroundColor: 'rgba(153, 102, 255, 0.5)',
                            borderColor: 'rgba(153, 102, 255, 1)',
                            borderWidth: 1,
                        }]
                    },
                    options: {
                        indexAxis: 'y',
                        plugins: { title: { display: true, text: chartTitle } },
                        scales: { x: { beginAtZero: true, ticks: { stepSize: 1 } } }
                    }
                });
            } catch (error) {
                console.error('Failed to render demographics chart:', error);
            }
        };

        fetchDataAndRenderChart();
    }, [selectedCourier]);


    return (
        <div>
            <div className="controls mb-4">
                <label htmlFor="courier-select" className="font-semibold text-slate-700 mr-2">Slice by Courier:</label>

                <select
                    id="courier-select"
                    value={selectedCourier}
                    onChange={(e) => setSelectedCourier(e.target.value)} // When it changes, we update the state.
                    className="border-slate-300 rounded-md shadow-sm"
                >
                    <option value="">All Couriers</option>
                    {couriers.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
            </div>
            <canvas ref={chartCanvas}></canvas>
        </div>
    );
}