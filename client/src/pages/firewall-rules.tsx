import { Box, Container, Stack, Typography } from '@mui/material';
import { DataGrid, GridColDef, GridRowSelectionModel } from '@mui/x-data-grid';
import { FirewallRule, firewallRuleService } from '../api/firewall-rule-service';
import { PaginatedResponse, usePaginatedData } from '../hooks/paginated-data';
import React, { useMemo, useState } from 'react';

import ActionsToolbar from '../components/actions-toolbar';

const fetchCRs = async (page: number, pageSize: number): Promise<PaginatedResponse<FirewallRule>> => {
    return await firewallRuleService.getAll(page, pageSize);
};

const FirewallRulesPage: React.FC = () => {
    const { data: firewallRules, total: totalCRs, paginationModel, setPaginationModel, getData, loading } = usePaginatedData<FirewallRule>(fetchCRs);
    const [selectedRows, setSelectedRows] = useState<GridRowSelectionModel>([]);

    const columns = useMemo<GridColDef<FirewallRuleRow>[]>(() => [
        { field: 'id', headerName: 'Id', width: 50 },
        { field: 'action', headerName: 'Action', width: 100 },
        { field: 'protocol', headerName: 'Protocol', width: 80 },
        { field: 'srcAddress', headerName: 'Src Address', width: 120 },
        { field: 'dstAddress', headerName: 'Dest Address', width: 120 },
        { field: 'srcPort', headerName: 'Src Port', width: 100 },
        { field: 'dstPort', headerName: 'Dest Port', width: 100 },
        { field: 'natSrcPort', headerName: 'NAT Src Port', width: 100 },
        { field: 'natdstPort', headerName: 'NAT Dest Port', width: 100 },
        { field: 'updatedAt', headerName: 'Last Update', width: 200, type: "dateTime", valueGetter: (value) => value && new Date(value) },
        { field: 'createdAt', headerName: 'Creation Time', width: 200, type: "dateTime", valueGetter: (value) => value && new Date(value) },
    ],
        []
    )

    type FirewallRuleRow = (typeof firewallRules)[number];

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
                                <Typography variant="h4">Firewall Rules</Typography>
                                <Stack alignItems="center" direction="row" spacing={1}>
                                    <DataGrid
                                        rows={firewallRules}
                                        columns={columns}
                                        initialState={{
                                            columns: {
                                                columnVisibilityModel: {
                                                    natSrcPort: false,
                                                    natdstPort: false,
                                                    startTime: false,
                                                    endTime: false,
                                                    createdAt: false,
                                                    srcAddress: false,
                                                    desAddress: false,
                                                    srcPort: false,
                                                }
                                            }
                                        }}
                                        slots={{ toolbar: ActionsToolbar }}
                                        slotProps={{
                                            toolbar: {
                                                onRefreshClick: getData,
                                                deleteIsDisabled: selectedRows.length === 0,
                                            },
                                        }}
                                        onRowSelectionModelChange={(newSelectedRows) => setSelectedRows(newSelectedRows)}
                                        rowSelectionModel={selectedRows}
                                        rowCount={totalCRs}
                                        pageSizeOptions={[25, 50, 100]}
                                        paginationMode='server'
                                        paginationModel={paginationModel}
                                        onPaginationModelChange={setPaginationModel}
                                        loading={loading}
                                        disableRowSelectionOnClick
                                        disableMultipleRowSelection
                                    />
                                </Stack>
                            </Stack>
                        </Stack>
                    </Stack>
                </Container>
            </Box>
        </>
    );
};

export default FirewallRulesPage;