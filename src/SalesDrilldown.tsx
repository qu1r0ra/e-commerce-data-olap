
import { useState, useEffect, useRef } from 'react';

import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);


export default function SalesDrilldown() {

    const [viewLevel, setViewLevel] = useState('category');
    const [categoryFilter, setCategoryFilter] = useState('');


    const chartCanvas = useRef<HTMLCanvasElement>(null);
    const chartInstance = useRef<Chart | null>(null);


    useEffect(() => {

        const renderChart = async () => {
            if (!chartCanvas.current) return;

            const isCategoryView = viewLevel === 'category';

            const endpoint = isCategoryView
                ? `http://localhost:3001/api/sales-by-category`
                : `http://localhost:3001/api/sales-by-product?category=${categoryFilter}`;

            const chartTitle = isCategoryView ? 'Sales by Category (Click a bar to drill down)' : `Product Sales in ${categoryFilter}`;

            try {//checl in server.ts
                const response = await fetch(endpoint);
                if (!response.ok) {
                    throw new Error(`Failed to fetch: ${response.status} ${response.statusText}`);
                }
                const data = await response.json();


                const labels = Object.keys(data);
                const values = Object.values(data);

                if (chartInstance.current) {
                    chartInstance.current.destroy();
                }

                chartInstance.current = new Chart(chartCanvas.current, {
                    type: 'bar',
                    data: {
                        labels,
                        datasets: [{
                            label: 'Total Revenue',
                            data: values,
                            backgroundColor: 'rgba(255, 99, 132, 0.5)',
                            borderColor: 'rgba(255, 99, 132, 1)',
                            borderWidth: 1,
                        }]
                    },
                    options: {
                        plugins: { title: { display: true, text: chartTitle } },

                        onClick: (event, elements) => {

                            if (viewLevel !== 'category' || elements.length === 0) {
                                return;
                            }
                            const clickedIndex = elements[0].index; // our way of knowing which element to drilldown
                            const clickedCategory = labels[clickedIndex];

                            setViewLevel('product');
                            setCategoryFilter(clickedCategory);
                        },

                        onHover: (event, chartElement) => {
                            const canvas = event.native?.target as HTMLCanvasElement;
                            if (canvas) {
                                canvas.style.cursor = chartElement[0] && isCategoryView ? 'pointer' : 'default';
                            }
                        },
                    }
                });
            } catch (error) {
                console.error('[Frontend] Failed to render sales chart:', error);
            }
        };

        renderChart();
    }, [viewLevel, categoryFilter]);

    const handleBackClick = () => {
        setViewLevel('category');
        setCategoryFilter('');
    };

    return (
        <div>
            {viewLevel === 'product' && (
                <button
                    onClick={handleBackClick}
                    className="mb-4 px-4 py-2 bg-slate-600 text-white rounded-md hover:bg-slate-700 transition"
                >
                    &larr; Back to Categories
                </button>
            )}
            <canvas ref={chartCanvas}></canvas>
        </div>
    );
}