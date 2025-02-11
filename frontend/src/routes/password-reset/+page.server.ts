import { env } from '$env/dynamic/public';
import type { Actions } from './$types';

interface PasswordResetResponse {
    detail?: string;
}

export const actions = {
    default: async ({ request, fetch, url, cookies }) => {
        const data = await request.formData();

        const response = (await fetch(
            env.PUBLIC_BACKEND_URL + '/api/dj-rest-auth/password/reset/',
            {
                method: 'POST',
                body: data,
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                },
                credentials: 'include',
            }
        ));
        const result = await response.json() as PasswordResetResponse;

        if (response.ok) {
            return {
                sent: true
            };
        }

        return result;
    },
} satisfies Actions;