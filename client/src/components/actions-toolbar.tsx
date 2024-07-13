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
    '& .MuiButton-startIcon': {
        marginRight: 0,
    },
    '&:hover .MuiButton-startIcon': {
        marginRight: theme.spacing(1),
    },
    '&:hover .button-text': {
        display: 'inline',
    },
    '& .button-text': {
        display: 'none',
    },
}));

interface ActionsToolbarProps {
    onCreateClick?: () => void;
    onRefreshClick?: () => void;
    onDeleteClick?: () => void;
    deleteIsDisabled: boolean;
}

const ActionsToolbar: any = ({
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
                        <span className="button-text">Create</span>
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
                        <span className="button-text">Refresh</span>
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
                        <span className="button-text">Delete</span>
                    </StyledButton>
                )}
            </Box>
        </GridToolbarContainer>
    );
};

export default ActionsToolbar;
