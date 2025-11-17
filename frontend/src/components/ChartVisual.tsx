import React from 'react';
import {
  Chart as ChartJS,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Pie, Bar, Line } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
);

interface ChartDataset {
  label: string;
  data: number[];
  backgroundColor?: string[];
  borderColor?: string[];
  borderWidth?: number;
}

interface ChartRequest {
  chart_type: 'pie' | 'bar' | 'line';
  title: string;
  labels: string[];
  datasets: ChartDataset[];
  insights?: string[];
}

interface ChartVisualProps {
  chartRequest: ChartRequest;
}

const ChartVisual: React.FC<ChartVisualProps> = ({ chartRequest }) => {
  const { chart_type, title, labels, datasets, insights } = chartRequest;

  // Color palette for charts
  const colorPalette = [
    'rgba(96, 165, 250, 0.8)',   // Blue
    'rgba(165, 180, 252, 0.8)',  // Indigo
    'rgba(251, 146, 60, 0.8)',   // Orange
    'rgba(34, 197, 94, 0.8)',    // Green
    'rgba(244, 63, 94, 0.8)',    // Red
    'rgba(168, 85, 247, 0.8)',   // Purple
    'rgba(236, 72, 153, 0.8)',   // Pink
    'rgba(14, 165, 233, 0.8)',   // Sky
    'rgba(245, 158, 11, 0.8)',   // Amber
    'rgba(59, 130, 246, 0.8)',   // Blue
  ];

  const borderColorPalette = [
    'rgba(96, 165, 250, 1)',
    'rgba(165, 180, 252, 1)',
    'rgba(251, 146, 60, 1)',
    'rgba(34, 197, 94, 1)',
    'rgba(244, 63, 94, 1)',
    'rgba(168, 85, 247, 1)',
    'rgba(236, 72, 153, 1)',
    'rgba(14, 165, 233, 1)',
    'rgba(245, 158, 11, 1)',
    'rgba(59, 130, 246, 1)',
  ];

  // Prepare chart data
  const chartData = {
    labels,
    datasets: datasets.map((dataset) => ({
      ...dataset,
      backgroundColor: dataset.backgroundColor || colorPalette.slice(0, labels.length),
      borderColor: dataset.borderColor || borderColorPalette.slice(0, labels.length),
      borderWidth: dataset.borderWidth || 2,
    })),
  };

  // Chart options
  const options = {
    responsive: true,
    maintainAspectRatio: true,
    aspectRatio: chart_type === 'pie' ? 1.5 : 2,
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          padding: 10,
          font: {
            size: 11,
            family: "'Inter', 'Segoe UI', 'Roboto', sans-serif",
          },
          usePointStyle: true,
          pointStyle: 'circle',
        },
      },
      title: {
        display: true,
        text: title,
        font: {
          size: 14,
          weight: 'bold' as const,
          family: "'Inter', 'Segoe UI', 'Roboto', sans-serif",
        },
        padding: {
          top: 8,
          bottom: 15,
        },
        color: '#232946',
      },
      tooltip: {
        backgroundColor: 'rgba(35, 41, 70, 0.95)',
        titleFont: {
          size: 13,
          family: "'Inter', 'Segoe UI', 'Roboto', sans-serif",
        },
        bodyFont: {
          size: 12,
          family: "'Inter', 'Segoe UI', 'Roboto', sans-serif",
        },
        padding: 12,
        cornerRadius: 8,
        callbacks: {
          label: function (context: any) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += '₹' + context.parsed.y.toLocaleString('en-IN');
            } else if (context.parsed !== null) {
              label += '₹' + context.parsed.toLocaleString('en-IN');
            }
            return label;
          },
        },
      },
    },
  };

  // Render appropriate chart type
  const renderChart = () => {
    switch (chart_type) {
      case 'pie':
        return <Pie data={chartData} options={options} />;
      case 'bar':
        return <Bar data={chartData} options={options} />;
      case 'line':
        return <Line data={chartData} options={options} />;
      default:
        return <Pie data={chartData} options={options} />;
    }
  };

  return (
    <div className="chart-visual">
      <div className="chart-container">
        {renderChart()}
      </div>
    </div>
  );
};

export default ChartVisual;
