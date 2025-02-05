import { env } from "$env/dynamic/public";

function getCookie(name: string) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2)
        return parts.pop()?.split(';').shift();
}

interface CheckoutResponse {
    error?: string;
    redirect_url?: string;
}

export async function checkout() {
    const response = (await fetch(
        env.PUBLIC_BACKEND_URL + '/api/subscription-checkout/',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken') || '',
            },
            credentials: 'include',
        }
    ));
    const data = await response.json() as CheckoutResponse;
    if (!data.redirect_url) {
        return {
            error: data.error,
        }
    }

    window.location.href = data.redirect_url;
}
