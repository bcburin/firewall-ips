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
        protocol: criticalRule?.protocol || "",
        srcAddress: criticalRule?.srcAddress || "",
        desAddress: criticalRule?.desAddress || "",
        srcPort: criticalRule?.srcPort || "",
        dstPort: criticalRule?.dstPort || "",
        action: criticalRule?.action || "",
        title: criticalRule?.title || "",
        description: criticalRule?.description || "",
        startTime: criticalRule?.startTime || "",
        endTime: criticalRule?.endTime || "",
        submit: "",
    };

    const validationSchema = Yup.object({
        title: Yup.string().max(100).nullable(),
        action: Yup.mixed<Action>().oneOf(Object.values(Action)).nullable(),
        protocol: Yup.string().max(250).nullable(),
        srcAddress: Yup.string().max(250).nullable(),
        desAddress: Yup.string().max(250).nullable(),
        srcPort: Yup.number().min(0).max(65535).nullable(),
        dstPort: Yup.number().min(0).max(65535).nullable(),
        startTime: Yup.date().default(new Date()).nullable(),
        endTime: Yup.date().nullable(),
        description: Yup.string().max(400).nullable(),
    });

    const handleSubmit = async (values: Record<string, any>) => {
        if (criticalRule) {
            const updateModel: CriticalRuleUpdate = {
                protocol: values.protocol,
                srcAddress: values.srcAddress,
                desAddress: values.desAddress,
                srcPort: values.srcPort,
                dstPort: values.dstPort,
                action: values.action,
                title: values.title,
                description: values.description,
                startTime: values.startTime,
                endTime: values.endTime,
            }
            try {
                await criticalRuleService.update(criticalRule.id, updateModel);
                onConfirm();
            } catch (err) {
            }
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
