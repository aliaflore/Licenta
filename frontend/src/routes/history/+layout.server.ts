import type { HistoryData } from '$lib/types';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ parent, fetch }) => {
    const parentData = await parent();

    const response = (await fetch(
        '/api/history/',
        {
            method: 'GET',
        },
    ));
    const result = (await response.json() || []) as HistoryData;
    return {
        ...parentData,
        history: result.results
    };
};