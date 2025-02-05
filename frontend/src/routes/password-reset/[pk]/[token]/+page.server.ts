import { redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { env } from '$env/dynamic/public';

export const load: PageServerLoad = async ({ url, params }) => {
    return {
        params: {
            pk: params.pk,
            token: params.token
        }
    }
};

interface PasswordResetResponse {
    detail?: string;
    uid?: string[];
    token?: string[];
    new_password1?: string[];
    new_password2?: string[];
    non_field_errors?: string[];
}

export const actions = {
    default: async ({ request, fetch, url, cookies }) => {
        const data = await request.formData();

        const response = (await fetch(
            env.PUBLIC_BACKEND_URL + '/api/dj-rest-auth/password/reset/confirm/',
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
            redirect(302, '/login');
        }

        return result;
    },
} satisfies Actions;