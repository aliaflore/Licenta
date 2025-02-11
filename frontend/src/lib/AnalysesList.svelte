<script lang="ts">
	import FileDocument from 'svelte-material-icons/FileDocument.svelte';
	import Play from 'svelte-material-icons/Play.svelte';
	import moment from 'moment';
	import { ConicGradient, popup } from '@skeletonlabs/skeleton';
	import type { ConicStop, PopupSettings } from '@skeletonlabs/skeleton';

	import { reload } from './AnalysesListLoad';

	import {
		Datatable,
		Pagination,
		RowCount,
		RowsPerPage,
		type State,
		TableHandler,
		ThSort
	} from '@vincjo/datatables/server';
	import type { AnalysisPDF, User } from '$lib/types';
	import { onMount } from 'svelte';

    export let viewAsUser: User | null;

	const table = new TableHandler<AnalysisPDF>([], { rowsPerPage: 10 });

	table.load((state: State) => reload(state, viewAsUser));

	onMount(() => {
		table.invalidate();
	});

	const popupDocument: PopupSettings = {
		event: 'hover',
		target: 'popupDocument',
		placement: 'top'
	};
	const popupInspect: PopupSettings = {
		event: 'hover',
		target: 'popupInspect',
		placement: 'top'
	};
	const conicStops: ConicStop[] = [
		{ color: 'transparent', start: 0, end: 25 },
		{ color: 'rgb(var(--color-surface-500))', start: 75, end: 100 }
	];

    export let columns = {
        'id': true,
        'uploaded_on': true,
        'provider': true,
        'taken_on': true,
        'suggestion': true,
        'doctor_notes': true,
        'actions': true
    };
</script>

<div class="table-container m-10 w-auto max-w-5xl">
	<div class="table-container !table-comfortable !table-hover">
		<Datatable {table}>
			{#snippet header()}
				<div></div>
				<RowsPerPage {table} />
			{/snippet}
			<table class="table">
				<thead>
					<tr>
                        {#if columns.id} 
						<ThSort {table} field="pk">ID</ThSort>
                        {/if}
                        {#if columns.uploaded_on}
						<ThSort {table} field="created">Uploaded On</ThSort>
                        {/if}
                        {#if columns.provider}
						<th>Provider</th>
                        {/if}
                        {#if columns.taken_on}
						<ThSort {table} field="taken_on">Taken On</ThSort>
                        {/if}
                        {#if columns.suggestion}
						<th>AI Suggestion</th>
                        {/if}
                        {#if columns.doctor_notes}
						<th>Doctor Notes</th>
                        {/if}
                        {#if columns.actions}
						<th>Actions</th>
                        {/if}
					</tr>
				</thead>
				<tbody>
					{#each table.rows as row}
						<tr>
                            {#if columns.id}
							<td>{row.pk}</td>
                            {/if}
                            {#if columns.uploaded_on}
							<td>
								<div class="flex flex-row">
									{moment(row.created).toLocaleString()}
								</div>
								<div class="text-gray-500 ml-2">{moment(row.created).from(moment(new Date()))}</div>
							</td>
                            {/if}
                            {#if columns.provider}
							<td>{row.provider.name}</td>
                            {/if}
                            {#if columns.taken_on}
							<td>
								{#if row.taken_on}
									<div class="flex flex-row">
										{moment(row.taken_on).format('ddd MMM DD YYYY')}
									</div>
									<div class="text-gray-500 ml-2">
										{moment(row.taken_on).from(moment(new Date()))}
									</div>
								{:else}
									<div class="text-red-500">No date</div>
								{/if}
							</td>
                            {/if}
                            {#if columns.suggestion}
							<td>
								{#if row.suggestion}
									<div class="text-green text-center">Yes</div>
								{:else}
									<div class="text-red text-center">No</div>
								{/if}
							</td>
                            {/if}
                            {#if columns.doctor_notes}
							<td>
								{#if row.doctor_notes}
									<div class="text-green-300">{row.doctor_notes}</div>
								{:else}
									No notes
								{/if}
							</td>
                            {/if}
                            {#if columns.actions}
							<td>
								<div class="flex flex-row w-auto h-auto gap-1">
									<div class="card p-4 shadow-xl" data-popup="popupDocument">
										<div><p>View Document</p></div>
									</div>
									<a
										href={row.file}
										target="_blank"
										class="btn-icon btn-sm bg-green-500 [&>*]:pointer-events-none"
										use:popup={popupDocument}
									>
										<FileDocument size={24} />
									</a>
									{#if !!row.analysis_id}
										<div class="card p-4 shadow-xl" data-popup="popupInspect">
											<div><p>Inspect the Analyses</p></div>
										</div>

										{#if viewAsUser}
											<a
												href={`/analyses/${row.analysis_id}?user=${viewAsUser.pk}`}
												class="btn-icon btn-sm bg-blue-500 [&>*]:pointer-events-none"
												use:popup={popupInspect}
											>
												<Play size={24} />
											</a>
										{:else}
											<a
												href={`/analyses/${row.analysis_id}`}
												class="btn-icon btn-sm bg-blue-500 [&>*]:pointer-events-none"
												use:popup={popupInspect}
											>
												<Play size={24} />
											</a>
										{/if}
									{:else}
										<div class="card p-4 shadow-xl" data-popup="popupInspect">
											<div><p>Not yet analyzed</p></div>
										</div>
										<btn
											disabled
											class="btn-icon btn-sm [&>*]:pointer-events-none"
											use:popup={popupInspect}
										>
											<ConicGradient stops={conicStops} spin width="w-10" />
										</btn>
									{/if}
								</div>
							</td>
                            {/if}
						</tr>
					{/each}
				</tbody>
			</table>
			{#snippet footer()}
				<RowCount {table} />
				<Pagination {table} />
			{/snippet}
		</Datatable>
	</div>
</div>
