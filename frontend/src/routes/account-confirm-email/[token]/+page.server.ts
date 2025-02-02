import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ url, params, fetch, cookies }) => {
    const response = (await fetch(
        '/api/dj-rest-auth/registration/verify-email/',
        {
            method: 'POST',
            body: JSON.stringify({ key: params.token }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': cookies.get('csrftoken') || '',
            },
        }
    ));
    if (response.ok) {
        redirect(302, '/');
    }

    return {
        message: "The token is invalid."
    }
};