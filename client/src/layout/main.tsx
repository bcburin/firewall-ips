import { Box, CircularProgress, useTheme } from '@mui/material';
import { ReactNode, useState, } from 'react';

import SideNav from '../components/sidenav';
import TopBar from '../components/topbar';
import { useAppSelector } from '../hooks/redux';
import { useAuthGuard } from '../hooks/auth';

const drawerWidth = 240;

interface MainLayoutProps {
    children: ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
    const theme = useTheme();
    const [sideNavIsOpen, setSideNavIdOpen] = useState(true);
    useAuthGuard(false);

    const isAuthenticated = useAppSelector((state) => state.auth.isAuthenticated);

    const handleDrawerOpen = () => {
        setSideNavIdOpen(true);
    };

    const handleDrawerClose = () => {
        setSideNavIdOpen(false);
    };

    if (!isAuthenticated) {
        return (
            <Box
                sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    height: '100vh'
                }}
            >
                <CircularProgress />
            </Box>
        );
    }

    return (
        <Box sx={{ display: 'flex' }}>
            <TopBar open={sideNavIsOpen} onOpen={handleDrawerOpen} />
            <SideNav open={sideNavIsOpen} onClose={handleDrawerClose} />
            <Box
                component="main"
                sx={{
                    flexGrow: 1,
                    p: 3,
                    mt: '64px',
                    ml: sideNavIsOpen ? 0 : `${-drawerWidth}px`,
                    transition: theme.transitions.create(['margin'], {
                        easing: theme.transitions.easing.sharp,
                        duration: theme.transitions.duration.leavingScreen,
                    }),
                }}
            >
                {children}
            </Box>
        </Box>
    );
};

export default MainLayout;
