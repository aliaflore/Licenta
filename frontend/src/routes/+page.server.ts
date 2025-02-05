import type { HistoryDataResult } from '$lib/types';
import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { env } from '$env/dynamic/public';

export const load: PageServerLoad = async ({ parent, fetch }) => {
    const parentData = await parent();

    if(parentData?.user?.is_doctor) {
        redirect(301, '/patient-invites');
    }

    const response = (await fetch(
        env.PUBLIC_BACKEND_URL + '/api/history/',
        {
            method: 'GET',
            credentials: 'include',
        },
    ));
    const history = (await response.json() || []) as HistoryDataResult;
    return {
        ...parentData,
        history: history,
    };
};