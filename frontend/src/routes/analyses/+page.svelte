<script lang="ts">
    import type { PageData } from './$types';
    import FileDocument from 'svelte-material-icons/FileDocument.svelte';
    import Play from 'svelte-material-icons/Play.svelte';
    export let data: PageData;

    import moment from 'moment';

    import { popup } from '@skeletonlabs/skeleton';
    import type { PopupSettings } from '@skeletonlabs/skeleton';

    import type { State } from '@vincjo/datatables/remote';

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

    export let parsedData = data.analyses || [];
    for (let i = 0; i < parsedData.length; i++) {
        parsedData[i].created = new Date(parsedData[i].created);
    }
</script>

<div class="table-container m-10">
	<table class="table table-hover">
		<thead>
			<tr>
				<th>Document ID</th>
				<th>Uploaded On</th>
				<th>Provider</th>
				<th>Taken On</th>
				<th>AI Suggestion</th>
				<th>Doctor Notes</th>
				<th>Actions</th>
			</tr>
		</thead>
		<tbody>
            {#each parsedData as analysis}
				<tr>
                    <td>{analysis.pk}</td>
					<td>
                        <div class="flex flex-row">
                            {moment(analysis.created).toLocaleString()}
                        </div>
                        <div class="text-gray-500 ml-2">{moment(analysis.created).from(moment(new Date()))}</div>
                    </td>
					<td>{analysis.provider.name}</td>
					<td>
                        {#if analysis.taken_on}
                            <div class="flex flex-row">
                                {moment(analysis.taken_on).format("ddd MMM DD YYYY")}
                            </div>
                            <div class="text-gray-500 ml-2">{moment(analysis.taken_on).from(moment(new Date()))}</div>
                        {:else}
                            <div class="text-red-500">No date</div>
                        {/if}
                    </td>
					<td>
                        {#if analysis.suggestion}
                            <div class="text-green-500">Yes</div>
                        {:else}
                            <div class="text-red-500">No</div>
                        {/if}
                    </td>
					<td>
                        {#if analysis.doctor_notes}
                            <div class="text-green-300">{analysis.doctor_notes}</div>
                        {:else}
                            No notes
                        {/if}
                    </td>
                    <td class="text-right">
                        <div class="card p-4 shadow-xl" data-popup="popupDocument">
                            <div><p>View Document</p></div>
                        </div>
                        <a href={analysis.file} class="btn-icon btn-sm bg-green-500 [&>*]:pointer-events-none" use:popup={popupDocument}>
                            <FileDocument size={24} />
                        </a>
                        <div class="card p-4 shadow-xl" data-popup="popupInspect">
                            <div><p>Inspect the Analyses</p></div>
                        </div>
                        <a href={`/analysis/${analysis.pk}`} target="_blank" class="btn-icon btn-sm bg-blue-500 [&>*]:pointer-events-none" use:popup={popupInspect}>
                            <Play size={24} />
                        </a>
                    </td>
				</tr>
            {/each}
		</tbody>
		<tfoot>
            <tr>
                <td colspan="7" class="text-center">
                    <div class="pagination">
                        {#if data.page > 3}
                            <a href="?page=1" class="btn btn-sm rounded">1</a>
                            {#if data.page > 4}
                                <span class="btn btn-sm rounded">...</span>
                            {/if}
                        {/if}


                        {#each Array(data?.totalPages).fill(0).map((_, i) => i + 1) as page (page)}
                            {#if page === data.page || (page >= data.page - 2 && page <= data.page + 2)}
                                <a href={`?page=${page}`} class="btn btn-sm rounded {page === data.page ? 'bg-blue-500 text-white' : ''}">{page}</a>
                            {/if}
                        {/each}

                        {#if data.page < data.totalPages - 2}
                            {#if data.page < data.totalPages - 3}
                                <span class="btn btn-sm rounded">...</span>
                            {/if}
                            <a href={`?page=${data.totalPages}`} class="btn btn-sm rounded">{data.totalPages}</a>
                        {/if}
                    </div>
                </td>
            </tr>
		</tfoot>
	</table>
</div>
