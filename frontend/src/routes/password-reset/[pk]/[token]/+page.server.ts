import { redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

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
            url.origin + '/api/dj-rest-auth/password/reset/confirm/',
            {
                method: 'POST',
                body: data,
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                }
            }
        ));
        const result = await response.json() as PasswordResetResponse;

        console.log(result);

        if (response.ok) {
            redirect(302, '/login');
        }

        return result;
    },
} satisfies Actions;