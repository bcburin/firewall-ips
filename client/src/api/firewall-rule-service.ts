import httpClient, { BaseModel } from './http-client';

export enum Action {
    Allow = "allow",
    Block = "block",
    Drop = "drop",
}

export interface FirewallRuleBase {
    protocol?: string | null;
    srcAddress?: string | null;
    desAddress?: string | null;
    srcPort?: number | null;
    desPort?: number | null;
    action: Action;
}

export interface FirewallRuleCreate extends FirewallRuleBase { }

export interface FirewallRuleUpdate extends Omit<FirewallRuleBase, 'action' | 'title'> {
    action?: Action | null;
    title?: string | null;
}

export interface FirewallRule extends FirewallRuleBase, BaseModel { }

interface GetAllResponse {
    data: FirewallRule[],
    total: number
}

export interface LoginData {
    username: string;
    password: string;
}

export const firewallRuleService = {

    getAll: async (page = 0, pageSize = 100) => {
        const response = await httpClient.get('/firewall-rules', {
            params: { page, pageSize },
        });
        return response.data as GetAllResponse;
    },
};
