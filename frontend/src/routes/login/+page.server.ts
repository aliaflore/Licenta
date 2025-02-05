import { redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import { env } from '$env/dynamic/public';

interface LoginResponse {
    username?: string;
    password?: string;
    non_field_errors?: string[];
}

export const actions = {
    default: async ({ request, fetch, url, cookies }) => {
        const data = await request.formData();

        const response = (await fetch(
            env.PUBLIC_BACKEND_URL + '/api/dj-rest-auth/login/',
            {
                method: 'POST',
                body: data,
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                },
                credentials: 'include',
            }
        ));
        const result = await response.json() as LoginResponse;

        if (response.ok) {
            redirect(302, '/');
        }

        return result;
    },
} satisfies Actions;