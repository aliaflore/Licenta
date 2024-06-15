<script lang="ts">
	import { enhance } from '$app/forms';
	import CheckBold from 'svelte-material-icons/CheckBold.svelte';
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h2">Autentificare</h2>
		<div class="flex justify-center space-x-2">
			<form method="post" use:enhance>
				<label class="label">
					<span>ID de utilizator</span>
					<input name="username" class="input" type="text" placeholder="scrie ID-ul..." />
				</label>

				<label class="label">
					<span>Parola</span>
					<input name="password" class="input" type="password" placeholder="scrie parola..." />
				</label>

				<button type="submit" class="btn btn-sm variant-ghost-surface mt-4"><CheckBold /></button>
			</form>
		</div>
	</div>
</div>
