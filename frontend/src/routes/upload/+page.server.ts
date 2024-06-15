import { redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

export const actions = {
    default: async ({ request, fetch, url, cookies }) => {
        const data: any = await request.formData();

        const formData = new FormData();


        formData.append("file", data.get("dropzoneAnalize"));
        formData.append("source", "0");

        console.log(formData);

        const response = (await fetch(
            url.origin + '/api/analizePdf/',
            {
                method: 'POST',
                body: formData,
                headers: {
                    "X-CSRFToken": cookies.get('csrftoken') || '',
                }
            }
        ));
        const result = await response.text() as any;

        console.log(result);

        if (result?.id) {
            console.log("PDF received");
            redirect(302, '/');
        }

        return {};
    },
} satisfies Actions;