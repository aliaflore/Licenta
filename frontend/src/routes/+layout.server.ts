import type { LayoutServerLoad } from './$types';
import type { UserResult, Error, AnalysisProviderResult } from '$lib/types';
import { redirect } from '@sveltejs/kit';

type UResult = UserResult & Error;
type AResult = AnalysisProviderResult & Error;

const allowed_paywall_urls = [
    '/login',
    '/logout',
    '/register',
    '/forgot-password',
    '/reset-password',
    '/paywall',
]

export const load: LayoutServerLoad = async ({ fetch, url }) => {
    const response = (await fetch(
        '/api/users/me/',
        {
            method: 'GET',
        }
    ));
    const result = await response.json() as UResult;
    if (result?.error) {
        return {
            user: null,
            analysisProviders: null
        }
    }

    if (!result?.user?.is_paying && !result?.user?.is_doctor && !result?.user?.is_superuser && result.user && !allowed_paywall_urls.includes(url.pathname)) {
        redirect(301, '/paywall');
    }

    const response2 = (await fetch (
        '/api/analysis-providers/',
        {
            method: 'GET',
        }
    ));
    const providers = await response2.json() as AResult;
    if (providers?.error) {
        return {
            user: null,
            analysisProviders: null
        }
    }
    return {
        user: result.user,
        analysisProviders: providers
    };
};