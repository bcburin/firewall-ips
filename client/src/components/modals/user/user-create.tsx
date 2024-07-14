import * as Yup from 'yup';

import GenericFormModal, { FieldType } from '../generic-modal';
import { UserCreate, userService } from '../../../api/user-service';

import React from 'react';

interface CreateUserModalProps {
    open: boolean;
    onClose: () => void;
    onConfirm: () => void;
}

const CreateUserModal: React.FC<CreateUserModalProps> = ({ open, onClose, onConfirm }) => {
    const initialValues = {
        email: "",
        username: "",
        firstName: "",
        lastName: "",
        password: "",
        submit: null,
    };

    const validationSchema = Yup.object({
        email: Yup.string().email("Must be a valid email").max(255).required("Email is required"),
        username: Yup.string().max(255).required("Username is required"),
        firstName: Yup.string().max(255).required("First name is required"),
        lastName: Yup.string().max(255).required("Last name is required"),
        password: Yup.string().max(255).required("Password is required"),
    });

    const fields = [
        { name: 'firstName', label: 'First Name' },
        { name: 'lastName', label: 'Last Name' },
        { name: 'email', label: 'Email Address' },
        { name: 'username', label: 'Username' },
        { name: 'password', label: 'Password', type: FieldType.PASSWORD },
    ];

    const handleSubmit = async (values: typeof initialValues) => {
        const userCreate: UserCreate = {
            password: values.password,
            email: values.email,
            username: values.username,
            firstName: values.firstName,
            lastName: values.lastName
        }
        await userService.create(userCreate);
        onConfirm();
    };

    return (
        <GenericFormModal
            open={open}
            onClose={onClose}
            title="Create"
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={handleSubmit}
            fields={fields}
        />
    );
};

export default CreateUserModal;
