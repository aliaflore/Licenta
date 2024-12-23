import type { PageServerLoad } from './$types';
import type { AnalysisPDFResult, Error } from '$lib/types';

type UResult = AnalysisPDFResult & Error;

const limit = 30;

export const load: PageServerLoad = async ({ fetch, parent, url }) => {
    const page = parseInt(url.searchParams.get('page') || '1');
    const parentData = await parent();
    const response = (await fetch(
        `/api/analysis-pdf/?limit=${limit}&offset=${(page - 1) * limit}`, 
        {
            method: 'GET',
        }
    ));
    const result = await response.json() as UResult;
    if (!result?.error) {
        return {
            ...parentData,
            analyses: result.results,
            page: page,
            totalPages: Math.floor(result.count / limit) + 100,
        }
    }
    return {
        ...parentData,
        analyses: null,
        page: 1,
        totalPages: 1,
    }
};