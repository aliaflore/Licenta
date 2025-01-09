<script lang="ts">
	import { Datatable, Pagination, RowCount, TableHandler, ThFilter, ThSort } from '@vincjo/datatables';
    import type { PageData } from './$types';
	import type { AnalysisResult } from '$lib/types';
    import Play from 'svelte-material-icons/Play.svelte';
	import { Tab, TabGroup } from '@skeletonlabs/skeleton';

    export let data: PageData;

    const table = new TableHandler<AnalysisResult>(data.analysis.results, { rowsPerPage: 5 })

    let tabSet: number = 0;
</script>

<script module lang="ts">
    export function getPageTitle(d: URL) {
        return "Analysis " + d.pathname.split('/').pop()
    }
</script>

<div class="flex h-full border-t border-gray-300">
    <div class="flex-1 flex items-center justify-center border-r border-gray-300">
      <iframe 
        src={`${data.analysis.source.file}#zoom=FitW`}
        class="w-full h-full"
        title="PDF Viewer" 
        frameborder="0">
      </iframe>
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
            <Tab bind:group={tabSet} name="tab1" value={0}>(label 1)</Tab>
            <Tab bind:group={tabSet} name="tab2" value={1}>(label 2)</Tab>
            <Tab bind:group={tabSet} name="tab3" value={2}>Rezultate</Tab>
            <svelte:fragment slot="panel">
                {#if tabSet === 0}
                    dasa
                {:else if tabSet === 1}
                    asdasdas
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
                                        <td class={`hover:text-black ${(row.range_min === null && row.range_max == null) ? '' : (row.in_range ? '!bg-green-900' : '!bg-red-900')}`}>
                                            {row.result} {row.measurement_unit}
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
                            <RowCount {table}/>
                            <Pagination {table}/>
                        {/snippet}
                    </Datatable>
                {/if}
            </svelte:fragment>
        </TabGroup>
    </div>
  </div>