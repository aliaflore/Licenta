<script lang="ts">
	import { enhance } from '$app/forms';
	import type { PageData, ActionData } from './$types';

	export let data: PageData;
    export let form: ActionData;

    console.log(data);
</script>

<svelte:head>
	<title>Profile</title>
</svelte:head>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 text-center flex flex-col items-center">
		<div class="flex justify-center space-x-2 flex-col gap-4">
            {#if form?.modified}
            <aside class="alert variant-ghost">
                <div class="alert-message">
                    <h3 class="h3">Success!</h3>
                    <p>The changes have been saved!</p>
                </div>
            </aside>
            {/if}
			<form method="post" class="space-y-4" action="?/edit" use:enhance={() => {
                return async ({ update }) => {
                    update({ reset: false });
                };
            }}>
                {#if form?.errors?.non_field_errors}
                    <p class="text-red-500">{form.errors.non_field_errors}</p>
                {/if}
				<input type="hidden" name="pk" value={data?.user?.pk} />

                <label class="label">
                    <span>Username</span>
                    <input class="input" type="text" name="username" value={data?.user?.username} disabled />
                </label>

				<label class="label">
					<span>Email</span>
					<input class="input" type="text" name="email" value={data?.user?.email} disabled />
				</label>

                {#if form?.errors?.first_name}
                    <p class="text-red-500">{form.errors.first_name}</p>
                {/if}
				<label class="label">
					<span>First Name</span>
					<input class="input" type="text" name="first_name" value={data?.user?.first_name} />
				</label>

                {#if form?.errors?.last_name}
                    <p class="text-red-500">{form.errors.last_name}</p>
                {/if}
				<label class="label">
					<span>Last Name</span>
					<input class="input" type="text" name="last_name" value={data?.user?.last_name} />
				</label>

                {#if form?.errors?.password1}
                    <p class="text-red-500">{form.errors.password1}</p>
                {/if}
				<label class="label">
					<span>Password</span>
					<input class="input" type="password" name="password1" />
				</label>

                {#if form?.errors?.password2}
                    <p class="text-red-500">{form.errors.password2}</p>
                {/if}
				<label class="label">
					<span>Confirm Password</span>
					<input class="input" type="password" name="password2" />
				</label>

				<button class="w-full btn-md btn variant-filled" type="submit">Update Profile</button>
			</form>
		</div>
        <form method="post" action="?/delete" class="w-full">
            <input type="hidden" name="user_pk" value={data?.user?.pk} />
            <button class="w-full btn-md btn variant-ghost !bg-red-500" type="submit">Delete Account</button>
        </form>
	</div>
</div>
