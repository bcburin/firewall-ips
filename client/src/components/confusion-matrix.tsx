import { Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';

// ConfusionMatrix.tsx
import React from 'react';

interface ConfusionMatrixProps {
    labels: string[];
    data: number[][];
}

const ConfusionMatrix: React.FC<ConfusionMatrixProps> = ({ labels, data }) => {
    const getColor = (value: number): string => {
        const blueIntensity = Math.round(255 - value * 255);
        return `rgb(${blueIntensity}, ${blueIntensity}, 255)`;
    };

    return (
        <Box display="flex" flexDirection="column" alignItems="center">
            <Typography variant="subtitle1" gutterBottom>
                Confusion Matrix
            </Typography>
            <TableContainer>
                <Table size="small">
                    <TableBody>
                        <TableRow>
                            <TableCell style={{ padding: '0px', width: '50px' }} />
                            {labels.map((label, index) => (
                                <TableCell
                                    key={index}
                                    align="center"
                                    style={{
                                        fontWeight: 300,
                                        fontSize: '0.75rem',
                                        padding: '4px',
                                        width: '60px',
                                        whiteSpace: 'nowrap',
                                        color: '#555',
                                    }}
                                >
                                    {label}
                                </TableCell>
                            ))}
                        </TableRow>
                        {data.map((row, rowIndex) => (
                            <TableRow key={rowIndex}>
                                <TableCell
                                    style={{
                                        fontWeight: 300,
                                        fontSize: '0.75rem',
                                        color: '#555',
                                        padding: '4px',
                                        textAlign: 'center',
                                        width: '60px',
                                    }}
                                >
                                    {labels[rowIndex]}
                                </TableCell>
                                {row.map((value, colIndex) => (
                                    <TableCell
                                        key={colIndex}
                                        align="center"
                                        style={{
                                            backgroundColor: getColor(value),
                                            color: value > 0.5 ? 'white' : 'black',
                                            width: '50px',
                                            height: '50px',
                                            padding: '0px', // Reduce padding for a tighter look
                                            fontSize: '0.75rem',
                                            opacity: 0.5,
                                            border: '1px'
                                        }}
                                    >
                                        {value.toFixed(2)}
                                    </TableCell>
                                ))}
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    );
};

export default ConfusionMatrix;
