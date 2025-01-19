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

<div class="flex flex-col items-start p-4">
    <h2 class="text-lg font-bold mb-4">Filter Data</h2>
    <div class="mb-4">
        <label for="start-date" class="block mb-2">Start Date</label>
        <DateInput bind:value={$startDate} />
    </div>
    <div class="mb-4">
        <label for="end-date" class="block mb-2">End Date</label>
        <DateInput bind:value={$endDate} timePrecision={"minute"} />
    </div>
    <div class="flex flex-col gap-2">
        <button type="button" class="btn btn-sm variant-outline-primary" on:click={setLastYear}>Last Year</button>
        <button type="button" class="btn btn-sm variant-outline-primary" on:click={setLastSixMonths}>Last 6 Months</button>
    </div>
</div>
<div class="flex items-center w-full flex-col gap-2">
    {#each data.history as item}
    <div class="bg-white">
        <Chart data={item} />
    </div>
    {/each}
</div>



