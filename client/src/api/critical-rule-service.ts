import httpClient, { BaseModel } from './http-client';

export enum Action {
    Allow = "allow",
    Block = "block",
    Drop = "drop",
}

export interface CriticalRuleBase {
    protocol?: string | null;
    src_address?: string | null;
    des_address?: string | null;
    src_port?: number | null;
    des_port?: number | null;
    nat_src_port?: number | null;
    nat_des_port?: number | null;
    action: Action;
    title: string;
    description?: string | null;
    start_time?: Date | null;
    end_time?: Date | null;
}

export interface CriticalRuleCreate extends CriticalRuleBase { }

export interface CriticalRuleUpdate extends Omit<CriticalRuleBase, 'action' | 'title'> {
    action?: Action | null;
    title?: string | null;
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
