import Box from '@mui/material/Box';
import PropTypes from "prop-types";
import SideNav from '../components/sidenav';
import TopBar from '../components/topbar';
import { useState } from 'react'
import { useTheme } from '@mui/material';

const drawerWidth = 240;

const DashboardLayout = ({ children }: any) => {
    const theme = useTheme();
    const [sideNavIsOpen, setSideNavIdOpen] = useState(true);

    const handleDrawerOpen = () => {
        setSideNavIdOpen(true);
    };

    const handleDrawerClose = () => {
        setSideNavIdOpen(false);
    };

    return (
        <Box sx={{ display: 'flex' }}>
            <TopBar open={sideNavIsOpen} onOpen={handleDrawerOpen} />
            <SideNav open={sideNavIsOpen} onClose={handleDrawerClose} />
            <Box
                component="main"
                sx={{
                    flexGrow: 1,
                    p: 3,
                    mt: '64px', // Adjust this value to the height of your TopBar
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

DashboardLayout.prototypes = {
    children: PropTypes.node,
};

export default DashboardLayout;
