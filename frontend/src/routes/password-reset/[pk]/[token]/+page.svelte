<script lang="ts">
	import { enhance } from '$app/forms';
	import type { ActionData, PageData } from './$types';

    export let form: ActionData;
    export let data: PageData;
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
                {#each form?.non_field_errors || [] as error}
                    <p class="text-red-500">{error}</p>
                {/each}
                {#each form?.uid || [] as error}
                    <p class="text-red-500">{error}</p>
                {/each}
                <input type="hidden" name="uid" value={data?.params.pk} />
                {#each form?.token || [] as error}
                    <p class="text-red-500">{error}</p>
                {/each}
                <input type="hidden" name="token" value={data?.params.token} />
                {#each form?.non_field_errors || [] as error}
                    <p class="text-red-500">{error}</p>
                {/each}

                {#each form?.new_password1 || [] as error}
                    <p class="text-red-500">{error}</p>
                {/each}
				<label class="label">
					<span>Password</span>
					<input name="new_password1" class="input" type="password" placeholder="Passsword" />
				</label>

                {#each form?.new_password2 || [] as error}
                    <p class="text-red-500">{error}</p>
                {/each}
                <label class="label">
                    <span>Confirm Password</span>
                    <input name="new_password2" class="input" type="password" placeholder="Password" />
                </label>

				<button type="submit" class="btn btn-md w-full variant-ghost-surface mt-4">Reset your password</button>
			</form>
		</div>
	</div>
</div>
