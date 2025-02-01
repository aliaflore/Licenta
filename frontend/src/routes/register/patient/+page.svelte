<script lang="ts">
	import type { PageData, ActionData } from './$types';
	import { enhance } from '$app/forms';

    export let data: PageData;
    export let form: ActionData;
</script>

<div class="container h-full mx-auto flex justify-center items-center">
    <div class="space-y-10 text-center flex flex-col items-center">
        {#if form?.message}
            <aside class="alert variant-ghost">
                <div class="alert-message">
                    <h3 class="h3">Success!</h3>
                    <p>{form?.message}</p>
                </div>
            </aside>
        {/if}
        <h2 class="h2">Register a Patient Account</h2>
        <div class="flex justify-center space-x-2 flex-col gap-4">
            <form method="post" enctype="multipart/form-data" use:enhance>
                <label class="label">
                    <span>Email</span>
                    <input name="email" class="input" type="text" placeholder="a@a.com" required />
                    {#if form?.email}
                        <div class="text-red-500">{form.email}</div>
                    {/if}
                </label>

                <label class="label">
                    <span>Username</span>
                    <input name="username" class="input" type="text" placeholder="username" required />
                    {#if form?.username}
                        <div class="text-red-500">{form.username}</div>
                    {/if}
                </label>

                <label class="label">
                    <span>Password</span>
                    <input name="password1" class="input" type="password" placeholder="password" required />
                    {#if form?.password1}
                        <div class="text-red-500">{form.password1}</div>
                    {/if}
                </label>

                <label class="label">
                    <span>Confirm Password</span>
                    <input name="password2" class="input" type="password" placeholder="password" required />
                    {#if form?.password2}
                        <div class="text-red-500">{form.password2}</div>
                    {/if}
                </label>

                <button type="submit" class="btn btn-md variant-ghost-surface h-8 mt-4 w-full"
                    >Submit</button
                >
            </form>
        </div>
    </div>
</div>