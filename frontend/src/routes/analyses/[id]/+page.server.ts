import { error, redirect } from '@sveltejs/kit';
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
        viewAsUser: user,
    }
}

export const actions = {
    edit: async ({ request, fetch, url, cookies }) => {
        const data = await request.formData();
        const pk = data.get('pk');
        if (!pk) {
            return;
        }
        const pkInt = parseInt(pk.toString(), 10);
        if (isNaN(pkInt)) {
            return;
        }

        const viewAsUser = data.get('viewas_user');

        const response = (await fetch(
            url.origin + `/api/analysis-results/${pk}/` + (viewAsUser ? `?user=${viewAsUser}` : ''),
            {
                method: 'PATCH',
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    result: data.get('result'),
                    measurement_unit: data.get('measurement_unit'),
                    range_min: data.get('range_min'),
                    range_max: data.get('range_max'),
                    in_range: data.get('in_range') === 'on',
                    doctor_note: data.get('doctor_note'),
                }),
            }
        ));
        return;
    },
    regenerate: async ({ request, fetch, url, cookies }) => {
        const data = await request.formData();
        const pk = data.get('pk');
        if (!pk) {
            return;
        }
        const pkInt = parseInt(pk.toString(), 10);
        if (isNaN(pkInt)) {
            return;
        }

        const viewAsUser = data.get('viewas_user');

        const response = (await fetch(
            url.origin + `/api/analysis-results/${pk}/regenerate_suggestions/` + (viewAsUser ? `?user=${viewAsUser}` : ''),
            {
                method: 'POST',
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                }
            }
        ));
        return;
    }
}