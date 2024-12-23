import { redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

export const actions = {
    default: async ({ request, fetch, url, cookies }) => {
        const data = await request.formData();
        const logout = data.get('logout')?.toString() || '';

        const response = (await fetch(
            url.origin + '/api/dj-rest-auth/logout/',
            {
                method: 'POST',
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                }
            }
        ));

        redirect(302, '/');
    },
} satisfies Actions;