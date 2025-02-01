<script module lang="ts">
	export function getPageTitle(d: URL) {
		return 'Analysis ' + d.pathname.split('/').pop();
	}
</script>

<script lang="ts">
	import Check from 'svelte-material-icons/Check.svelte';
	import Close from 'svelte-material-icons/Close.svelte';
	import Help from 'svelte-material-icons/Help.svelte';

	import {
		Datatable,
		Pagination,
		RowCount,
		Search,
		TableHandler,
		ThFilter,
		ThSort
	} from '@vincjo/datatables';
	import type { ActionData, PageData } from './$types';
	import type { AnalysisResult, HistoryData } from '$lib/types';
	import Play from 'svelte-material-icons/Play.svelte';
	import { Accordion, AccordionItem, Tab, TabGroup } from '@skeletonlabs/skeleton';
	import Chart from '$lib/Chart.svelte';
	import { enhance } from '$app/forms';
	import { fade } from 'svelte/transition';

	export let data: PageData;
	export let form: ActionData;

	const table = new TableHandler<AnalysisResult>(data.analysis.results, { rowsPerPage: 100 });

	let tabSet: number = 0;

	let selectedAnalysisHistory: HistoryData | undefined = undefined;
	let selectedAnalysis: AnalysisResult | null = null;

	let selectAnalysis = (pk: number, category: string, name: string) => {
		const user = new URL(document.location.toString()).searchParams.get('user');
		tabSet = 0;
		selectedAnalysisHistory = data.historyData.find(
			(r) => r.category.name === category && r.name === name
		);
		fetch(`/api/analysis-results/${pk}/` + (user ? `?user=${user}` : ''))
			.then((res) => res.json())
			.then((res) => {
				selectedAnalysis = res as AnalysisResult;
			});
	};

    let notification: HTMLElement | null = null;

    $: if (notification && form) {
        setTimeout(() => {
            form.edit_ok = false;
        }, 2000);
    }
</script>

<div class="flex h-full border-t border-gray-300">
	<div
		class="flex-1 flex items-center justify-center border-r border-gray-300 overflow-x-hidden overflow-y-scroll h-[90vh] pl-3 pr-2"
	>
		{#if !data.user?.is_doctor}
			<iframe
				src={`${data.analysis.source.file}#zoom=FitW`}
				class="w-full h-full"
				title="PDF Viewer"
				frameborder="0"
			>
			</iframe>
		{:else}
			<Datatable basic {table}>
				<table class="table table-compact !table-hover !w-[50vw]">
					<thead>
						<tr>
							<ThSort {table} field="category">Category</ThSort>
							<ThSort {table} field="name">Name</ThSort>
							<th>Result</th>
							<th>Inspect</th>
						</tr>
					</thead>
					<tbody class="w-full">
						{#each table.rows as row}
							<tr>
								<td>
									{row.category.name}
								</td>
								<td>{row.name}</td>
								<td
									class={`hover:text-black ${row.range_min === null && row.range_max == null ? '' : row.in_range ? '!bg-green-900' : '!bg-red-900'}`}
								>
									{row.result}
									{row.measurement_unit}
								</td>
								<td class="text-center my-auto justify-center">
									<button
										onclick={() => selectAnalysis(row.pk, row.category.name, row.name)}
										class="btn-icon bg-green-500 [&>*]:pointer-events-none"
									>
										<Play size={24} />
									</button>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
				{#snippet footer()}
					<RowCount {table} />
					<Pagination {table} />
				{/snippet}
			</Datatable>
		{/if}
	</div>

	<div class="flex-1 flex items-start justify-start w-full table-container">
		<TabGroup
			justify="justify-center"
			active="variant-filled-primary"
			hover="hover:variant-soft-primary"
			flex="flex-1 lg:flex-none"
			rounded=""
			border=""
			class="bg-surface-100-800-token w-full"
		>
			<Tab bind:group={tabSet} name="tab1" value={0}>Analyses</Tab>
			<Tab bind:group={tabSet} name="tab2" value={1}>Suggestions</Tab>
			{#if !data.user?.is_doctor}
				<Tab bind:group={tabSet} name="tab3" value={2}>Rezultate</Tab>
			{/if}
			<svelte:fragment slot="panel">
				{#if tabSet === 0}
					<div class="flex items-center w-full flex-col gap-2 overflow-y-scroll h-[84vh]">
						{#if selectedAnalysisHistory}
							<div class="bg-white">
								<Chart data={selectedAnalysisHistory} height="h-60" width="w-[40vw]" />
							</div>
						{:else}
							<div class="text-gray-200">Select an analysis to view the history</div>
						{/if}

						{#if selectedAnalysis}
							{#if form?.edit_ok}
								<aside class="alert variant-filled-success absolute right-2 bottom-2" bind:this={notification} transition:fade={{ duration: 200 }}>
                                    <div class="alert-message">
                                        <p>Saved Analysis</p>
                                    </div>                            
                                </aside>
							{/if}

							<form
								class="flex flex-col gap-2 w-[30vw]"
								method="POST"
								action="?/edit"
								use:enhance={() => {
									return async ({ update }) => {
										update({ reset: false });
									};
								}}
							>
								<input type="hidden" name="pk" value={selectedAnalysis.pk} />
								<input type="hidden" name="viewas_user" value={data.viewAsUser} />
								<label class="label">
									<span>Result</span>
									<input
										name="result"
										class="input"
										type="text"
										placeholder="Result"
										value={selectedAnalysis.result}
									/>
								</label>
								<label class="label">
									<span>Measurement Unit</span>
									<input
										name="measurement_unit"
										class="input"
										type="text"
										placeholder="Measurement Unit"
										value={selectedAnalysis.measurement_unit}
									/>
								</label>
								<label class="label">
									<span>Minimum Range</span>
									<input
										name="range_min"
										class="input"
										type="number"
										placeholder="Minimum Range"
										value={selectedAnalysis.range_min}
									/>
								</label>
								<label class="label">
									<span>Minimum Range</span>
									<input
										name="range_max"
										class="input"
										type="number"
										placeholder="Maximum Range"
										value={selectedAnalysis.range_max}
									/>
								</label>
								<label class="label">
									<input
										name="in_range"
										class="checkbox"
										type="checkbox"
										placeholder="In Range"
										checked={selectedAnalysis.in_range}
									/>
									<span>In Range</span>
								</label>
								<label class="label">
									<input
										name="approve_ai_suggestion"
										class="checkbox"
										type="checkbox"
										placeholder="Approve AI Suggestion"
										checked={selectedAnalysis.approve_ai_suggestion}
									/>
									<span>Approve AI Suggestion</span>
								</label>
								<label class="label">
									<span>AI Suggestion</span>
									<textarea
										name="suggestion"
										class="textarea h-40 block"
										placeholder="AI Suggestion"
										value={selectedAnalysis.suggestion}
									></textarea>
								</label>
								<label class="label">
									<span>Doctor Note</span>
									<textarea
										name="doctor_note"
										class="textarea h-40 block"
										placeholder="Doctor Note"
										value={selectedAnalysis.doctor_note}
										disabled={!data.user?.is_doctor}
									></textarea>
								</label>
								<button class="btn btn-md bg-green-500" type="submit">Save</button>
							</form>
							<form
								class="flex flex-col gap-2 w-[30vw]"
								method="POST"
								action="?/regenerate"
								use:enhance
								onsubmit={() => window.location.reload()}
							>
								<input type="hidden" name="pk" value={selectedAnalysis.pk} />
								<input type="hidden" name="viewas_user" value={data.viewAsUser} />
								<button class="btn btn-md bg-green-500" type="submit"
									>Regenerate AI Suggestion</button
								>
							</form>
						{/if}
					</div>
				{:else if tabSet === 1}
					<div class="overflow-y-scroll h-[84vh]">
						<Accordion autocollapse>
							{#each data.analysis.results as result}
								<AccordionItem>
									<svelte:fragment slot="lead">
										{#if result.in_range}
											<Check size={24} />
										{:else if result.range_min !== null && result.range_max !== null}
											<Close size={24} />
										{:else}
											<Help size={24} />
										{/if}
									</svelte:fragment>
									<svelte:fragment slot="summary">
										{result.category.name} - {result.name}
									</svelte:fragment>
									<svelte:fragment slot="content">
										{#if result.suggestion && result.doctor_note}
											<b>AI Suggestion:</b>
                                            {#if result.approve_ai_suggestion}
                                                <b class="text-green-500">Approved by the Doctor</b>
                                            {:else}
                                                <b class="text-red-500">Not Approved by the Doctor</b>
                                            {/if}
                                            <br />
											{result.suggestion}
                                            <br />
                                            <br />
											<b>Doctor Notes:</b>
                                            <b class="text-red-500">Additional notes written by the Doctor</b>
                                            <br/>
											{result.doctor_note}
										{:else if result.suggestion}
											<b>AI Suggestion:</b> {result.suggestion}
										{:else if result.doctor_note}
											<b>Doctor Notes:</b> {result.doctor_note}
										{:else}
											<div class="text-gray-200">No suggestions</div>
										{/if}
									</svelte:fragment>
								</AccordionItem>
							{/each}
						</Accordion>
					</div>
				{:else if tabSet === 2}
					<Datatable basic {table}>
						<table class="table table-compact !table-hover !w-[50vw]">
							<thead>
								<tr>
									<ThSort {table} field="category">Category</ThSort>
									<ThSort {table} field="name">Name</ThSort>
									<th>Result</th>
									<th>Inspect</th>
								</tr>
							</thead>
							<tbody class="w-full">
								{#each table.rows as row}
									<tr>
										<td>
											{row.category.name}
										</td>
										<td>{row.name}</td>
										<td
											class={`hover:text-black ${row.range_min === null && row.range_max == null ? '' : row.in_range ? '!bg-green-900' : '!bg-red-900'}`}
										>
											{row.result}
											{row.measurement_unit}
										</td>
										<td class="flex justify-center">
											<div class="btn-icon bg-green-500 [&>*]:pointer-events-none">
												<Play size={24} />
											</div>
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
						{#snippet footer()}
							<RowCount {table} />
							<Pagination {table} />
						{/snippet}
					</Datatable>
				{/if}
			</svelte:fragment>
		</TabGroup>
	</div>
</div>
