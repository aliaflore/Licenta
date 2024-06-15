<script lang="ts">
	import { enhance } from '$app/forms';
	import CheckBold from 'svelte-material-icons/CheckBold.svelte';
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h2">Esti sigur ca vrei sa te deloghezi?</h2>
		<div class="flex justify-center space-x-2">
			<button type="submit" class="btn btn-sm variant-ghost-surface mt-4"><CheckBold />Nu, mergi inapoi</button>
    		<form method="post" use:enhance>
				<button name="logout" type="submit" class="btn btn-sm variant-ghost-surface mt-4"><CheckBold />Da</button>
			</form>
		</div>
	</div>
</div>
