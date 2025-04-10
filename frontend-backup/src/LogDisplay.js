import React from 'react';
import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';

const LogDisplay = ({ logs }) => {
    return (
        <TableContainer component={Paper} sx={{ mt: 4 }}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>Day</TableCell>
                        <TableCell align="right">Driving (hrs)</TableCell>
                        <TableCell align="right">On Duty (hrs)</TableCell>
                        <TableCell align="right">Rest (hrs)</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {logs.map((log) => (
                        <TableRow key={log.day}>
                            <TableCell>{log.day}</TableCell>
                            <TableCell align="right">{log.driving.toFixed(2)}</TableCell>
                            <TableCell align="right">{log.on_duty.toFixed(2)}</TableCell>
                            <TableCell align="right">{log.rest.toFixed(2)}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};

export default LogDisplay;