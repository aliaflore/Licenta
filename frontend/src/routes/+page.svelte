<script lang="ts">
	import type { PageData } from "./$types";
	import Chart from "../lib/Chart.svelte";

    interface Props {
        data: PageData;
    }

    let { data }: Props = $props();
    import { onMount } from 'svelte';
    import { DateInput } from 'date-picker-svelte';
    import { writable } from 'svelte/store';
	import { viewAsUser } from "$lib";
	import AnalysesList from "$lib/AnalysesList.svelte";

    let startDate = writable(new Date());
    let endDate = writable(new Date());

    const setLastYear = () => {
        const now = new Date();
        startDate.set(new Date(now.getFullYear() - 1, now.getMonth(), now.getDate()));
        endDate.set(now);
    };

    const setLastSixMonths = () => {
        const now = new Date();
        startDate.set(new Date(now.getFullYear(), now.getMonth() - 6, now.getDate()));
        endDate.set(now);
    };

    onMount(() => {
        setLastYear();
    });
</script>

<div class="flex h-full border-t border-gray-300">
    <div class="basis-[10%] grow shrink"></div>
    <div class="grow shrink basis-[20%] flex w-full table-container flex-col items-center">

        <h1 class="h1 pt-20">Istoricul Analizelor</h1>
        <div class="w-full h-full flex items-center justify-start flex-col gap-2 mt-20">
            {#each data.analyses.results || [] as item}
                <a href={item.file} class="w-full">
                    <div class="bg-surface-50 w-full p-4 card shadow-sm">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                                <div class="text-lg font-bold">{item.taken_on}</div>
                                <!-- <div class="text-sm text-gray-500">{item.analysis_id}</div> -->
                            </div>
                            <div class="text-sm text-gray-500">{item.provider.name}</div>
                        </div>
                    </div>
                </a>    
            {/each}
        </div>
    </div>

	<div
		class="grow shrink basis-[70%] flex items-center justify-center overflow-x-hidden overflow-y-scroll h-[90vh] pt-60"
	>

        <div class="flex items-center w-full flex-col gap-2">
            {#each data.history as item}
            <div class="bg-surface-50">
                <Chart data={item} />
            </div>
            {/each}
        </div>
    </div>
</div>


