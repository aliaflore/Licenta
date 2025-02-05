import { redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import type { AnalysisPDF } from '$lib/types';
import { env } from '$env/dynamic/public';

interface uploadErrors {
    provider_id?: string[];
    file?: string[];
    doctor_notes?: string[];
    taken_on?: string[];
}

export const actions = {
    default: async ({ request, fetch, url, cookies }) => {
        const data = await request.formData();

        const response = (await fetch(
            env.PUBLIC_BACKEND_URL + '/api/analysis-pdf/',
            {
                method: 'POST',
                body: data,
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                },
                credentials: 'include',
            }
        ));

        if(response.ok) {
            const result = await response.json() as AnalysisPDF;
            redirect(302, `/analyses`);
        }

        const result = await response.json() as uploadErrors;
        return {
            status: response.status,
            errors: result
        };
    },
} satisfies Actions;