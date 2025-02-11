<script lang="ts">
    import FileDocument from 'svelte-material-icons/FileDocument.svelte';
    import moment from 'moment';
    import { popup } from '@skeletonlabs/skeleton';
    import type { ConicStop, PopupSettings } from '@skeletonlabs/skeleton';

    import { reload } from './load';

    import { Datatable, Pagination, RowCount, RowsPerPage, type State, TableHandler, ThSort } from '@vincjo/datatables/server'
	import type { RadiographyPDF } from '$lib/types';
	import { onMount } from 'svelte';
	import { viewAsUser } from '$lib';

    const table = new TableHandler<RadiographyPDF>([], { rowsPerPage: 10 })

    table.load((state: State) => reload(state, $viewAsUser));

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
    const conicStops: ConicStop[] = [
        { color: 'transparent', start: 0, end: 25 },
        { color: 'rgb(var(--color-surface-500))', start: 75, end: 100 }
    ];
</script>

<div class="flex justify-center align-middle">
    <div class="table-container m-10 w-auto max-w-5xl">
        <div class="table-container !table-comfortable !table-hover">
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
                            <th>Doctor Notes</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each table.rows as row}
                            <tr>
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
                                    {#if row.doctor_notes}
                                        <div class="text-green-300">{row.doctor_notes}</div>
                                    {:else}
                                        No notes
                                    {/if}
                                </td>
                                <td>
                                    <div class="flex flex-row w-auto h-auto gap-1">
                                        <div class="card p-4 shadow-xl" data-popup="popupDocument">
                                            <div><p>View Document</p></div>
                                        </div>
                                        <a href={row.file} target="_blank" class="btn-icon btn-sm bg-green-500 [&>*]:pointer-events-none" use:popup={popupDocument}>
                                            <FileDocument size={24} />
                                        </a>
                                    </div>
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