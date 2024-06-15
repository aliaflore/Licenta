<script lang="ts">
	import '../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';
	import AccountCircle from 'svelte-material-icons/AccountCircle.svelte';
	import AccountArrowDown from 'svelte-material-icons/AccountArrowDown.svelte';
	import AccountQuestion from 'svelte-material-icons/AccountQuestion.svelte';
	import AccountWrench from 'svelte-material-icons/AccountWrench.svelte';
	import AccountOff from 'svelte-material-icons/AccountOff.svelte';
	import History from 'svelte-material-icons/History.svelte';
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<!-- App Shell -->
<AppShell>
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar>
			<svelte:fragment slot="lead">
				<strong class="text-xl uppercase">Licenta</strong>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				{#if data.loggedIn}
					<a href="/history" class="btn btn-sm variant-ghost-surface">
						<span><History size={30} /></span>
						<span>Istoricul datelor</span>
					</a>
					<a href="/logout" class="btn btn-sm variant-ghost-surface">
						<span><AccountOff size={30} /></span>
						<span>Iesire din cont</span>
					</a>
					<a href="/account-settings" class="btn btn-sm variant-ghost-surface">
						<span><AccountWrench size={30} /></span>
						<span>Setarile contului</span>
					</a>

					<a href="/" class="btn btn-sm variant-ghost-surface">
						<span><AccountCircle size={30} /></span>
						<span>Profilul meu</span>
					</a>
				{:else}
					<a href="/register" class="btn btn-sm variant-ghost-surface">
						<span><AccountQuestion size={30} /></span>
						<span>Inregistrare</span>
					</a>
					<a href="/login" class="btn btn-sm variant-ghost-surface">
						<span><AccountArrowDown size={30} /></span>
						<span>Autentificare</span>
					</a>
				{/if}
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<!-- Page Route Content -->
	<slot />
</AppShell>
