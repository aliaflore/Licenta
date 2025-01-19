<script lang="ts">
    import moment from 'moment';

    import { reload } from './load';

    import { Datatable, Pagination, RowCount, RowsPerPage, type State, TableHandler, ThSort } from '@vincjo/datatables/server'
	import { onMount } from 'svelte';
	import type { PatientInvite } from '$lib/types';

    const table = new TableHandler<PatientInvite>([], { rowsPerPage: 10 })

    table.load((state: State) => reload(state));

    onMount(() => {
        table.invalidate();
    });

    const search = table.createSearch();
</script>

<div class="flex justify-center align-middle">
    <div class="table-container m-10 w-auto max-w-5xl">
        <div class="table-container !table-comfortable !table-hover">
            <Datatable {table}>
                {#snippet header()}
                    <input
                        bind:value={search.value}
                        oninput={() => search.set()}
                        placeholder={table.i18n.search}
                        spellcheck="false"
                        class="input"
                    />
                    <RowsPerPage {table}/>
                {/snippet}
                <table class="table">
                    <thead>
                        <tr>
                            <ThSort {table} field="pk">ID</ThSort>
                            <th>Email</th>
                            <th>First Name</th>
                            <th>Last Name</th>
                            <th>Full Name</th>
                            <ThSort {table} field="accepted">Accepted</ThSort>
                            <ThSort {table} field="expires">Expires</ThSort>
                            <th class="text-center">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each table.rows as row}
                            <tr>
                                <td>{row.pk}</td>
                                <td>{row.patient.email}</td>
                                <td>{row.patient.first_name}</td>
                                <td>{row.patient.last_name}</td>
                                <td>{row.patient.full_name}</td>
                                <td>
                                    {#if row.accepted}
                                        <div class="text-green">Yes</div>
                                        <div class="text-gray-500 ml-2">{moment(row.accepted_on).from(moment(new Date()))}</div>
                                    {:else}
                                        <div class="text-red">No</div>
                                    {/if}
                                </td>
                                <td>
                                    {#if row.expires}
                                        <div class="flex flex-row">
                                            {moment(row.expires).format("ddd MMM DD YYYY")}
                                        </div>
                                        <div class="text-gray-500 ml-2">{moment(row.expires).from(moment(new Date()))}</div>
                                    {:else}
                                        <div class="text-red-500">No date</div>
                                    {/if}
                                </td>
                                <td>
                                    assad
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