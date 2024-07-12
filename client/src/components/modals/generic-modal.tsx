import * as Yup from 'yup';

import { Box, Button, Dialog, DialogActions, DialogContent, DialogTitle, Stack, TextField, Typography } from '@mui/material';
import { FormikHelpers, useFormik } from 'formik';

import React from 'react';

interface FieldConfig {
    name: string;
    label: string;
    type?: string;
}

interface GenericFormModalProps {
    open: boolean;
    onClose: () => void;
    title: string;
    initialValues: Record<string, any>;
    validationSchema: Yup.ObjectSchema<any>;
    onSubmit: (values: any, helpers: FormikHelpers<any>) => Promise<void>;
    fields: FieldConfig[];
}

const GenericFormModal: React.FC<GenericFormModalProps> = ({ open, onClose, title, initialValues, validationSchema, onSubmit, fields }) => {
    const formik = useFormik({
        initialValues,
        validationSchema,
        onSubmit: async (values, helpers) => {
            try {
                await onSubmit(values, helpers);
            } catch (err) {
                helpers.setStatus({ success: false });
                helpers.setErrors({ submit: (err as Error).message });
                helpers.setSubmitting(false);
            }
        },
    });

    return (
        <Dialog open={open} onClose={onClose} sx={{ maxWidth: '600px', margin: 'auto' }} fullWidth>
            <Box sx={{ width: '90%', margin: 'auto' }}>
                <DialogTitle>{title}</DialogTitle>
                <DialogContent>
                    <form noValidate onSubmit={formik.handleSubmit}>
                        <Stack spacing={3}>
                            {fields.map((field) => (
                                <TextField
                                    key={field.name}
                                    error={!!(formik.touched[field.name] && formik.errors[field.name])}
                                    fullWidth
                                    helperText={formik.touched[field.name] && formik.errors[field.name]?.toString()}
                                    label={field.label}
                                    name={field.name}
                                    onBlur={formik.handleBlur}
                                    onChange={formik.handleChange}
                                    type={field.type || 'text'}
                                    value={formik.values[field.name]}
                                />
                            ))}
                        </Stack>
                        {formik.errors.submit && (
                            <Typography color="error" sx={{ mt: 3 }} variant="body2">
                                {formik.errors.submit?.toString()}
                            </Typography>
                        )}
                        <DialogActions>
                            <Button onClick={onClose}>Cancel</Button>
                            <Button
                                variant="contained"
                                color="primary"
                                type="submit"
                            >
                                {title}
                            </Button>
                        </DialogActions>
                    </form>
                </DialogContent>
            </Box>
        </Dialog>
    );
};

export default GenericFormModal;
