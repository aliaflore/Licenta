import type { LayoutServerLoad } from './$types';

type User = {
    url: string;
    username: string;
    email: string;
    is_staff: boolean;
    id: number;
};

type Error = {
    error: string;
};

type UserResult = {
    user: User;
}

type Result = UserResult & Error;

export const load: LayoutServerLoad = async ({ fetch }) => {
    const response = (await fetch(
        '/api/users/me/',
        {
            method: 'GET',
        }
    ));
    const result = await response.json() as Result;
    if (result?.error) {
        return {
            loggedIn: false,
            user: null
        }
    }
    return {
        loggedIn: true,
        user: result.user
    };
};