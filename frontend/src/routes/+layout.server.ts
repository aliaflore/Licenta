import type { LayoutServerLoad } from './$types';
import type { UserResult, Error, AnalysisProviderResult } from '$lib/types';

type UResult = UserResult & Error;
type AResult = AnalysisProviderResult & Error;

export const load: LayoutServerLoad = async ({ fetch }) => {
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