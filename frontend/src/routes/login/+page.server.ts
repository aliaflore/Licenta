import { redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

export const actions = {
    default: async ({ request, fetch, url }) => {
        const data = await request.formData();
        const username = data.get('username')?.toString() || '';
        const password = data.get('password')?.toString() || '';

        const response = (await fetch(
            url.origin + '/api/dj-rest-auth/login/',
            {
                method: 'POST',
                body: JSON.stringify({ username: username, password: password }),
                headers:
                {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            }
        ));
        const result = await response.json() as any;

        if (result?.key) {
            console.log("Logged in");
            redirect(302, '/');
        }

        return { error: result?.non_field_errors };
    },
} satisfies Actions;