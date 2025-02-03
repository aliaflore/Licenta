<script lang="ts">
    import Check from 'svelte-material-icons/Check.svelte';
    import AccountRemove from 'svelte-material-icons/AccountRemove.svelte';
    import moment from 'moment';
    import type { ActionData } from './$types';

    let { form }: { form: ActionData } = $props();

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
                                    <div class="flex flex-row w-auto h-auto gap-1">
                                        {#if !row.accepted}
                                        <form method="POST" action="?/accept">
                                            <input type="hidden" name="pk" value={row.pk} />
                                            <button type="submit" class="btn-icon btn-sm bg-yellow-500 [&>*]:pointer-events-none">
                                                <Check size={24} />
                                            </button>
                                        </form>
                                        {:else}
                                        <form method="POST" action="?/delete">
                                            <input type="hidden" name="pk" value={row.pk} />
                                            <button type="submit" class="btn-icon btn-sm bg-green-500 [&>*]:pointer-events-none">
                                                <AccountRemove size={24} />
                                            </button>
                                        </form>
                                        {/if}
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
