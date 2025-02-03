<script lang="ts">
	import { onMount } from 'svelte';
	import { generateChartOptions } from './chartOptions';
	import * as echarts from 'echarts';
	import type { HistoryData } from '$lib/types';

	export let data: HistoryData;

    export let width = "w-svw md:w-[60vw] sm:w-[80vw] lg:w-[50vw]";
    export let height = "h-80";

	let chartDiv: HTMLDivElement;
    let chart: echarts.ECharts;

    $: {
        let options = generateChartOptions(data);
        if (options && chart) {
            chart.setOption(options, true);
        }
    }

	onMount(() => {
		chart = echarts.init(chartDiv);

        window.addEventListener('resize', () => {
			chart.resize();
		});
	});
</script>

<div bind:this={chartDiv} class={`${width} ${height}`}></div>