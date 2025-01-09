<script lang="ts">
	import { Datatable, Pagination, RowCount, TableHandler, ThFilter, ThSort } from '@vincjo/datatables';
    import type { PageData } from './$types';
	import type { AnalysisResult } from '$lib/types';
    import Play from 'svelte-material-icons/Play.svelte';

    export let data: PageData;

    const table = new TableHandler<AnalysisResult>(data.analysis.results, { rowsPerPage: 5 })
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
    </div>
  </div>