import React, { useState } from 'react';
import { Button, TextField, Container, Typography, Box, CircularProgress } from '@mui/material';
import axios from 'axios';
import MapComponent from './MapComponent';
import LogDisplay from './LogDisplay';

function App() {
    const [formData, setFormData] = useState({
        current: '',
        pickup: '',
        dropoff: '',
        cycle: ''
    });
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        
        try {
            const response = await axios.post('http://localhost:8000/api/calculate/', formData);
            setResult(response.data);
        } catch (err) {
            setError(err.response?.data?.error || 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container maxWidth="md" sx={{ py: 4 }}>
            <Typography variant="h4" gutterBottom>
                ELD Log Generator
            </Typography>
            
            <Box component="form" onSubmit={handleSubmit} sx={{ mb: 4 }}>
                <TextField
                    fullWidth
                    label="Current Location"
                    name="current"
                    value={formData.current}
                    onChange={(e) => setFormData({...formData, current: e.target.value})}
                    margin="normal"
                    required
                />
                <TextField
                    fullWidth
                    label="Pickup Location"
                    name="pickup"
                    value={formData.pickup}
                    onChange={(e) => setFormData({...formData, pickup: e.target.value})}
                    margin="normal"
                    required
                />
                <TextField
                    fullWidth
                    label="Dropoff Location"
                    name="dropoff"
                    value={formData.dropoff}
                    onChange={(e) => setFormData({...formData, dropoff: e.target.value})}
                    margin="normal"
                    required
                />
                <TextField
                    fullWidth
                    label="Current Cycle Used (Hrs)"
                    name="cycle"
                    type="number"
                    value={formData.cycle}
                    onChange={(e) => setFormData({...formData, cycle: e.target.value})}
                    margin="normal"
                    required
                    inputProps={{ min: 0, max: 70, step: 0.1 }}
                />
                
                <Button
                    type="submit"
                    variant="contained"
                    disabled={loading}
                    sx={{ mt: 2 }}
                    startIcon={loading ? <CircularProgress size={20} /> : null}
                >
                    {loading ? 'Calculating...' : 'Generate Route & Logs'}
                </Button>
            </Box>

            {error && (
                <Typography color="error" sx={{ mb: 2 }}>
                    {error}
                </Typography>
            )}

            {result && (
                <>
                    <Typography variant="h6" gutterBottom>
                        Route Overview
                    </Typography>
                    <Typography>
                        Distance: {result.distance.toFixed(2)} miles | Duration: {result.duration.toFixed(2)} hours
                    </Typography>
                    
                    <MapComponent route={result.route} />
                    
                    <Typography variant="h6" sx={{ mt: 4 }} gutterBottom>
                        ELD Logs
                    </Typography>
                    <LogDisplay logs={result.logs} />
                </>
            )}
        </Container>
    );
}

export default App;