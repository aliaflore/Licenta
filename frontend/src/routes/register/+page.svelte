<script lang="ts">
	import CheckBold from 'svelte-material-icons/CheckBold.svelte';
	import type { PageData } from './$types';

	export let data: PageData;
</script>

{#if data.loggedIn}
	You are logged in. Click here to go to the main page
{:else}
	<div class="container h-full mx-auto flex justify-center items-center">
		<div class="space-y-10 text-center flex flex-col items-center">
			<h2 class="h2">Inregistrare</h2>
			<div class="flex justify-center space-x-2 flex-col gap-4">
				<label class="label">
					<span>Email</span>
					<input class="input" type="text" placeholder="scrie email-ul..." />
				</label>

				<label class="label">
					<span>Telefon</span>
					<input class="input" type="text" placeholder="scrie numarul..." />
				</label>

				<label class="label">
					<span>ID de utilizator</span>
					<input class="input" type="text" placeholder="scrie ID-ul..." />
				</label>

				<label class="label">
					<span>Parola</span>
					<input class="input" type="text" placeholder="scrie parola..." />
				</label>

				<label class="label">
					<span>Confirma parola</span>
					<input class="input" type="text" placeholder="scrie parola..." />
				</label>

				<button type="button" class="btn btn-sm variant-ghost-surface h-8 mt-4"
					><CheckBold /></button
				>
			</div>
		</div>
	</div>
{/if}
