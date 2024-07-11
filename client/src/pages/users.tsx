import { Box, Container, Stack, Typography } from '@mui/material';
import { DataGrid, GridActionsCellItem, GridColDef } from '@mui/x-data-grid';
import React, { useEffect, useState } from 'react';
import { User, userService } from '../api/user-service';

import ActionsToolbar from '../components/actions-toolbar';
import DeleteRoundedIcon from '@mui/icons-material/DeleteRounded';
import EditRoundedIcon from '@mui/icons-material/EditRounded';
import MainLayout from '../layout/main';
import ToggleOffRoundedIcon from '@mui/icons-material/ToggleOffRounded';
import ToggleOnRoundedIcon from '@mui/icons-material/ToggleOnRounded';
import { useMemo } from 'react';

const UsersPage: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);

  const getUsersHandler = async () => {
    try {
      const fetchedUsers = await userService.getAll();
      setUsers(fetchedUsers);
    } catch (e) {
      console.log(e);
    }
  }

  useEffect(() => {
    getUsersHandler();
  }, []);

  const columns = useMemo<GridColDef<UserRow>[]>(() => [
    { field: 'id', headerName: 'Id', width: 50 },
    { field: 'username', headerName: 'Username', width: 100 },
    { field: 'email', headerName: 'E-mail', width: 150 },
    { field: 'firstName', headerName: 'First Name', width: 150 },
    { field: 'lastName', headerName: 'Last Name', width: 150 },
    { field: 'lastLogin', headerName: 'Last Login', width: 200, type: "dateTime", valueGetter: (value) => value && new Date(value) },
    { field: 'loginAttempts', headerName: 'Login Attempts', width: 120, type: "number" },
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
    <MainLayout>
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
                    initialState={{
                      columns: {
                        columnVisibilityModel: {
                          createdAt: false,
                          updatedAt: false,
                        }
                      }
                    }}
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
                  // disableRowSelectionOnClick
                  // onRowSelectionModelChange={(ids) => setSelectedRows(ids)}
                  />
                </Stack>
              </Stack>
            </Stack>
          </Stack>
        </Container>
      </Box>
    </MainLayout>
  );
};

export default UsersPage;