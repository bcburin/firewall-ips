import { Button, Container, Paper, Typography } from '@mui/material';

import React from 'react';
import { useNavigate } from 'react-router-dom';

const NotFoundPage: React.FC = () => {
    const navigate = useNavigate();

    const handleGoBack = () => {
        navigate('/dashboard');
    };

    return (
        <Container component="main" maxWidth="md">
            <Paper
                elevation={3}
                sx={{
                    mt: 8,
                    p: 4,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}
            >
                <Typography variant="h1" component="h1" gutterBottom>
                    404
                </Typography>
                <Typography variant="h3" component="h2" gutterBottom>
                    Page Not Found
                </Typography>
                <Typography variant="subtitle1" gutterBottom>
                    Sorry, the page you are looking for does not exist.
                </Typography>
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleGoBack}
                    sx={{ mt: 2 }}
                >
                    Go to Dashboard
                </Button>
            </Paper>
        </Container>
    );
};

export default NotFoundPage;
