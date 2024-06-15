<script lang="ts">
	import FileUpload from 'svelte-material-icons/FileUpload.svelte';
	import CheckBold from 'svelte-material-icons/CheckBold.svelte';
	import { FileDropzone } from '@skeletonlabs/skeleton';
	import { enhance } from '$app/forms';
	let files: FileList;
	let filesRa: FileList;
	function onChangeHandler(e: Event): void {
		console.log('file data:', e);
		console.log(files);
	}
	function onChangeHandlerRadio(e: Event): void {
		console.log('file data:', e);
		console.log(files);
	}
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="text-center flex flex-col items-center">
		<h2 class="h2">Incarca fisierele in functie de nevoile tale</h2>
		<form
			method="post"
			use:enhance
			enctype="multipart/form-data"
			class="text-center flex flex-col items-center gap-2 mt-10"
		>
			<div class="flex flex-row items-center gap-2">
				<div class="flex justify-center flex-col gap-2">
					<FileDropzone name="dropzoneAnalize" on:change={onChangeHandler} bind:files>
						<svelte:fragment slot="lead"
							><div class="flex justify-center align-center">
								<FileUpload size={100} />
							</div></svelte:fragment
						>
						<svelte:fragment slot="message">
							{#if !files?.length}
								Incarca analiza
							{:else}
								Analiza incarcata
							{/if}
						</svelte:fragment>
						<svelte:fragment slot="meta">
							{#if !files?.length}
								doar fisiere de tipul PDF
							{:else}
								{files[0].name}
							{/if}
						</svelte:fragment>
					</FileDropzone>

					<select name="select_for_analysis" class="select">
						<option value="1">Arcadia</option>
						<option value="2">Regina Maria</option>
						<option value="3">Synevo</option>
					</select>
				</div>
				<div class="flex justify-center flex-col gap-2">
					<FileDropzone name="dropzoneRadiografii" on:change={onChangeHandlerRadio} bind:filesRa>
						<svelte:fragment slot="lead"
							><div class="flex justify-center align-center">
								<FileUpload size={100} />
							</div></svelte:fragment
						>
						<svelte:fragment slot="message">
							{#if !filesRa?.length}
								Incarca Radiografia
							{:else}
								Radiografia incarcata
							{/if}
						</svelte:fragment>
						<svelte:fragment slot="meta">
							{#if !filesRa?.length}
								doar fisiere de tipul PDF
							{:else}
								{filesRa[0].name}
							{/if}
						</svelte:fragment>
					</FileDropzone>
					<select name="select_for_analysis" class="select">
						<option value="1">Arcadia</option>
						<option value="2">Regina Maria</option>
						<option value="3">Synevo</option>
					</select>
				</div>
			</div>
			<button type="submit" class="btn btn-sm variant-ghost-surface h-8 mt-4"><CheckBold /></button>
		</form>
	</div>
</div>
