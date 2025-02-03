<script lang="ts">
	import { viewAsUser } from '$lib';
    import AnalysesList from '$lib/AnalysesList.svelte';
</script>

<div class="flex justify-center align-middle">
    <AnalysesList viewAsUser={$viewAsUser} />
</div>