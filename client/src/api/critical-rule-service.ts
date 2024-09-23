import httpClient, { BaseModel } from './http-client';

export enum Action {
    Allow = "allow",
    Block = "block",
    Drop = "drop",
}

export interface CriticalRuleBase {
    protocol?: string;
    srcAddress?: string;
    desAddress?: string;
    srcPort?: number | '';
    dstPort?: number | '';
    action: Action | '';
    title: string;
    description?: string;
    startTime?: Date | '';
    endTime?: Date | '';
}

export interface CriticalRuleCreate extends CriticalRuleBase { }

export interface CriticalRuleUpdate extends Omit<CriticalRuleBase, 'action' | 'title'> {
    action?: Action | '';
    title?: string | '';
}

export interface CriticalRule extends CriticalRuleBase, BaseModel { }

interface GetAllResponse {
    data: CriticalRule[],
    total: number
}

export interface LoginData {
    username: string;
    password: string;
}

export const criticalRuleService = {

    create: async (data: CriticalRuleCreate) => {
        const response = await httpClient.post('/critical-rules', data);
        return response.data;
    },

    update: async (id: number, data: CriticalRuleUpdate) => {
        const response = await httpClient.put(`/critical-rules/${id}`, data);
        return response.data;
    },

    delete: async (id: number) => {
        const response = await httpClient.delete(`/critical-rules/${id}`);
        return response.data;
    },

    deleteMultiple: async (ids: number[]) => {
        const response = await httpClient.delete('/critical-rules/', { data: ids });
        return response.data;
    },

    getAll: async (page = 0, pageSize = 100) => {
        const response = await httpClient.get('/critical-rules', {
            params: { page, pageSize },
        });
        return response.data as GetAllResponse;
    },
};
