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
    { name: 'src_address', label: 'Src. Address', type: FieldType.NUMBER },
    { name: 'des_address', label: 'Des. Address', type: FieldType.NUMBER },
    { name: 'src_port', label: 'Src. Port', type: FieldType.NUMBER },
    { name: 'des_port', label: 'Des. Port', type: FieldType.NUMBER },
    { name: 'nat_src_port', label: 'NAT Src. Port', type: FieldType.NUMBER },
    { name: 'nat_des_port', label: 'NAT Des. Port', type: FieldType.NUMBER },
    { name: 'start_time', label: 'Start Time', type: FieldType.DATE },
    { name: 'end_time', label: 'End Time', type: FieldType.DATE },
    { name: 'description', label: 'Description', type: FieldType.TEXTAREA },
];