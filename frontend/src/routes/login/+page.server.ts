import { redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

interface LoginResponse {
    username?: string;
    password?: string;
    non_field_errors?: string[];
}

export const actions = {
    default: async ({ request, fetch, url, cookies }) => {
        const data = await request.formData();

        const response = (await fetch(
            url.origin + '/api/dj-rest-auth/login/',
            {
                method: 'POST',
                body: data,
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                }
            }
        ));
        const result = await response.json() as LoginResponse;

        if (response.ok) {
            redirect(302, '/');
        }

        return result;
    },
} satisfies Actions;