<script lang="ts">
	import type { PageData } from "./$types";
    import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
	import Chart from "./Chart.svelte";

    interface Props {
        data: PageData;
    }

    let { data }: Props = $props();
</script>

<div class="flex items-center w-full flex-col gap-2">
    {#each data.history as item, id}
    <div class="bg-white">
        <Chart data={item} />
    </div>

            <!-- {#if item?.suggestions?.length > 0}
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
            {/if} -->
    {/each}
</div>



