import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { env } from '$env/dynamic/public';

export const load: PageServerLoad = async ({ url, params, fetch, cookies }) => {
    const response = (await fetch(
        env.PUBLIC_BACKEND_URL + '/api/dj-rest-auth/registration/verify-email/',
        {
            method: 'POST',
            body: JSON.stringify({ key: params.token }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': cookies.get('csrftoken') || '',
            },
            credentials: 'include',
        }
    ));
    if (response.ok) {
        redirect(302, '/');
    }

    return {
        message: "The token is invalid."
    }
};