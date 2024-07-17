import { Box, Container, Stack, Typography } from '@mui/material';
import { DataGrid, GridActionsCellItem, GridColDef, GridRowSelectionModel } from '@mui/x-data-grid';
import { PaginatedResponse, usePaginatedData } from '../hooks/paginated-data';
import React, { useCallback, useMemo, useState } from 'react';
import { User, userService } from '../api/user-service';

import ActionsToolbar from '../components/actions-toolbar';
import ConfirmationModal from '../components/modals/confirmation-modal';
import CreateUserModal from '../components/modals/user/user-create';
import DeleteRoundedIcon from '@mui/icons-material/DeleteRounded';
import EditRoundedIcon from '@mui/icons-material/EditRounded';
import ToggleOffRoundedIcon from '@mui/icons-material/ToggleOffRounded';
import ToggleOnRoundedIcon from '@mui/icons-material/ToggleOnRounded';
import UpdateUserModal from '../components/modals/user/user-update';
import { useModalState } from '../hooks/modals';
import { useUpdateModalState } from '../hooks/modals';

const fetchUsers = async (page: number, pageSize: number): Promise<PaginatedResponse<User>> => {
  return await userService.getAll(page, pageSize);
};

const UsersPage: React.FC = () => {
  const { data: users, total: totalUsers, paginationModel, setPaginationModel, getData: getUsers, loading } = usePaginatedData<User>(fetchUsers);
  const [selectedRows, setSelectedRows] = useState<GridRowSelectionModel>([]);

  const createModal = useModalState();
  const updateModal = useUpdateModalState<User | null>();
  const deleteModal = useUpdateModalState<User | null>();

  const deleteUserHandler = async (userId: number) => {
    try {
      deleteModal.close();
      await userService.delete(userId);
      await getUsers();
    } catch (e) {
      console.log(e);
    }
  }

  const toggleUserHandler = useCallback(async (userId: number) => {
    try {
      await userService.toggleActive(userId);
      await getUsers();
    } catch (e) {
      console.log(e);
    }
  }, [getUsers])

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
          label="Toggle"
          onClick={() => toggleUserHandler(params.row.id)}
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
          onClick={() => deleteModal.open(params.row)}
        />,
        <GridActionsCellItem
          icon={<EditRoundedIcon />}
          label="Edit"
          onClick={() => updateModal.open(params.row)}
        />,
      ],
    },
  ], [toggleUserHandler, deleteModal, updateModal]);

  type UserRow = (typeof users)[number];

  return (
    <>
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
                        onCreateClick: createModal.open,
                        onRefreshClick: getUsers,
                        deleteIsDisabled: selectedRows.length === 0,
                      },
                    }}
                    checkboxSelection
                    disableMultipleRowSelection
                    onRowSelectionModelChange={(newSelectedRows) => setSelectedRows(newSelectedRows)}
                    rowSelectionModel={selectedRows}
                    rowCount={totalUsers}
                    pageSizeOptions={[25, 50, 100]}
                    paginationMode='server'
                    paginationModel={paginationModel}
                    onPaginationModelChange={setPaginationModel}
                    loading={loading}
                  />
                </Stack>
              </Stack>
            </Stack>
          </Stack>
        </Container>
      </Box>

      <CreateUserModal
        open={createModal.isOpen}
        onClose={createModal.close}
        onConfirm={async () => {
          createModal.close();
          await getUsers();
        }}
      />

      <UpdateUserModal
        open={updateModal.state.isOpen}
        onClose={updateModal.close}
        onConfirm={async () => {
          updateModal.close();
          await getUsers();
        }}
        user={updateModal.state.data as User}
      />

      <ConfirmationModal
        open={deleteModal.state.isOpen}
        onClose={deleteModal.close}
        onConfirm={() => deleteUserHandler(deleteModal.state.data?.id as number)}
        title="Delete User"
        content={`Are you sure you want to delete user ${deleteModal.state.data?.username}?`}
      />
    </>
  );
};

export default UsersPage;
