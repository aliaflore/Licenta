import { redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import { env } from '$env/dynamic/public';

export const actions = {
    default: async ({ request, fetch, url, cookies }) => {
        const data = await request.formData();
        const logout = data.get('logout')?.toString() || '';

        const response = (await fetch(
            env.PUBLIC_BACKEND_URL + '/api/dj-rest-auth/logout/',
            {
                method: 'POST',
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                },
                credentials: 'include',
            }
        ));

        redirect(302, '/');
    },
} satisfies Actions;