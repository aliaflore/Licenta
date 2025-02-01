<script lang="ts">
	import { enhance } from '$app/forms';
	import CheckBold from 'svelte-material-icons/CheckBold.svelte';
	import type { ActionData } from './$types';

    export let form: ActionData;
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h2">Login</h2>
		<div class="flex justify-center space-x-2">
			<form method="post" use:enhance={() => {
                return async ({ update }) => {
                    update({ reset: false });
                };
            }}>
                {#each form?.non_field_errors || [] as error}
                    <p class="text-red-500">{error}</p>
                {/each}

                {#if form?.username}
                    <p class="text-red-500">Invalid username or password</p>
                {/if}
				<label class="label">
					<span>Username</span>
					<input name="username" class="input" type="text" placeholder="Username" />
				</label>

                {#if form?.password}
                    <p class="text-red-500">Invalid username or password</p>
                {/if}
				<label class="label">
					<span>Password</span>
					<input name="password" class="input" type="password" placeholder="Password" />
				</label>

				<button type="submit" class="btn btn-md w-full variant-ghost-surface mt-4">Login into your account</button>
			</form>
		</div>
	</div>
</div>
