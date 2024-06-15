import type { LayoutServerLoad } from './$types';

type User = {
    url: string;
    username: string;
    email: string;
    is_staff: boolean;
    id: number;
};

export const load: LayoutServerLoad = async ({ fetch, url }) => {

    const response = (await fetch(
        url.origin + '/api/users/me/',
        {
            method: 'GET',
        }
    ));
    const result = await response.json() as any;
    console.log(result);
    return {
        loggedIn: !result?.error,
        user: result?.user as User
    };
};