import { Box, Button, SvgIcon, styled } from "@mui/material";
import {
    GridToolbarColumnsButton,
    GridToolbarContainer,
    GridToolbarDensitySelector,
    GridToolbarExport,
    GridToolbarFilterButton,
} from "@mui/x-data-grid";

import AddBoxRoundedIcon from "@mui/icons-material/AddBoxRounded";
import CachedRoundedIcon from "@mui/icons-material/CachedRounded";
import DeleteRoundedIcon from "@mui/icons-material/DeleteRounded";

const StyledButton = styled(Button)(({ theme }) => ({
    marginRight: theme.spacing(1),
}));

interface ActionsToolbarProps {
    onCreateClick?: () => void,
    onRefreshClick?: () => void,
    onDeleteClick?: () => void,
    deleteIsDisabled: boolean
}

const ActionsToolbar: any = ({  // TODO: fix actions toolbar type
    onCreateClick,
    onRefreshClick,
    onDeleteClick,
    deleteIsDisabled,
}: ActionsToolbarProps) => {
    return (
        <GridToolbarContainer>
            <GridToolbarColumnsButton />
            <GridToolbarFilterButton />
            <GridToolbarDensitySelector />
            <GridToolbarExport />
            <Box sx={{ flexGrow: 1 }} />
            <Box>
                {onCreateClick && (
                    <StyledButton
                        startIcon={
                            <SvgIcon fontSize="small">
                                <AddBoxRoundedIcon />
                            </SvgIcon>
                        }
                        variant="contained"
                        onClick={onCreateClick}
                    >
                        Create
                    </StyledButton>
                )}
                {onRefreshClick && (
                    <StyledButton
                        startIcon={
                            <SvgIcon fontSize="small">
                                <CachedRoundedIcon />
                            </SvgIcon>
                        }
                        variant="contained"
                        onClick={onRefreshClick}
                    >
                        Refresh
                    </StyledButton>
                )}
                {onDeleteClick && (
                    <StyledButton
                        startIcon={
                            <SvgIcon fontSize="small">
                                <DeleteRoundedIcon />
                            </SvgIcon>
                        }
                        variant="contained"
                        onClick={onDeleteClick}
                        disabled={deleteIsDisabled}
                    >
                        Delete
                    </StyledButton>
                )}
            </Box>
        </GridToolbarContainer>
    );
};

export default ActionsToolbar;
