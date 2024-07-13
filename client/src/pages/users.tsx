import { Box, Container, Stack, Typography } from '@mui/material';
import { DataGrid, GridActionsCellItem, GridColDef, GridRowSelectionModel } from '@mui/x-data-grid';
import React, { useCallback, useEffect, useState } from 'react';
import { User, userService } from '../api/user-service';

import ActionsToolbar from '../components/actions-toolbar';
import ConfirmationModal from '../components/modals/confirmation-modal';
import CreateUserModal from '../components/modals/user/user-create';
import DeleteRoundedIcon from '@mui/icons-material/DeleteRounded';
import EditRoundedIcon from '@mui/icons-material/EditRounded';
import ToggleOffRoundedIcon from '@mui/icons-material/ToggleOffRounded';
import ToggleOnRoundedIcon from '@mui/icons-material/ToggleOnRounded';
import UpdateUserModal from '../components/modals/user/user-update';
import { useMemo } from 'react';

const UsersPage: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [selectedRows, setSelectedRows] = useState<GridRowSelectionModel>([])
  const [createModalIsOpen, setCreateModalIsOpen] = useState(false);
  const [updateModalState, setUpdateModalState] = useState<{ isOpen: boolean, user: User | null }>({
    isOpen: false,
    user: null
  });
  const [deleteModalState, setDeleteModalState] = useState<{ isOpen: boolean, user: User | null }>({
    isOpen: false,
    user: null,
  });
  const [totalUsers, setTotalUsers] = useState(0);
  const [paginationModel, setPaginationModel] = React.useState({
    page: 0,
    pageSize: 2,
  });
  const rowCountRef = React.useRef(users.length || 0);

  const rowCount = React.useMemo(() => {
    if (totalUsers !== undefined) {
      rowCountRef.current = totalUsers;
    }
    return rowCountRef.current;
  }, [totalUsers]);

  const getUsersHandler = useCallback(async () => {
    try {
      const getAllResponse = await userService.getAll(paginationModel.page, paginationModel.pageSize);
      setUsers(getAllResponse.data);
      setTotalUsers(getAllResponse.total)
    } catch (e) {
      console.log(e);
    }
  }, [paginationModel]);

  const deleteUserHandler = (userId: number) => async () => {
    try {
      setDeleteModalState({ isOpen: false, user: null });
      await userService.delete(userId);
      await getUsersHandler();
    } catch (e) {
      console.log(e);
    }
  }

  const toggleUserHandler = useCallback((userId: number) => async () => {
    try {
      await userService.toggleActive(userId);
      await getUsersHandler();
    } catch (e) {
      console.log(e);
    }
  }, [getUsersHandler])

  useEffect(() => {
    getUsersHandler();
  }, [getUsersHandler]);

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
          onClick={toggleUserHandler(params.row.id)}
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
          onClick={() => setDeleteModalState({ isOpen: true, user: params.row })}
        />,
        <GridActionsCellItem
          icon={<EditRoundedIcon />}
          label="Edit"
          onClick={() => setUpdateModalState({ isOpen: true, user: params.row })}
        />,
      ],
    },
  ],
    [toggleUserHandler]
  )

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
                        onCreateClick: () => setCreateModalIsOpen(true),
                        onRefreshClick: () => getUsersHandler(),
                        deleteIsDisabled: selectedRows.length === 0,
                      },
                    }}
                    checkboxSelection
                    onRowSelectionModelChange={(newSelectedRows) => setSelectedRows(newSelectedRows)}
                    rowSelectionModel={selectedRows}
                    rowCount={rowCount}
                    pageSizeOptions={[2, 4, 8]}
                    paginationMode='server'
                    paginationModel={paginationModel}
                    onPaginationModelChange={setPaginationModel}
                  />
                </Stack>
              </Stack>
            </Stack>
          </Stack>
        </Container>
      </Box>

      <CreateUserModal
        open={createModalIsOpen}
        onClose={() => setCreateModalIsOpen(false)}
        onConfirm={async () => {
          setCreateModalIsOpen(false);
          await getUsersHandler();
        }}
      />

      <UpdateUserModal
        open={updateModalState.isOpen}
        onClose={() => setUpdateModalState({ isOpen: false, user: null })}
        onConfirm={async () => {
          setUpdateModalState({ isOpen: false, user: null })
          await getUsersHandler();
        }}
        user={updateModalState.user as User}
      />

      <ConfirmationModal
        open={deleteModalState.isOpen}
        onClose={() => setDeleteModalState({ isOpen: false, user: null })}
        onConfirm={deleteUserHandler(deleteModalState.user?.id as number)}
        title="Delete User"
        content={`Are you sure you want to delete user ${deleteModalState.user?.username}?`}
      />
    </>
  );
};

export default UsersPage;