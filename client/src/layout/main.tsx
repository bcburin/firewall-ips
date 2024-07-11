import { ReactNode, useState } from 'react'

import Box from '@mui/material/Box';
import SideNav from '../components/sidenav';
import TopBar from '../components/topbar';
import { useAuthGuard } from '../hooks/auth';
import { useTheme } from '@mui/material';

const drawerWidth = 240;

interface MainLayoutProps {
    children: ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }: any) => {
    const theme = useTheme();
    const [sideNavIsOpen, setSideNavIdOpen] = useState(true);
    useAuthGuard(false);

    const handleDrawerOpen = () => {
        setSideNavIdOpen(true);
    };

    const handleDrawerClose = () => {
        setSideNavIdOpen(false);
    };

    return (
        // <AuthGuard>
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
        // </AuthGuard>
    );


};

export default MainLayout;
