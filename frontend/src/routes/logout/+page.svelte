<script lang="ts">
	import { enhance } from '$app/forms';
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h2">Are you sure you want to logout?</h2>
		<div class="flex justify-center space-x-2">
    		<form method="post" use:enhance>
				<button name="logout" type="submit" class="btn btn-md w-full variant-ghost-surface mt-4">Logout</button>
			</form>
		</div>
	</div>
</div>
