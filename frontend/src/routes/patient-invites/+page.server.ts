import { redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import type { Error } from '$lib/types';
import { env } from '$env/dynamic/public';

export const actions = {
    resend: async ({ request, fetch, url, cookies }) => {
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
            env.PUBLIC_BACKEND_URL + `/api/patient-invites/${pk}/resend/`,
            {
                method: 'POST',
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                },
                credentials: 'include',
            }
        ));

        redirect(302, '/patient-invites');
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
            env.PUBLIC_BACKEND_URL + `/api/patient-invites/${pk}/`,
            {
                method: 'DELETE',
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                },
                credentials: 'include',
            }
        ));

        redirect(302, '/patient-invites');
    },
    invite: async ({ request, fetch, url, cookies }) => {
        const data = await request.formData();
        const email = data.get('email');
        if (!email) {
            return;
        }

        const response = (await fetch(
            env.PUBLIC_BACKEND_URL + '/api/patient-invites/',
            {
                method: 'POST',
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email }),
                credentials: 'include',
            }
        ));

        const responseData = await response.json() as any;
        if(responseData?.email) {
            return {
                errors: {
                    email: responseData.email
                }
            }
        }

        redirect(302, '/patient-invites');
    }
} satisfies Actions;