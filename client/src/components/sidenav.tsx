import * as React from 'react';

import { styled, useTheme } from '@mui/material/styles';

import AssessmentRoundedIcon from '@mui/icons-material/AssessmentRounded';
import Box from '@mui/material/Box';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import CssBaseline from '@mui/material/CssBaseline';
import Drawer from '@mui/material/Drawer';
import GavelRoundedIcon from '@mui/icons-material/GavelRounded';
import IconButton from '@mui/material/IconButton';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import PersonRoundedIcon from '@mui/icons-material/PersonRounded';
import SettingsRoundedIcon from '@mui/icons-material/SettingsRounded';
import { SvgIconComponent } from '@mui/icons-material';
import WhatshotRoundedIcon from '@mui/icons-material/WhatshotRounded';

const drawerWidth = 240;

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: 'flex-end',
}));

interface SideNavItemProps {
  text: string;
  color: string;
  Icon: SvgIconComponent;
}

const SideNavItem: React.FC<SideNavItemProps> = ({ text, color, Icon }) => {
  return (
    <ListItem disablePadding>
      <ListItemButton>
        <ListItemIcon sx={{ color }}>
          <Icon />
        </ListItemIcon>
        <ListItemText primary={text} />
      </ListItemButton>
    </ListItem>
  );
};

interface SideNavProps {
  open: boolean,
  onClose: () => void
}

const SideNav: React.FC<SideNavProps> = ({ open, onClose }) => {
  const theme = useTheme();

  const pageIcons = [
    {
      text: "Dashboard",
      Icon: AssessmentRoundedIcon
    },
    {
      text: "Critical Rules",
      Icon: GavelRoundedIcon
    },
    {
      text: "Firewall Rules",
      Icon: WhatshotRoundedIcon
    },
    {
      text: "Users",
      Icon: PersonRoundedIcon
    },
    {
      text: "Configurations",
      Icon: SettingsRoundedIcon
    }
  ]

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
            backgroundColor: theme.palette.primary.main,
            color: theme.palette.common.white,
          },
        }}
        variant="persistent"
        anchor="left"
        open={open}
      >
        <DrawerHeader>
          <IconButton onClick={onClose} sx={{ color: theme.palette.common.white }}>
            {theme.direction === 'ltr' ? <ChevronLeftIcon /> : <ChevronRightIcon />}
          </IconButton>
        </DrawerHeader>
        <List>
          {pageIcons.map(({ text, Icon }, index) =>
            <SideNavItem key={index} text={text} color={theme.palette.common.white} Icon={Icon} />
          )}
        </List>
      </Drawer>
    </Box>
  );
};


export default SideNav;
