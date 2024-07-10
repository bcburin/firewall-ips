import { Container, Typography } from '@mui/material';

import DashboardLayout from '../layout/dashboard';
import React from 'react';

const DashboardPage: React.FC = () => {
  return (
    <DashboardLayout>
        <Container>
            <Typography variant="h4" sx={{ mt: 4 }}>
                Dashboard
            </Typography>
            <Typography variant="body1" sx={{ mt: 2 }}>
                Welcome to the dashboard!
            </Typography>
        </Container>
    </DashboardLayout>
  );
};

export default DashboardPage;