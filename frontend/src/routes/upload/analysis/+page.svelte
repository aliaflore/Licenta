<script lang="ts">
	import type { PageData, ActionData } from './$types';
	import { FileDropzone } from '@skeletonlabs/skeleton';
    import FileUpload from 'svelte-material-icons/FileUpload.svelte';
    export let data: PageData;
    export let form: ActionData;

    let file: FileList;
</script>

<div class="flex justify-center items-center min-h-full">
	<div class="w-full max-w-lg bg-transparent shadow-lg rounded-lg card p-6">
		<h1 class="text-xl font-semibold text-center mb-4">
			Incarca fisierele in functie de nevoile tale
		</h1>

		<form method="post" enctype="multipart/form-data" class="flex flex-col gap-4">
            <div class="mb-4">
                <label class="block mb-2 font-medium">Provider</label>
                {#each form?.errors?.provider_id || [] as error}
                    <p class="text-red-500 text-sm">{error}</p>
                {/each}
                <select
                    class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none bg-surface-600"
                    name="provider_id"
                >
                    <option value="" disabled selected>Select a provider</option>
                    {#each data.analysisProviders || [] as provider}
                        <option value={provider.name}>{provider.name}</option>
                    {/each}
                </select>
            </div>

			<div class="mb-4">
				<label class="block mb-2 font-medium">Taken on</label>
                {#each form?.errors?.taken_on || [] as error}
                    <p class="text-red-500 text-sm">{error}</p>
                {/each}
				<input
					type="date"
                    name="taken_on"
					class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none bg-surface-600"
                    required
				/>
			</div>

			<div class="mb-4">
				<label class="block mb-2 font-medium">Doctor Notes</label>
                {#each form?.errors?.doctor_notes || [] as error}
                    <p class="text-red-500 text-sm">{error}</p>
                {/each}
				<textarea
                    name="doctor_notes"
					class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none bg-surface-600"
				></textarea>
            </div>

            {#each form?.errors?.file || [] as error}
                <p class="text-red-500 text-sm">{error}</p>
            {/each}
            <FileDropzone name="file" class="mb-4" bind:files={file} required accept="application/pdf">
                <svelte:fragment slot="lead">
                    <div class="flex justify-center align-center">
                        <FileUpload size={80} />
                    </div>
                </svelte:fragment>
                <svelte:fragment slot="message">
                    <p class="text-center">Drop files here or click to upload</p>
                    <p class="text-center text-secondary-100 text-sm">Accepts only PDF files</p>
                </svelte:fragment>
                <svelte:fragment slot="meta">
                    {#if file?.length}
                        <p class="text-center">{file[0].name}</p>
                    {/if}
                </svelte:fragment>
            </FileDropzone>

			<button
				type="submit"
				class="w-full bg-blue-500 text-white rounded-lg px-4 py-2 hover:bg-blue-600"
			>
				Submit
			</button>
		</form>
	</div>
</div>
