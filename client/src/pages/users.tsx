import { Box, Container, Stack, Typography } from '@mui/material';
import { DataGrid, GridActionsCellItem, GridColDef } from '@mui/x-data-grid';

import ActionsToolbar from '../components/actions-toolbar';
import DashboardLayout from '../layout/dashboard';
import DeleteRoundedIcon from '@mui/icons-material/DeleteRounded';
import EditRoundedIcon from '@mui/icons-material/EditRounded';
import React from 'react';
import ToggleOffRoundedIcon from '@mui/icons-material/ToggleOffRounded';
import ToggleOnRoundedIcon from '@mui/icons-material/ToggleOnRounded';
import { useMemo } from 'react';

const UsersPage: React.FC = () => {

  const users = [
    {
      username: "admin",
      id: 1,
      firstName: "Administrator",
      active: true,
      loginAttempts: 0,
      updatedAt: "2024-05-25T19:00:15.313570",
      email: "admin@ime.eb.br",
      createdAt: "2024-05-25T19:00:15.313567",
      lastName: "Admin",
      lastLogin: "2024-05-25T19:00:15.313570"
    },
    {
      username: "user1",
      id: 2,
      firstName: "User",
      active: false,
      loginAttempts: 1,
      updatedAt: "2024-07-10T13:08:39.601083",
      email: "user1@domain.com",
      createdAt: "2024-07-10T13:08:39.601078",
      lastName: "One",
      lastLogin: "2024-07-10T13:08:39.601078"
    }
  ]

  const columns = useMemo<GridColDef<UserRow>[]>(() => [
    { field: 'id', headerName: 'Id', width: 50 },
    { field: 'username', headerName: 'Username', width: 100 },
    { field: 'email', headerName: 'E-mail', width: 150 },
    { field: 'firstName', headerName: 'First Name', width: 150 },
    { field: 'lastName', headerName: 'Last Name', width: 150 },
    { field: 'lastLogin', headerName: 'Last Login', width: 200, type: "dateTime", valueGetter: (value) => value && new Date(value) },
    { field: 'loginAttempts', headerName: 'Login Attempts', width: 120 },
    { field: 'updatedAt', headerName: 'Last Update', width: 200, type: "dateTime", valueGetter: (value) => value && new Date(value) },
    { field: 'createdAt', headerName: 'Creation Time', width: 200, type: "dateTime", valueGetter: (value) => value && new Date(value) },
    { field: 'active', headerName: 'Is active?', width: 100, type: "boolean" },
    {
      field: "activationActions",
      type: "actions",
      width: 100,
      getActions: (params) => [
        <GridActionsCellItem
          icon={(params.row.active) ? <ToggleOnRoundedIcon /> : <ToggleOffRoundedIcon />}
          label="Edit"
          onClick={() => { }}
        />,
      ],
    },
    {
      field: "generalActions",
      type: "actions",
      width: 100,
      getActions: (params) => [
        <GridActionsCellItem
          icon={<DeleteRoundedIcon />}
          label="Delete"
          onClick={() => { }}
        />,
        <GridActionsCellItem
          icon={<EditRoundedIcon />}
          label="Edit"
          onClick={() => { }}
        />,
      ],
    },
  ],
    []
  )

  type UserRow = (typeof users)[number];

  return (
    <DashboardLayout>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          py: 8,
        }}
      >
        <Container maxWidth="xl">
          <Stack spacing={3}>
            <Stack direction="row" justifyContent="space-between" spacing={4}>
              <Stack spacing={1}>
                <Typography variant="h4">Users</Typography>
                <Stack alignItems="center" direction="row" spacing={1}>
                  <DataGrid
                    rows={users}
                    columns={columns}
                    slots={{ toolbar: ActionsToolbar }}
                    slotProps={{
                      toolbar: {
                        onCreateClick: () => { },
                        onRefreshClick: () => { },
                        onDeleteClick: () => { },
                        deleteIsDisabled: true,
                      },
                    }}
                    checkboxSelection
                    disableRowSelectionOnClick
                  // onRowSelectionModelChange={(ids) => setSelectedRows(ids)}
                  />
                </Stack>
              </Stack>
            </Stack>
          </Stack>
        </Container>
      </Box>
    </DashboardLayout>
  );
};

export default UsersPage;