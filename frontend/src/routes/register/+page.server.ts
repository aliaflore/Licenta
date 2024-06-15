import { redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

export const actions = {
    default: async ({ request, fetch, url }) => {
        const data = await request.formData();
        const email = data.get('email')?.toString() || '';
        const telefon = data.get('telefon')?.toString() || '';
        const username = data.get('username')?.toString() || '';
        const password1 = data.get('password1')?.toString() || '';
        const password2 = data.get('password2')?.toString() || '';

        const response = (await fetch(
            url.origin + '/api/dj-rest-auth/registration/',
            {
                method: 'POST',
                body: JSON.stringify({ email: email, telefon: telefon, username: username, password1: password1, password2: password2 }),
                headers:
                {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            }
        ));
        const result = await response.text() as any;

        console.log(result);

        if (result?.key) {
            console.log("Logged in");
            redirect(302, '/');
        }

        return { error: result?.non_field_errors };
    },
} satisfies Actions;