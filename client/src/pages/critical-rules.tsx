import { Box, Container, Stack, Typography } from '@mui/material';
import { CriticalRule, criticalRuleService } from '../api/critical-rule-service';
import { DataGrid, GridActionsCellItem, GridColDef, GridRowSelectionModel } from '@mui/x-data-grid';
import { PaginatedResponse, usePaginatedData } from '../hooks/paginated-data';
import React, { useState } from 'react';
import { useModalState, useUpdateModalState } from '../hooks/modals';

import ActionsToolbar from '../components/actions-toolbar';
import ConfirmationModal from '../components/modals/confirmation-modal';
import CreateCriticalRuleModal from '../components/modals/critical-rule/critical-rule-create';
import DeleteRoundedIcon from '@mui/icons-material/DeleteRounded';
import EditRoundedIcon from '@mui/icons-material/EditRounded';
import UpdateCriticalRuleModal from '../components/modals/critical-rule/critical-rule-update';
import { useMemo } from 'react';

const fetchCRs = async (page: number, pageSize: number): Promise<PaginatedResponse<CriticalRule>> => {
    return await criticalRuleService.getAll(page, pageSize);
};

const CriticalRulesPage: React.FC = () => {
    const { data: criticalRules, total: totalCRs, paginationModel, setPaginationModel, getData, loading } = usePaginatedData<CriticalRule>(fetchCRs);
    const [selectedRows, setSelectedRows] = useState<GridRowSelectionModel>([]);

    const createModal = useModalState();
    const updateModal = useUpdateModalState<CriticalRule | null>();
    const deleteModal = useUpdateModalState<CriticalRule | null>();
    const deleteMultipleModal = useUpdateModalState<null>();

    const deleteCriticalRuleHandler = async (id: number) => {
        try {
            await criticalRuleService.delete(id);
            deleteModal.close();
        } catch (e: any) {
            const message = e?.response?.data?.detail ?? e?.message ?? "Something went wrong";
            deleteModal.setError(message);
        }
        try {
            await getData();
        } catch (e) {
            console.log(e);
        }
    }

    const deleteMultipleCriticalRulesHandler = async (ids: number[]) => {
        try {
            await criticalRuleService.deleteMultiple(ids);
            deleteMultipleModal.close();
        } catch (e: any) {
            const message = e?.response?.data?.detail ?? e?.message ?? "Something went wrong";
            deleteMultipleModal.setError(message);
        }
        try {
            await getData();
        } catch (e) {
            console.log(e);
        }
    }

    const columns = useMemo<GridColDef<CriticalRuleRow>[]>(() => [
        { field: 'id', headerName: 'Id', width: 50 },
        { field: 'title', headerName: 'Title', width: 150 },
        { field: 'action', headerName: 'Action', width: 100 },
        { field: 'protocol', headerName: 'Protocol', width: 80 },
        { field: 'srcAddress', headerName: 'Src Address', width: 100 },
        { field: 'desAddress', headerName: 'Dest Address', width: 100 },
        { field: 'srcPort', headerName: 'Src Port', width: 100 },
        { field: 'desPort', headerName: 'Dest Port', width: 100 },
        { field: 'natSrcPort', headerName: 'NAT Src Port', width: 100 },
        { field: 'natDesPort', headerName: 'NAT Dest Port', width: 100 },
        { field: 'startTime', headerName: 'Start Time', width: 200, type: "dateTime", valueGetter: (value) => value && new Date(value) },
        { field: 'endTime', headerName: 'End Time', width: 200, type: "dateTime", valueGetter: (value) => value && new Date(value) },
        { field: 'updatedAt', headerName: 'Last Update', width: 200, type: "dateTime", valueGetter: (value) => value && new Date(value) },
        { field: 'createdAt', headerName: 'Creation Time', width: 200, type: "dateTime", valueGetter: (value) => value && new Date(value) },
        {
            field: "actions",
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
    ],
        [updateModal, deleteModal]
    )

    type CriticalRuleRow = (typeof criticalRules)[number];

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
                                <Typography variant="h4">Critical Rules</Typography>
                                <Stack alignItems="center" direction="row" spacing={1}>
                                    <DataGrid
                                        rows={criticalRules}
                                        columns={columns}
                                        initialState={{
                                            columns: {
                                                columnVisibilityModel: {
                                                    natSrcPort: false,
                                                    natDesPort: false,
                                                    startTime: false,
                                                    endTime: false,
                                                    createdAt: false,
                                                }
                                            }
                                        }}
                                        slots={{ toolbar: ActionsToolbar }}
                                        slotProps={{
                                            toolbar: {
                                                onCreateClick: createModal.open,
                                                onRefreshClick: getData,
                                                onDeleteClick: () => deleteMultipleModal.open(null),
                                                deleteIsDisabled: selectedRows.length === 0,
                                            },
                                        }}
                                        checkboxSelection
                                        onRowSelectionModelChange={(newSelectedRows) => setSelectedRows(newSelectedRows)}
                                        rowSelectionModel={selectedRows}
                                        rowCount={totalCRs}
                                        pageSizeOptions={[50, 100, 150]}
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

            <CreateCriticalRuleModal
                open={createModal.isOpen}
                onClose={createModal.close}
                onConfirm={async () => {
                    createModal.close();
                    await getData();
                }}
            />

            <UpdateCriticalRuleModal
                open={updateModal.state.isOpen}
                onClose={updateModal.close}
                onConfirm={async () => {
                    updateModal.close();
                    await getData();
                }}
                criticalRule={updateModal.state.data as CriticalRule}
            />

            <ConfirmationModal
                open={deleteModal.state.isOpen}
                onClose={deleteModal.close}
                onConfirm={() => deleteCriticalRuleHandler(deleteModal.state.data?.id as number)}
                title="Delete User"
                content={`Are you sure you want to delete rule "${deleteModal.state.data?.title}"?`}
                error={deleteModal.state.error}
            />

            <ConfirmationModal
                open={deleteMultipleModal.state.isOpen}
                onClose={deleteMultipleModal.close}
                onConfirm={() => deleteMultipleCriticalRulesHandler(selectedRows as number[])}
                title="Delete User"
                content={`Are you sure you want to delete these rules"?`}
                error={deleteModal.state.error}
            />
        </>
    );
};

export default CriticalRulesPage;