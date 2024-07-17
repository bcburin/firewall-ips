import * as Yup from 'yup';

import { Action, CriticalRuleCreate, criticalRuleService } from '../../../api/critical-rule-service';

import GenericFormModal from '../generic-modal';
import React from 'react';
import { fields } from './constants';

interface CreateCriticalRuleModalProps {
    open: boolean;
    onClose: () => void;
    onConfirm: () => void;
}

interface CriticalRuleCreateModelInitialValues extends CriticalRuleCreate {
    submit?: any,
}

const CreateCriticalRuleModal: React.FC<CreateCriticalRuleModalProps> = ({ open, onClose, onConfirm }) => {
    const initialValues: CriticalRuleCreateModelInitialValues = {
        protocol: "",
        srcAddress: "",
        desAddress: "",
        srcPort: "",
        desPort: "",
        action: Action.Allow,
        title: "",
        description: "",
        startTime: "",
        endTime: "",
        submit: "",
    };

    const validationSchema = Yup.object({
        title: Yup.string().max(100).required(),
        action: Yup.mixed<Action>().oneOf(Object.values(Action)).required(),
        protocol: Yup.string().max(250).nullable(),
        srcAddress: Yup.string().max(250).nullable(),
        desAddress: Yup.string().max(250).nullable(),
        srcPort: Yup.number().min(0).max(65535).nullable(),
        desPort: Yup.number().min(0).max(65535).nullable(),
        startTime: Yup.date().default(new Date()).nullable(),
        endTime: Yup.date().nullable(),
        description: Yup.string().max(400).nullable(),
    });



    const handleSubmit = async (values: typeof initialValues) => {
        const createModel: CriticalRuleCreate = {
            protocol: values.protocol,
            srcAddress: values.srcAddress,
            desAddress: values.desAddress,
            srcPort: values.srcPort,
            desPort: values.desPort,
            action: values.action,
            title: values.title,
            description: values.description,
            startTime: values.startTime,
            endTime: values.endTime,
        };
        await criticalRuleService.create(createModel);
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

export default CreateCriticalRuleModal;
