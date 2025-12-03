import axios from 'axios';
import { useToastStore } from '@/stores/toast';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8001',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        const toastStore = useToastStore();

        // Prevent infinite loops
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');

                if (refreshToken) {
                    const response = await axios.post(`${api.defaults.baseURL}/api/token/refresh/`, {
                        refresh: refreshToken
                    });

                    if (response.status === 200) {
                        const newAccessToken = response.data.access;
                        localStorage.setItem('access_token', newAccessToken);

                        // Update the header for the original request
                        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

                        // Update the header for future requests
                        api.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;

                        return api(originalRequest);
                    }
                }
            } catch (refreshError) {
                // Refresh failed - clear tokens and redirect
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('username');
                localStorage.removeItem('is_staff');

                toastStore.error('Session expirée, veuillez vous reconnecter.');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        if (error.response) {
            // Server responded with error code
            const status = error.response.status;
            const data = error.response.data;

            if (status === 401) {
                // If we get here, it means the retry failed or it wasn't a refreshable 401
                // Only show toast if we haven't already handled the redirect in the catch block above
                // But actually, if the refresh logic above fails, it rejects.
                // If we are here, it might be a 401 that didn't trigger the retry logic (e.g. no refresh token)
                if (!originalRequest._retry) {
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    localStorage.removeItem('username');
                    localStorage.removeItem('is_staff');
                    toastStore.error('Session expirée, veuillez vous reconnecter.');
                    window.location.href = '/login';
                }
            } else if (status === 403) {
                toastStore.error('Accès refusé.');
            } else if (status >= 500) {
                toastStore.error('Erreur serveur. Veuillez réessayer plus tard.');
            } else {
                // Other errors (400, 404, etc.)
                const message = data.detail || data.message || data.error || 'Une erreur est survenue.';
                toastStore.error(message);
            }
        } else if (error.request) {
            // No response received (Network error)
            toastStore.error('Impossible de contacter le serveur. Vérifiez votre connexion.');
        } else {
            // Request setup error
            toastStore.error('Erreur inattendue.');
        }

        return Promise.reject(error);
    }
);

export default api;
