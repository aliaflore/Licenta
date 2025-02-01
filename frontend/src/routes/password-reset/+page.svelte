<script lang="ts">
	import { enhance } from '$app/forms';
	import type { ActionData } from './$types';

    export let form: ActionData;
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h2">Reset password</h2>
		<div class="flex justify-center space-x-2">
			<form method="post" use:enhance={() => {
                return async ({ update }) => {
                    update({ reset: false });
                };
            }}>
                {#if form?.sent}
                    <aside class="alert variant-ghost">
                        <div class="alert-message">
                            <p>The password reset link has been sent to your email.</p>
                        </div>
                    </aside>
                {/if}

                {#each form?.detail || [] as error}
                    <p class="text-red-500">{error}</p>
                {/each}
				<label class="label">
					<span>Email</span>
					<input name="email" class="input" type="email" placeholder="Email" />
				</label>
            
				<button type="submit" class="btn btn-md w-full variant-ghost-surface mt-4">Reset your password</button>
			</form>
		</div>
	</div>
</div>
