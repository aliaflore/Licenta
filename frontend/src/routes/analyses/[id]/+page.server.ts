import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { Analysis } from '$lib/types';


export const load: PageServerLoad = async ({ params, fetch }) => {
    const response = await fetch('/api/analysis/' + params.id + '/', {
        method: 'GET',
    });
    if (!response.ok) {
        error(response.status, response.statusText);
    }
    const analysis = await response.json() as Analysis;
    return {
        id: params.id,
        analysis,
    }
}