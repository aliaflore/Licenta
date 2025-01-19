import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { Analysis } from '$lib/types';


export const load: PageServerLoad = async ({ params, fetch, url }) => {
    const user = url.searchParams.get('user');
    const response = await fetch('/api/analysis/' + params.id + '/' + (user ? `?user=${user}` : ''), {
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