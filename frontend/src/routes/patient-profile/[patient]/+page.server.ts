import type { PageServerLoad } from '../$types';
import type { User } from '$lib/types';

export const load: PageServerLoad = async ({ fetch, url, params }) => {
    const response = (await fetch(
        `/api/users/${params.patient}/`,
        {
            method: 'GET',
        }
    ));
    const result = await response.json() as User;
    if (!response.ok) {
        return {
            patient: null
        }
    }

    return {
        patient: result
    }
};