import { Box, Container, Stack, Typography } from '@mui/material';
import { DataGrid, GridActionsCellItem, GridColDef } from '@mui/x-data-grid';

import ActionsToolbar from '../components/actions-toolbar';
import DeleteRoundedIcon from '@mui/icons-material/DeleteRounded';
import EditRoundedIcon from '@mui/icons-material/EditRounded';
import React from 'react';
import { useMemo } from 'react';

const CriticalRulesPage: React.FC = () => {

    const criticalRules = [
        {
            "createdAt": "2024-07-10T14:49:44.425132",
            "updatedAt": "2024-07-10T14:49:44.425135",
            "srcAddress": null,
            "srcPort": null,
            "natSrcPort": null,
            "action": "allow",
            "description": "Allow all HTTP requests",
            "endTime": null,
            "protocol": "tcp",
            "id": 1,
            "desAddress": null,
            "desPort": 80,
            "natDesPort": null,
            "title": "Allow HTTP",
            "startTime": "2024-07-10T14:48:21.828000"
        },
        {
            "createdAt": "2024-07-10T14:50:34.755092",
            "updatedAt": "2024-07-10T14:50:34.755094",
            "srcAddress": null,
            "srcPort": null,
            "natSrcPort": null,
            "action": "allow",
            "description": "Allow all HTTPS requests",
            "endTime": null,
            "protocol": "tcp",
            "id": 2,
            "desAddress": null,
            "desPort": 443,
            "natDesPort": null,
            "title": "Allow HTTPS",
            "startTime": "2024-07-10T14:48:21.828000"
        },
    ]

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

    type CriticalRuleRow = (typeof criticalRules)[number];

    return (
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
    );
};

export default CriticalRulesPage;