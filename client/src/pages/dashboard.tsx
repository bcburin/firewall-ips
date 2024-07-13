import { Container, Typography } from '@mui/material';

import React from 'react';

const DashboardPage: React.FC = () => {
    return (
        <Container>
            <Typography variant="h4" sx={{ mt: 4 }}>
                Dashboard
            </Typography>
            <Typography variant="body1" sx={{ mt: 2 }}>
                Welcome to the dashboard!
            </Typography>
        </Container>
    );
};

export default DashboardPage;