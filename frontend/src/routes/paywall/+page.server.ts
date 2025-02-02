import type { HistoryDataResult } from '$lib/types';
import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ parent, fetch }) => {
    const parentData = await parent();

    if (parentData.user?.is_paying) {
        redirect(301, '/');
    }
};