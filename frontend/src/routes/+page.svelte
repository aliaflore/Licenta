<script lang="ts">
	import type { PageData } from './$types';
	import Chart from '../lib/Chart.svelte';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();
	import { onMount } from 'svelte';
	import { DateInput } from 'date-picker-svelte';
	import { writable } from 'svelte/store';
	import { viewAsUser } from '$lib';
	import AnalysesList from '$lib/AnalysesList.svelte';

	let startDate = writable(new Date());
	let endDate = writable(new Date());

	const setLastYear = () => {
		const now = new Date();
		startDate.set(new Date(now.getFullYear() - 1, now.getMonth(), now.getDate()));
		endDate.set(now);
	};

	const setLastSixMonths = () => {
		const now = new Date();
		startDate.set(new Date(now.getFullYear(), now.getMonth() - 6, now.getDate()));
		endDate.set(now);
	};

	onMount(() => {
		setLastYear();
	});
</script>

{#if data.user}
	<div class="flex h-full border-t border-gray-300">
		<div class="basis-[10%] grow shrink"></div>
		<div class="grow shrink basis-[20%] flex w-full table-container flex-col items-center">
			<h1 class="h1 pt-20">Istoricul Analizelor</h1>
			<div class="w-full h-full flex items-center justify-start flex-col gap-2 mt-20">
				{#each data.analyses.results || [] as item}
					<a href={item.file} class="w-full">
						<div class="bg-surface-50 w-full p-4 card shadow-sm">
							<div class="flex items-center justify-between">
								<div class="flex items-center gap-2">
									<div class="text-lg font-bold">{item.taken_on}</div>
									<!-- <div class="text-sm text-gray-500">{item.analysis_id}</div> -->
								</div>
								<div class="text-sm text-gray-500">{item.provider.name}</div>
							</div>
						</div>
					</a>
				{/each}
			</div>
		</div>

		<div
			class="grow shrink basis-[70%] flex items-center justify-center overflow-x-hidden overflow-y-scroll h-[90vh] pt-60"
		>
			<div class="flex items-center w-full flex-col gap-2">
				{#each data.history as item}
					<div class="bg-surface-50">
						<Chart data={item} />
					</div>
				{/each}
			</div>
		</div>
	</div>
{:else}
	<section class="bg-gray-50 h-full flex items-center justify-center px-6">
		<div class="max-w-7xl text-center">
			<h1 class="h1">
				Welcome to <span class="text-blue-600">Licenta</span>
			</h1>
			<p class="mt-4 text-lg text-gray-600">
				A platform that empowers users and doctors to collaborate on health analyses.
			</p>

			<div class="grid gap-8 mt-8 md:grid-cols-2">
				<!-- User Features -->
				<div class="p-6 bg-white shadow-lg rounded-2xl">
					<h2 class="text-2xl font-semibold text-blue-600">For Users</h2>
					<ul class="mt-4 space-y-2 text-left">
						<li class="flex items-center">
							<svg
								class="h-5 w-5 text-green-500 mr-2"
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 20 20"
								fill="currentColor"
							>
								<path
									fill-rule="evenodd"
									d="M16.707 5.293a1 1 0 00-1.414 0L9 11.586 6.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l7-7a1 1 0 000-1.414z"
									clip-rule="evenodd"
								/>
							</svg>
							Upload analyses and radiographies
						</li>
						<li class="flex items-center">
							<svg
								class="h-5 w-5 text-green-500 mr-2"
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 20 20"
								fill="currentColor"
							>
								<path
									fill-rule="evenodd"
									d="M16.707 5.293a1 1 0 00-1.414 0L9 11.586 6.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l7-7a1 1 0 000-1.414z"
									clip-rule="evenodd"
								/>
							</svg>
							AI-generated suggestions for abnormal values
						</li>
						<li class="flex items-center">
							<svg
								class="h-5 w-5 text-green-500 mr-2"
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 20 20"
								fill="currentColor"
							>
								<path
									fill-rule="evenodd"
									d="M16.707 5.293a1 1 0 00-1.414 0L9 11.586 6.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l7-7a1 1 0 000-1.414z"
									clip-rule="evenodd"
								/>
							</svg>
							Doctor's notes for deeper insights
						</li>
						<li class="flex items-center">
							<svg
								class="h-5 w-5 text-green-500 mr-2"
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 20 20"
								fill="currentColor"
							>
								<path
									fill-rule="evenodd"
									d="M16.707 5.293a1 1 0 00-1.414 0L9 11.586 6.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l7-7a1 1 0 000-1.414z"
									clip-rule="evenodd"
								/>
							</svg>
							Import results from Synevo and Regina Maria
						</li>
					</ul>
				</div>

				<!-- Doctor Features -->
				<div class="p-6 bg-white shadow-lg rounded-2xl">
					<h2 class="text-2xl font-semibold text-blue-600">For Doctors</h2>
					<ul class="mt-4 space-y-2 text-left">
						<li class="flex items-center">
							<svg
								class="h-5 w-5 text-green-500 mr-2"
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 20 20"
								fill="currentColor"
							>
								<path
									fill-rule="evenodd"
									d="M16.707 5.293a1 1 0 00-1.414 0L9 11.586 6.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l7-7a1 1 0 000-1.414z"
									clip-rule="evenodd"
								/>
							</svg>
							Invite users as patients
						</li>
						<li class="flex items-center">
							<svg
								class="h-5 w-5 text-green-500 mr-2"
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 20 20"
								fill="currentColor"
							>
								<path
									fill-rule="evenodd"
									d="M16.707 5.293a1 1 0 00-1.414 0L9 11.586 6.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l7-7a1 1 0 000-1.414z"
									clip-rule="evenodd"
								/>
							</svg>
							Edit and approve analysis results
						</li>
						<li class="flex items-center">
							<svg
								class="h-5 w-5 text-green-500 mr-2"
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 20 20"
								fill="currentColor"
							>
								<path
									fill-rule="evenodd"
									d="M16.707 5.293a1 1 0 00-1.414 0L9 11.586 6.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l7-7a1 1 0 000-1.414z"
									clip-rule="evenodd"
								/>
							</svg>
							Add personalized notes to analyses
						</li>
						<li class="flex items-center">
							<svg
								class="h-5 w-5 text-green-500 mr-2"
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 20 20"
								fill="currentColor"
							>
								<path
									fill-rule="evenodd"
									d="M16.707 5.293a1 1 0 00-1.414 0L9 11.586 6.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l7-7a1 1 0 000-1.414z"
									clip-rule="evenodd"
								/>
							</svg>
							Accept or modify AI suggestions
						</li>
					</ul>
				</div>
			</div>
		</div>
	</section>
{/if}
