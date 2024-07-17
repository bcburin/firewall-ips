import { FieldConfig, FieldType } from "../generic-modal";

import { Action } from "../../../api/critical-rule-service";

export const fields: FieldConfig[] = [
    { name: 'title', label: 'Title' },
    {
        name: 'action',
        label: 'Action',
        type: FieldType.ENUM,
        options: [
            {
                value: Action.Allow,
                label: "Allow",
            },
            {
                value: Action.Block,
                label: "Block",
            },
            {
                value: Action.Drop,
                label: "Drop",
            }
        ]
    },
    { name: 'protocol', label: 'Protocol' },
    { name: 'srcAddress', label: 'Src. Address', type: FieldType.NUMBER },
    { name: 'desAddress', label: 'Des. Address', type: FieldType.NUMBER },
    { name: 'srcPort', label: 'Src. Port', type: FieldType.NUMBER },
    { name: 'desPort', label: 'Des. Port', type: FieldType.NUMBER },
    { name: 'startTime', label: 'Start Time', type: FieldType.DATE },
    { name: 'endTime', label: 'End Time', type: FieldType.DATE },
    { name: 'description', label: 'Description', type: FieldType.TEXTAREA },
];