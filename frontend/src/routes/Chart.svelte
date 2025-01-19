<script lang="ts">
	import { onMount } from 'svelte';
	import { generateChartOptions } from './chartOptions';
	import * as echarts from 'echarts';
	import type { HistoryData } from '$lib/types';

	export let data: HistoryData;

	let chartDiv: HTMLDivElement;

	onMount(() => {
		const chart = echarts.init(chartDiv);
		const option = generateChartOptions(data);
        console.log(option);
		chart.setOption(option);

        window.addEventListener('resize', () => {
			chart.resize();
		});
	});
</script>

<div bind:this={chartDiv} class="w-svw md:w-[60vw] sm:w-[80vw] lg:w-[50vw] h-80"></div>
