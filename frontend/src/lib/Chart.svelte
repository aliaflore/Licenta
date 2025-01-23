<script lang="ts">
	import { onMount } from 'svelte';
	import { generateChartOptions } from './chartOptions';
	import * as echarts from 'echarts';
	import type { HistoryData } from '$lib/types';

	export let data: HistoryData;

    export let width = "w-svw md:w-[60vw] sm:w-[80vw] lg:w-[50vw]";
    export let height = "h-80";

	let chartDiv: HTMLDivElement;
    const option = generateChartOptions(data);

	onMount(() => {
        if (!option) return;
		const chart = echarts.init(chartDiv);
		chart.setOption(option);

        window.addEventListener('resize', () => {
			chart.resize();
		});
	});
</script>

{#if option}
    <div bind:this={chartDiv} class={`${width} ${height}`}></div>
{/if}
