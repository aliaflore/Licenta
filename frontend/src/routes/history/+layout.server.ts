import type { LayoutServerLoad } from './$types';

type HistoryData = {
    results: {
        nume: string,
        data: {
            date: string,
            is_numeric: boolean,
            result: number,
            range_min: number,
            range_max: number,
            expected: boolean,
            measurement_unit: string
            suggestion?: string
        }[]
    }[]
}

export const load: LayoutServerLoad = async ({ parent, fetch }) => {
    const parentData = await parent();

    const response = (await fetch(
        '/api/history/',
        {
            method: 'GET',
        },
    ));
    const result = (await response.json() || []) as HistoryData;
    console.log(result);
    return {
        ...parentData,
        history: result.results
    };
};