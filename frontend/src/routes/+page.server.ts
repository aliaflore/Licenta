import type { HistoryDataResult } from '$lib/types';
import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ parent, fetch }) => {
    const parentData = await parent();

    if(parentData?.user?.is_doctor) {
        redirect(301, '/patient-invites');
    }

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