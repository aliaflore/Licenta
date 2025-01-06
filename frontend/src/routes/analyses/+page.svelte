<script lang="ts">
    import type { PageData } from './$types';
    import FileDocument from 'svelte-material-icons/FileDocument.svelte';
    import Play from 'svelte-material-icons/Play.svelte';
    import moment from 'moment';
    import { popup } from '@skeletonlabs/skeleton';
    import type { PopupSettings } from '@skeletonlabs/skeleton';

    import { reload } from './load';

    import { Datatable, Pagination, RowCount, RowsPerPage, type State, TableHandler, ThSort } from '@vincjo/datatables/server'
	import type { AnalysisPDF } from '$lib/types';
	import { onMount } from 'svelte';

    const table = new TableHandler<AnalysisPDF>([], { rowsPerPage: 10 })

    table.load((state: State) => reload(state));

    onMount(() => {
        table.invalidate();
    });

    const popupDocument: PopupSettings = {
        event: 'hover',
        target: 'popupDocument',
        placement: 'top',
    };
    const popupInspect: PopupSettings = {
        event: 'hover',
        target: 'popupInspect',
        placement: 'top',
    };
</script>

<div class="flex justify-center align-middle">
    <div class="table-container m-10 w-auto max-w-5xl">
        <div class="table-container">
            <Datatable {table}>
                {#snippet header()}
                    <div></div>
                    <RowsPerPage {table}/>
                {/snippet}
                <table class="table">
                    <thead>
                        <tr>
                            <ThSort {table} field="pk">ID</ThSort>
                            <ThSort {table} field="created">Uploaded On</ThSort>
                            <th>Provider</th>
                            <ThSort {table} field="taken_on">Taken On</ThSort>
                            <th>AI Suggestion</th>
                            <th>Doctor Notes</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each table.rows as row}
                            <tr class="hover:text-black">
                                <td>{row.pk}</td>
                                <td>
                                    <div class="flex flex-row">
                                        {moment(row.created).toLocaleString()}
                                    </div>
                                    <div class="text-gray-500 ml-2">{moment(row.created).from(moment(new Date()))}</div>
                                </td>
                                <td>{row.provider.name}</td>
                                <td>
                                    {#if row.taken_on}
                                        <div class="flex flex-row">
                                            {moment(row.taken_on).format("ddd MMM DD YYYY")}
                                        </div>
                                        <div class="text-gray-500 ml-2">{moment(row.taken_on).from(moment(new Date()))}</div>
                                    {:else}
                                        <div class="text-red-500">No date</div>
                                    {/if}
                                </td>
                                <td>
                                    {#if row.suggestion}
                                        <div class="text-green text-center">Yes</div>
                                    {:else}
                                        <div class="text-red text-center">No</div>
                                    {/if}
                                </td>
                                <td>
                                    {#if row.doctor_notes}
                                        <div class="text-green-300">{row.doctor_notes}</div>
                                    {:else}
                                        No notes
                                    {/if}
                                </td>
                                <td class="text-right">
                                    <div class="card p-4 shadow-xl" data-popup="popupDocument">
                                        <div><p>View Document</p></div>
                                    </div>
                                    <a href={row.file} class="btn-icon btn-sm bg-green-500 [&>*]:pointer-events-none" use:popup={popupDocument}>
                                        <FileDocument size={24} />
                                    </a>
                                    <div class="card p-4 shadow-xl" data-popup="popupInspect">
                                        <div><p>Inspect the Analyses</p></div>
                                    </div>
                                    <a href={`/analysis/${row.pk}`} target="_blank" class="btn-icon btn-sm bg-blue-500 [&>*]:pointer-events-none" use:popup={popupInspect}>
                                        <Play size={24} />
                                    </a>
                                </td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
                {#snippet footer()}
                    <RowCount {table}/>
                    <Pagination {table}/>
                {/snippet}
            </Datatable>
        </div>
    </div>
</div>