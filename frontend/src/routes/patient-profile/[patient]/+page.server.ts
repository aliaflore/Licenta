import type { PageServerLoad } from '../$types';
import type { User } from '$lib/types';
import { env } from '$env/dynamic/public';

export const load: PageServerLoad = async ({ fetch, url, params }) => {
    const response = (await fetch(
        env.PUBLIC_BACKEND_URL + `/api/users/${params.patient}/`,
        {
            method: 'GET',
            credentials: 'include',
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