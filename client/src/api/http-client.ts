import Cookies from 'js-cookie';
import axios from 'axios';

export interface BaseModel {
    id: number;
    createdAt: Date;
    updatedAT: Date;
}

export const baseURL = 'http://localhost:8000'

const httpClient = axios.create({
    baseURL: baseURL,
    headers: {
        'Content-Type': 'application/json',
    },
});

httpClient.interceptors.request.use((config) => {
    const token = Cookies.get('access_token');
    if (!token) {
        throw new Error('No access token found');
    }
    config.headers.Authorization = `Bearer ${token}`;
    return config;
  });

export default httpClient;
