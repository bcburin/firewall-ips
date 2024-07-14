import * as Yup from 'yup';

import { Action, CriticalRule, CriticalRuleUpdate, criticalRuleService } from '../../../api/critical-rule-service';

import GenericFormModal from '../generic-modal';
import React from 'react';
import { fields } from './constants';

interface UpdateCriticalRuleModalProps {
    open: boolean;
    onClose: () => void;
    onConfirm: () => void;
    criticalRule: CriticalRule;
}

interface CriticalRuleUpdateModelInitialValues extends CriticalRuleUpdate {
    submit?: any,
}

const UpdateCriticalRuleModal: React.FC<UpdateCriticalRuleModalProps> = ({ open, onClose, onConfirm, criticalRule }) => {
    const initialValues: CriticalRuleUpdateModelInitialValues = {
        protocol: criticalRule?.protocol || null,
        src_address: criticalRule?.src_address || null,
        des_address: criticalRule?.des_address || null,
        src_port: criticalRule?.src_port || null,
        des_port: criticalRule?.des_port || null,
        nat_src_port: criticalRule?.nat_src_port || null,
        nat_des_port: criticalRule?.nat_des_port || null,
        action: criticalRule?.action || null,
        title: criticalRule?.title || null,
        description: criticalRule?.description || null,
        start_time: criticalRule?.start_time || null,
        end_time: criticalRule?.end_time || null,
        submit: null,
    };

    const validationSchema = Yup.object({
        title: Yup.string().max(100).nullable(),
        action: Yup.mixed<Action>().oneOf(Object.values(Action)).nullable(),
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

    const handleSubmit = async (values: Record<string, any>) => {
        if (criticalRule) {
            const updateModel: CriticalRuleUpdate = {
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
            }
            await criticalRuleService.update(criticalRule.id, updateModel);
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

export default UpdateCriticalRuleModal;
