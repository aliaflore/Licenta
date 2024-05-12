<script lang="ts">
	import CheckBold from 'svelte-material-icons/CheckBold.svelte';
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h2">Autentificare</h2>
		<div class="flex justify-center space-x-2">
			<label class="label">
				<span>ID de utilizator</span>
				<input class="input" type="text" placeholder="scrie ID-ul..." />
			</label>

			<label class="label">
				<span>Parola</span>
				<input class="input" type="text" placeholder="scrie parola..." />
			</label>

			<button type="button" class="btn btn-sm variant-ghost-surface"><CheckBold /></button>
		</div>
	</div>
</div>
