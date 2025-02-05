import { env } from '$env/dynamic/public';
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
            env.PUBLIC_BACKEND_URL + '/api/dj-rest-auth/registration-doctor/',
            {
                method: 'POST',
                body: data,
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                },
                credentials: 'include',
            }
        ));
        const result = await response.json() as DoctorRegisterResponse;

        if(response.ok) {
            return {
                message: "Registration successful. Please check your email for a verification link."
            }
        }

        return result;
    },
} satisfies Actions;