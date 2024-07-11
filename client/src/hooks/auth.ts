import { useAppDispatch, useAppSelector } from './redux';

import { initialize } from '../store/authSlice'; // Import the initialize action
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export const useAuthGuard = (test_mode: boolean) => {
    const isAuthenticated = useAppSelector((state) => state.auth.isAuthenticated);
    const dispatch = useAppDispatch();
    const navigate = useNavigate();

    useEffect(() => {
        if (!isAuthenticated && !test_mode) {
            dispatch(initialize())
                .unwrap()
                .then(() => {
                    // Initialization succeeded, user is now authenticated
                })
                .catch(() => {
                    // Initialization failed, redirect to login
                    navigate("/login");
                });
        }
    }, [isAuthenticated, navigate, test_mode, dispatch]);
};
