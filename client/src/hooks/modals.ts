import { useState } from 'react';

interface ModalState<T> {
    isOpen: boolean;
    data: T | null;
    error?: string | null;
}

export const useModalState = (initialState: boolean = false) => {
    const [isOpen, setIsOpen] = useState(initialState);
    const open = () => setIsOpen(true);
    const close = () => setIsOpen(false);
    return { isOpen, open, close };
};
  
export const useUpdateModalState = <T,>(initialData: T | null = null) => {
    const [state, setState] = useState<ModalState<T>>({ isOpen: false, data: initialData });
    const open = (data: T) => setState({ isOpen: true, data });
    const close = () => setState({ isOpen: false, data: null });
    const setError = (error: string) => setState({...state, error })
    return { state, open, close, setError };
};