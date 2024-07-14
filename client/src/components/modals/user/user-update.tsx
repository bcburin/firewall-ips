import * as Yup from 'yup';

import { User, UserUpdate, userService } from '../../../api/user-service';

import GenericFormModal from '../generic-modal';
import React from 'react';

interface UpdateUserModalProps {
    open: boolean;
    onClose: () => void;
    onConfirm: () => void;
    user: User;
}

const UpdateUserModal: React.FC<UpdateUserModalProps> = ({ open, onClose, onConfirm, user }) => {
    const initialValues = {
        username: user?.username || "",
        email: user?.email || "",
        firstName: user?.firstName || "",
        lastName: user?.lastName || "",
        submit: null,
    };

    const validationSchema = Yup.object({
        username: Yup.string().max(255),
        email: Yup.string().email("Must be a valid email").max(255),
        firstName: Yup.string().max(255),
        lastName: Yup.string().max(255),
    });

    const fields = [
        { name: 'username', label: 'Username' },
        { name: 'firstName', label: 'First Name' },
        { name: 'lastName', label: 'Last Name' },
        { name: 'email', label: 'Email Address' },
    ];

    const handleSubmit = async (values: Record<string, any>) => {
        if (user) {
            const userUpdate: UserUpdate = {
                email: values.email,
                username: values.username,
                firstName: values.firstName,
                lastName: values.lastName
            }
            await userService.update(user.id, userUpdate);
            onConfirm();
        }
    };

    return (
        <GenericFormModal
            open={open}
            onClose={onClose}
            title="Update"
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={handleSubmit}
            fields={fields}
        />
    );
};

export default UpdateUserModal;
