<script lang="ts">
	import type { PageData } from "./$types";
    import { Line } from 'svelte-chartjs';
    import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale } from 'chart.js';
    import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
    ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale);

    interface Props {
        data: PageData;
    }

    let { data }: Props = $props();

    const chartData = data.history.map(item => {
        const d = item.data.map((item) => {
            let percentage = 0;

            if (item.is_numeric) {
                if (item.range_min && item.range_max) {
                    percentage = (item.result - item.range_min) / (item.range_max - item.range_min);
                } else if (item.range_max) {
                    percentage = (item.result - 0) / (item.range_max - 0);
                } else if (item.range_min) {
                    percentage = (item.result - item.range_min) / (1 - item.range_min);
                } else {
                    percentage = item.result;
                }
            } else {
                percentage = Number((item.result === 1.0) === item.expected)
            }

            return {
                x: new Date(item.date).getTime(),
                y: percentage,
                original: item.result,
                unit: item.measurement_unit,
                minimum: item.range_min,
                maximum: item.range_max
            };
        })

        return {
            data: {
                labels: item.data.map(item => item.date),
                datasets: [
                    {
                        label: item.nume + ' Percentage',
                        data: d,
                        fill: false,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }
                ],
            },
            options: {
                tooltips: {
                    enabled: false,
                },
                scales: {
                    y: {
                        display: true,
                        suggestedMin: 0,
                        suggestedMax: 1,
                    },
                },
                plugins: {
                    responsive: true,
                    tooltip: {
                        callbacks: {
                            label: function(context: any) {
                                const original = context.raw.original;
                                const unit = context.raw.unit;
                                return [`Original: ${original} ${unit}`, `Minimum: ${context.raw.minimum} ${context.raw.unit}`, `Maximum: ${context.raw.maximum} ${context.raw.unit}`];
                            }
                        }
                    }
                }
            },
            suggestions: item.data.map((item) => {return {suggestion: item.suggestion, date: item.date}}).filter((item) => item.suggestion !== null)
        }
    });
</script>

<div class="flex items-center w-full flex-col">
    {#each chartData as item}
        <div class="bg-gray-200 max-w-xl w-full text-black text-sm">
            <Line {...item} />

            {#if item.suggestions.length > 0}
                <Accordion>
                    {#each item.suggestions as suggestion}
                        <AccordionItem>
                            {#snippet lead()}
                                                        Suggestion from {suggestion.date}
                                                    {/snippet}
                            {#snippet summary()}
                                                        <div></div>
                                                    {/snippet}
                            {#snippet content()}
                                                        <div class="whitespace-pre-line">{suggestion.suggestion}</div>
                                                    {/snippet}
                        </AccordionItem>
                    {/each}
                </Accordion>
            {/if}
        </div>
    {/each}
</div>



