import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { Analysis, HistoryDataResult } from '$lib/types';
import { env } from '$env/dynamic/public';


export const load: PageServerLoad = async ({ params, fetch, url }) => {
    const user = url.searchParams.get('user');
    const response = await fetch(env.PUBLIC_BACKEND_URL + '/api/analysis/' + params.id + '/' + (user ? `?user=${user}` : ''), {
        method: 'GET',
        credentials: 'include',
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

    const histroyGraphsData = await fetch(env.PUBLIC_BACKEND_URL + '/api/history/?' + historyGraphParams.toString(), {
        method: 'GET',
        credentials: 'include',
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

        const viewAsUser = data.get('viewas_user');

        const response = (await fetch(
            env.PUBLIC_BACKEND_URL + `/api/analysis-results/${pk}/` + (viewAsUser ? `?user=${viewAsUser}` : ''),
            {
                method: 'PATCH',
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                },
                body: data,
                credentials: 'include',
            }
        ));
        return {
            edit_ok: response.ok
        }
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
            env.PUBLIC_BACKEND_URL + `/api/analysis-results/${pk}/regenerate_suggestions/` + (viewAsUser ? `?user=${viewAsUser}` : ''),
            {
                method: 'POST',
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                },
                credentials: 'include',
            }
        ));
        return;
    }
}