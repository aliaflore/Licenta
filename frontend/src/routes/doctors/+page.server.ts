import { redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import { env } from '$env/dynamic/public';

export const actions = {
    accept: async ({ request, fetch, url, cookies }) => {
        const data = await request.formData();
        const pk = data.get('pk');
        if (!pk) {
            return;
        }
        const pkInt = parseInt(pk.toString(), 10);
        if (isNaN(pkInt)) {
            return;
        }

        const response = (await fetch(
            env.PUBLIC_BACKEND_URL + `/api/doctor-invites/${pk}/`,
            {
                method: 'PUT',
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    accepted: true,
                }),
                credentials: 'include',
            }
        ));

        redirect(302, '/doctors');
    },
    delete: async ({ request, fetch, url, cookies }) => {
        const data = await request.formData();
        const pk = data.get('pk');
        if (!pk) {
            return;
        }
        const pkInt = parseInt(pk.toString(), 10);
        if (isNaN(pkInt)) {
            return;
        }

        const response = (await fetch(
            env.PUBLIC_BACKEND_URL + `/api/doctor-invites/${pk}/`,
            {
                method: 'DELETE',
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                },
                credentials: 'include',
            }
        ));

        redirect(302, '/doctors');
    }
} satisfies Actions;