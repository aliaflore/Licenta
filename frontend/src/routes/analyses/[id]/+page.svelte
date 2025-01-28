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
		TableHandler,
		ThFilter,
		ThSort
	} from '@vincjo/datatables';
	import type { PageData } from './$types';
	import type { AnalysisResult } from '$lib/types';
	import Play from 'svelte-material-icons/Play.svelte';
	import { Accordion, AccordionItem, Tab, TabGroup } from '@skeletonlabs/skeleton';
	import Chart from '$lib/Chart.svelte';

	export let data: PageData;

	const table = new TableHandler<AnalysisResult>(data.analysis.results, { rowsPerPage: 100 });

	let tabSet: number = 0;
</script>

<div class="flex h-full border-t border-gray-300">
	<div class="flex-1 flex items-center justify-center border-r border-gray-300">
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
					<div class="flex items-center w-full flex-col gap-2">
						{#each data.historyData as item}
							<div class="bg-white">
								<Chart data={item} height="h-60" width="w-[40vw]" />
							</div>
						{/each}
					</div>
				{:else if tabSet === 1}
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
									{#if result.suggestion}
										{result.suggestion}
									{:else}
										<div class="text-gray-200">No suggestions</div>
									{/if}
								</svelte:fragment>
							</AccordionItem>
						{/each}
					</Accordion>
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
