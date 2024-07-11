import { LoginData, User, userService } from '../api/user-service';
import { PayloadAction, createAsyncThunk, createSlice } from '@reduxjs/toolkit';

import Cookies from 'js-cookie';

interface AuthState {
    isAuthenticated: boolean;
    user: User | null;
    loading: boolean;
    error: string | null;
}

const initialState: AuthState = {
    isAuthenticated: false,
    user: null,
    loading: false,
    error: null,
};

export const login = createAsyncThunk(
    'auth/login',
    async ({ username, password }: LoginData, { rejectWithValue }) => {
        try {
            const response = await userService.login({ username, password });
            const token = response.access_token;
            Cookies.set('access_token', token);
            const user = await userService.getMe();
            return user;
        } catch (error: any) {
            return rejectWithValue(JSON.parse(error.request.response).detail);
        }
    }
);

export const initialize = createAsyncThunk(
    'auth/initialize',
    async (_, { rejectWithValue }) => {
        try {
            const user = await userService.getMe();
            return user;
        } catch (error) {
            return rejectWithValue("No session found");
        }
    }
);

export const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        logout: (state) => {
            Cookies.remove('access_token');
            state.isAuthenticated = false;
            state.user = null;
        },
    },
    extraReducers: (builder) => {
        builder
            // login
            .addCase(login.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(login.fulfilled, (state, action: PayloadAction<User>) => {
                state.isAuthenticated = true;
                state.user = action.payload;
                state.loading = false;
            })
            .addCase(login.rejected, (state, action: PayloadAction<any>) => {
                state.loading = false;
                state.error = action.payload;
            })
            // initialize
            .addCase(initialize.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(initialize.fulfilled, (state, action: PayloadAction<User>) => {
                state.isAuthenticated = true;
                state.user = action.payload;
                state.loading = false;
            })
            .addCase(initialize.rejected, (state) => {
                state.loading = false;
            });
    },
});

export const { logout } = authSlice.actions;

export default authSlice.reducer;
