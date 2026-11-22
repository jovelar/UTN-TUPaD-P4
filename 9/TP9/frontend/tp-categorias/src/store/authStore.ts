import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { UsuarioAuth } from '../types/auth.types';
import { requestLogin, requestLogout, requestMe } from '../api/auth';

interface AuthState {
    user: UsuarioAuth | null;
    isChecking: boolean;        // confirmando la sesión con /auth/me
    isSubmitting: boolean;      // enviando el formulario de login
    error: string | null;

    login: (email: string, password: string) => Promise<void>;
    checkSession: () => Promise<void>;
    logout: () => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set) => ({
            user: null,
            isChecking: true,
            isSubmitting: false,
            error: null,

            login: async (email, password) => {
                set({ isSubmitting: true, error: null });
                try {
                    await requestLogin(email, password);      // el servidor guarda la cookie
                    set({ user: await requestMe() });
                } catch (e) {
                    set({ user: null, error: (e as Error).message });
                } finally {
                    set({ isSubmitting: false });
                }
            },

            checkSession: async () => {
                try {
                    set({ user: await requestMe() });         // null si la cookie venció
                } catch {
                    set({ user: null });                      // backend caído o error de red
                } finally {
                    set({ isChecking: false });
                }
            },

            logout: async () => {
                try {
                    await requestLogout();                    // el servidor borra la cookie
                } finally {
                    set({ user: null });
                }
            },
        }),
        {
            name: 'auth-storage',
            storage: createJSONStorage(() => sessionStorage),
            // no guarda isChecking, isSubmitting ni error
            partialize: (state) => ({ user: state.user }),
        },
    ),
);