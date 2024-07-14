import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import { Typography } from "@mui/material";

interface ConfirmationModalProps {
    open: boolean;
    onClose: () => void;
    onConfirm: () => void;
    title: string;
    content: string;
    error?: string | null;
}

const ConfirmationModal: React.FC<ConfirmationModalProps> = ({ open, onClose, onConfirm, title, content, error }) => {
    return (
        <Dialog open={open}>
            <DialogTitle>{title}</DialogTitle>
            <DialogContent>
                <p>{content}</p>
                {error && (
                    <Typography color="error" variant="body2">
                        {error}
                    </Typography>
                )}
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Cancel</Button>
                <Button onClick={onConfirm} variant="contained" color="error">
                    Confirm
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default ConfirmationModal;
