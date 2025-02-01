import { redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

interface DoctorRegisterResponse {
    message?: string;
    email?: string;
    username?: string;
    password1?: string;
    password2?: string;
    doctor_proof?: File;
    non_field_errors?: string;
}

export const actions = {
    default: async ({ request, fetch, url, cookies }) => {
        const data = await request.formData();

        const response = (await fetch(
            url.origin + '/api/dj-rest-auth/registration-doctor/',
            {
                method: 'POST',
                body: data,
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                }
            }
        ));
        const result = await response.json() as DoctorRegisterResponse;

        return result;
    },
} satisfies Actions;