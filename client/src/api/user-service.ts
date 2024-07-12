import httpClient, { BaseModel, baseURL } from './http-client';

import axios from 'axios';

export interface UserBase {
    username: string;
    email: string;
    firstName: string;
    lastName: string;
    active: boolean;
}

export interface UserCreate extends Omit<UserBase, 'active'> {
    password: string;
    active?: boolean;
}

export interface UserUpdate {
    username?: string;
    email?: string;
    firstName?: string;
    lastName?: string;
    password?: string;
    active?: boolean;
}

export interface User extends UserBase, BaseModel {
    lastLogin: Date;
    loginAttempts: number;
}

export interface LoginData {
    username: string;
    password: string;
}

export const userService = {
    login: async (data: LoginData) => {
        const formData = new FormData();
        formData.append("grant_type", "password");
        formData.append("username", data.username);
        formData.append("password", data.password);
        const config = {
            headers: {
                "content-type": "multipart/form-data",
            },
        };
        const response = await axios.post(`${baseURL}/users/login`, formData, config);
        return response.data;
    },

    getMe: async () => {
        const response = await httpClient.get('/users/me');
        return response.data;
    },

    create: async (data: UserCreate) => {
        const response = await httpClient.post('/users', data);
        return response.data;
    },

    update: async (id: number, data: UserUpdate) => {
        const response = await httpClient.put(`/users/${id}`, data);
        return response.data;
    },

    toggleActive: async (id: number) => {
        const response = await httpClient.put(`/users/${id}/toggle`);
        return response.data;
    },

    delete: async (id: number) => {
        const response = await httpClient.delete(`/users/${id}`);
        return response.data;
    },

    getAll: async (skip = 0, limit = 100) => {
        const response = await httpClient.get('/users', {
            params: { skip, limit },
        });
        return response.data;
    },
};
