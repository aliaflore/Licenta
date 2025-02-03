import { redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import type { User } from '$lib/types';

interface ProfileErrorResponse {
    password1?: string;
    password2?: string;
    first_name?: string;
    last_name?: string;
    non_field_errors?: string;
    accept_new_patients?: string;
    birth_date?: string;
    phone_number?: string;
    height?: string;
    weight?: string;
}

export const actions = {
    edit: async ({ request, fetch, url, cookies }) => {
        const data = await request.formData();
        const pk = data.get('pk');
        if (!pk) {
            return;
        }

        const response = (await fetch(
            url.origin + `/api/users/${pk}/`,
            {
                method: 'PATCH',
                body: data,
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                }
            }
        ));
        const result = await response.json() as ProfileErrorResponse;

        if (!response.ok) {
            return {
                errors: result,
            }
        }

        return {
            modified: true,
        };
    },
    delete: async ({ request, fetch, url, cookies }) => {
        const data = await request.formData();
        const pk = data.get('pk');
        if (!pk) {
            return;
        }

        const response = (await fetch(
            url.origin + `/api/users/${pk}/`,
            {
                method: 'DELETE',
                body: data,
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                }
            }
        ));
        if (response.ok) {
            redirect(301, '/login');
        }

        return {
            deleted: false,
        };
    },
} satisfies Actions;