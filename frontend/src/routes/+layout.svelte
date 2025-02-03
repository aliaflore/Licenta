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

    import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
    import { storePopup } from '@skeletonlabs/skeleton';
	import { page } from '$app/stores';
	import { viewAsUser } from '$lib';
	import { redirect } from '@sveltejs/kit';
    storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });

	interface Props {
		data: PageData;
		children?: import('svelte').Snippet;
	}

	let { data, children }: Props = $props();
</script>

<!-- App Shell -->
<AppShell>
	{#snippet header()}
			<!-- App Bar -->
			<AppBar>
				{#snippet lead()}
					
		                <a href="/">
                            {#if data.user?.is_doctor}
		                        <strong class="text-xl uppercase">Licenta: Doctor</strong>
                            {:else}
		                        <strong class="text-xl uppercase">Licenta: Patient</strong>
                            {/if}
		                </a>
					
					{/snippet}
				{#snippet trail()}
					
						{#if data?.user}
							<!-- <a href="/history" class="btn btn-sm variant-ghost-surface">
								<span><History size={30} /></span>
								<span>Istoricul datelor</span>
							</a> -->
							<!-- <a href="/logout" class="btn btn-sm variant-ghost-surface">
								<span><AccountOff size={30} /></span>
								<span>Iesire din cont</span>
							</a>
							<a href="/account-settings" class="btn btn-sm variant-ghost-surface">
								<span><AccountWrench size={30} /></span>
								<span>Setarile contului</span>
							</a> -->
                            {#if data?.user?.is_doctor && !$viewAsUser}
                            <a href="/patient-invites" class="btn btn-sm variant-ghost-surface">
								<span><AccountCircle size={30} /></span>
								<span>Patients</span>
							</a>
                            {:else if !$viewAsUser}
                            <a href="/upload" class="btn btn-sm variant-ghost-surface">
								<span><AccountCircle size={30} /></span>
								<span>Upload</span>
							</a>
                            <a href="/doctors" class="btn btn-sm variant-ghost-surface">
								<span><AccountCircle size={30} /></span>
								<span>Doctors</span>
							</a>
                            {/if}
                            {#if !data?.user?.is_doctor}
                            <a href="/analyses" class="btn btn-sm variant-ghost-surface">
								<span><AccountCircle size={30} /></span>
								<span>Analyses</span>
							</a>
                            {/if}
                            {#if !data?.user?.is_doctor || $viewAsUser}
                            <a href="/radiographies" class="btn btn-sm variant-ghost-surface">
								<span><AccountCircle size={30} /></span>
								<span>Radiographies</span>
							</a>
                            <a href="/patient-profile/${$viewAsUser?.pk}" class="btn btn-sm variant-ghost-surface">
								<span><AccountCircle size={30} /></span>
								<span>Patient Profile</span>
							</a>
                            {/if}
                            {#if !$viewAsUser}
							<a href="/profile" class="btn btn-sm variant-ghost-surface">
								<span><AccountCircle size={30} /></span>
								<span>My profile</span>
							</a>
                            {:else}
                            <button class="btn btn-sm variant-ghost-surface" onclick={() => {
                                viewAsUser.set(null);
                                window.location.pathname = '/patient-invites';
                            }}>
								<span><AccountCircle size={30} /></span>
								<span>Viewing as: <b>{$viewAsUser.full_name}</b></span>
							</button>
                            {/if}
                            <a href="/logout" class="btn btn-sm variant-ghost-surface">
                                <span><AccountArrowDown size={30} /></span>
                                <span>Logout</span>
                            </a>
						{:else}
							<a href="/register" class="btn btn-sm variant-ghost-surface">
								<span><AccountQuestion size={30} /></span>
								<span>Register</span>
							</a>
							<a href="/login" class="btn btn-sm variant-ghost-surface">
								<span><AccountArrowDown size={30} /></span>
								<span>Login</span>
							</a>
                            {/if}
					
					{/snippet}
			</AppBar>
		
	{/snippet}
	<!-- Page Route Content -->
	{@render children?.()}
</AppShell>
