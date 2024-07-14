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
        protocol: null,
        src_address: null,
        des_address: null,
        src_port: null,
        des_port: null,
        nat_src_port: null,
        nat_des_port: null,
        action: Action.Allow,
        title: "",
        description: null,
        start_time: null,
        end_time: null,
        submit: null,
    };

    const validationSchema = Yup.object({
        title: Yup.string().max(100).required(),
        action: Yup.mixed<Action>().oneOf(Object.values(Action)).required(),
        protocol: Yup.string().max(250).nullable(),
        src_address: Yup.string().max(250).nullable(),
        des_address: Yup.string().max(250).nullable(),
        src_port: Yup.number().min(0).max(65535).nullable(),
        des_port: Yup.number().min(0).max(65535).nullable(),
        nat_src_port: Yup.number().min(0).max(65535).nullable(),
        nat_des_port: Yup.number().min(0).max(65535).nullable(),
        start_time: Yup.date().default(new Date()).nullable(),
        end_date: Yup.date().nullable(),
        description: Yup.string().max(400).nullable(),
    });



    const handleSubmit = async (values: typeof initialValues) => {
        const createModel: CriticalRuleCreate = {
            protocol: values.protocol,
            src_address: values.src_address,
            des_address: values.des_address,
            src_port: values.src_port,
            des_port: values.des_port,
            nat_src_port: values.nat_src_port,
            nat_des_port: values.nat_des_port,
            action: values.action,
            title: values.title,
            description: values.description,
            start_time: values.start_time,
            end_time: values.end_time,
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
