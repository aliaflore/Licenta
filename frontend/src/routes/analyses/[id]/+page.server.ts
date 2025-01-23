import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { Analysis, HistoryDataResult } from '$lib/types';


export const load: PageServerLoad = async ({ params, fetch, url }) => {
    const user = url.searchParams.get('user');
    const response = await fetch('/api/analysis/' + params.id + '/' + (user ? `?user=${user}` : ''), {
        method: 'GET',
    });
    if (!response.ok) {
        error(response.status, response.statusText);
    }
    const analysis = await response.json() as Analysis;

    const historyGraphParams = new URLSearchParams();
    if (user) {
        historyGraphParams.set('user', user);
    }
    analysis.results.forEach((result) => {
        historyGraphParams.append('analysis', result.category.name + ':' + result.name);
    });

    const histroyGraphsData = await fetch('/api/history/?' + historyGraphParams.toString(), {
        method: 'GET',
    });
    const historyData = await histroyGraphsData.json() as HistoryDataResult;
    if (!histroyGraphsData.ok) {
        error(histroyGraphsData.status, histroyGraphsData.statusText);
    }

    return {
        id: params.id,
        analysis,
        historyData: historyData,
    }
}