import { Bar, Line } from 'react-chartjs-2';
import {
    BarElement,
    CategoryScale,
    Chart as ChartJS,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    Title,
    Tooltip,
} from 'chart.js';
import { ChartData, ChartOptions } from 'chart.js';
import { Container, Grid, Typography } from '@mui/material';

import ConfusionMatrix from '../components/confusion-matrix'
import React from 'react';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    LineElement,
    PointElement,
    Title,
    Tooltip,
    Legend
);

const attackTypesOptions: ChartOptions<'bar'> = {
    responsive: true,
    plugins: {
        legend: {
            display: false,
        },
        title: {
            display: true,
            text: 'Number of Attacks per Type in a Period',
        },
    },
    scales: {
        y: {
            beginAtZero: true,
            title: {
                display: true,
                text: 'Number of Attacks',
            },
        },
        x: {
            title: {
                display: true,
                text: 'Attack Types',
            },
        },
    },
};

const portsAttackOptions: ChartOptions<'bar'> = {
    responsive: true,
    plugins: {
        legend: {
            display: false,
        },
        title: {
            display: true,
            text: 'Top 10 Ports That Suffered the Most Attacks',
        },
    },
    scales: {
        y: {
            beginAtZero: true,
            title: {
                display: true,
                text: 'Number of Attacks',
            },
        },
        x: {
            title: {
                display: true,
                text: 'Port Numbers',
            },
        },
    },
};

const attacksPerTimeOptions: ChartOptions<'line'> = {
    responsive: true,
    plugins: {
        legend: {
            display: false,
        },
        title: {
            display: true,
            text: 'Number of Attacks per Time of Day',
        },
    },
    scales: {
        y: {
            beginAtZero: true,
            title: {
                display: true,
                text: 'Number of Attacks',
            },
        },
        x: {
            title: {
                display: true,
                text: 'Time of Day (24h format)',
            },
        },
    },
};

const confusionMatrixChartOptions: ChartOptions<'bar'> = {
    responsive: true,
    plugins: {
        legend: {
            position: 'top',
        },
        title: {
            display: true,
            text: 'Confusion Matrix',
        },
    },
    scales: {
        y: {
            beginAtZero: true,
            title: {
                display: true,
                text: 'Number of Occurrences',
            },
        },
        x: {
            title: {
                display: true,
                text: 'Predicted Classes',
            },
        },
    },
};

const mockAttackTypesData: ChartData<'bar', number[], string> = {
    labels: ['Brute Force', 'SQL Injection', 'DoS', 'DDoS', 'Bot', 'Infiltration'],
    datasets: [
        {
            label: 'Number of Attacks',
            data: [120, 45, 200, 150, 80, 30],
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
        },
    ],
};

const mockPortsAttackData: ChartData<'bar', number[], string> = {
    labels: ['22', '80', '443', '8080', '21', '25', '110', '1433', '3389', '53'],
    datasets: [
        {
            label: 'Number of Attacks',
            data: [300, 450, 200, 180, 250, 150, 100, 220, 130, 90],
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
        },
    ],
};

const mockAttacksPerTimeData: ChartData<'line', number[], string> = {
    labels: ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00'],
    datasets: [
        {
            label: 'Number of Attacks',
            data: [20, 50, 75, 30, 100, 85, 120, 60],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            tension: 0.1,
        },
    ],
};

const cmLabels = ['array', 'function', 'loop', 'pointers'];
const cmData = [
    [0.96, 0.00, 0.00, 0.04],
    [0.08, 0.92, 0.00, 0.00],
    [0.20, 0.20, 0.60, 0.00],
    [0.00, 0.00, 0.00, 1.00],
];


const DashboardPage: React.FC = () => {
    return (
        <Container>
            <Typography variant="h4" sx={{ mt: 4 }}>
                Dashboard
            </Typography>
            <Typography variant="body1" sx={{ mt: 2, mb: 4 }}>

            </Typography>

            <Grid container spacing={4}>
                {/* First row: Two bar charts */}
                <Grid item xs={12} md={6}>
                    <Bar data={mockAttackTypesData} options={attackTypesOptions} />
                </Grid>
                <Grid item xs={12} md={6}>
                    <Bar data={mockPortsAttackData} options={portsAttackOptions} />
                </Grid>

                {/* Second row: Line chart and confusion matrix */}
                <Grid item xs={12} md={6}>
                    <Line data={mockAttacksPerTimeData} options={attacksPerTimeOptions} />
                </Grid>
                <Grid item xs={12} md={6}>
                    <ConfusionMatrix labels={cmLabels} data={cmData} />
                </Grid>
            </Grid>
        </Container>
    );
};

export default DashboardPage;
