import * as Yup from 'yup';

import { Box, Button, Dialog, DialogActions, DialogContent, DialogTitle, FormControlLabel, MenuItem, Stack, Switch, TextField, Typography } from '@mui/material';
import { FormikHelpers, useFormik } from 'formik';

import React from 'react';

export enum FieldType {
    TEXT = 'text',
    DATE = 'date',
    BOOLEAN = 'boolean',
    PASSWORD = 'password',
    NUMBER = 'number',
    TEXTAREA = 'textarea',
    ENUM = 'enum'
}

export interface FieldConfig {
    name: string;
    label: string;
    type?: FieldType;
    options?: { value: any; label: string }[]; // for ENUM type
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

    const renderField = (field: FieldConfig) => {
        switch (field.type) {
            case FieldType.DATE:
                return (
                    <TextField
                        key={field.name}
                        error={!!(formik.touched[field.name] && formik.errors[field.name])}
                        fullWidth
                        helperText={formik.touched[field.name] && formik.errors[field.name]?.toString()}
                        label={field.label}
                        name={field.name}
                        onBlur={formik.handleBlur}
                        onChange={formik.handleChange}
                        type="date"
                        value={formik.values[field.name]}
                        InputLabelProps={{ shrink: true }}
                    />
                );
            case FieldType.BOOLEAN:
                return (
                    <FormControlLabel
                        key={field.name}
                        control={
                            <Switch
                                checked={formik.values[field.name]}
                                onChange={formik.handleChange}
                                name={field.name}
                                color="primary"
                            />
                        }
                        label={field.label}
                    />
                );
            case FieldType.PASSWORD:
                return (
                    <TextField
                        key={field.name}
                        error={!!(formik.touched[field.name] && formik.errors[field.name])}
                        fullWidth
                        helperText={formik.touched[field.name] && formik.errors[field.name]?.toString()}
                        label={field.label}
                        name={field.name}
                        onBlur={formik.handleBlur}
                        onChange={formik.handleChange}
                        type="password"
                        value={formik.values[field.name]}
                    />
                );
            case FieldType.NUMBER:
                return (
                    <TextField
                        key={field.name}
                        error={!!(formik.touched[field.name] && formik.errors[field.name])}
                        fullWidth
                        helperText={formik.touched[field.name] && formik.errors[field.name]?.toString()}
                        label={field.label}
                        name={field.name}
                        onBlur={formik.handleBlur}
                        onChange={formik.handleChange}
                        type="number"
                        value={formik.values[field.name]}
                    />
                );
            case FieldType.TEXTAREA:
                return (
                    <TextField
                        key={field.name}
                        error={!!(formik.touched[field.name] && formik.errors[field.name])}
                        fullWidth
                        helperText={formik.touched[field.name] && formik.errors[field.name]?.toString()}
                        label={field.label}
                        name={field.name}
                        onBlur={formik.handleBlur}
                        onChange={formik.handleChange}
                        multiline
                        rows={4}
                        value={formik.values[field.name]}
                    />
                );
            case FieldType.ENUM:
                return (
                    <TextField
                        key={field.name}
                        error={!!(formik.touched[field.name] && formik.errors[field.name])}
                        fullWidth
                        helperText={formik.touched[field.name] && formik.errors[field.name]?.toString()}
                        label={field.label}
                        name={field.name}
                        onBlur={formik.handleBlur}
                        onChange={formik.handleChange}
                        select
                        value={formik.values[field.name]}
                    >
                        {field.options?.map(option => (
                            <MenuItem key={option.value} value={option.value}>
                                {option.label}
                            </MenuItem>
                        ))}
                    </TextField>
                );
            case FieldType.TEXT:
            default:
                return (
                    <TextField
                        key={field.name}
                        error={!!(formik.touched[field.name] && formik.errors[field.name])}
                        fullWidth
                        helperText={formik.touched[field.name] && formik.errors[field.name]?.toString()}
                        label={field.label}
                        name={field.name}
                        onBlur={formik.handleBlur}
                        onChange={formik.handleChange}
                        type="text"
                        value={formik.values[field.name]}
                    />
                );
        }
    };

    return (
        <Dialog
            open={open}
            onClose={onClose}
            sx={{ maxWidth: '600px', margin: 'auto' }}
            fullWidth
            slotProps={{ backdrop: { onClick: onClose } }}>
            <Box sx={{ width: '90%', margin: 'auto' }}>
                <DialogTitle>{title}</DialogTitle>
                <DialogContent>
                    <form noValidate onSubmit={formik.handleSubmit}>
                        <Stack spacing={3}>
                            {fields.map((field) => renderField(field))}
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
