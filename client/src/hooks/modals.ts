import { useState } from 'react';

interface ModalState<T> {
    isOpen: boolean;
    data: T | null;
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
    return { state, open, close };
};