import type { HistoryDataResult } from '$lib/types';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ parent, fetch }) => {
    const parentData = await parent();

    const response = (await fetch(
        '/api/history/',
        {
            method: 'GET',
        },
    ));
    const history = (await response.json() || []) as HistoryDataResult;
    return {
        ...parentData,
        history: history,
    };
};