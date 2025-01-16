import type { HistoryData } from '$lib/types';
import * as echarts from 'echarts';

type EChartsOption = echarts.EChartsOption;

export function generateChartOptions(data: HistoryData): EChartsOption {
    const dates: string[] = [];
    const percentages: number[] = [];
    const rangeMins: number[] = [];
    const rangeMaxs: number[] = [];
    const results: number[] = [];
    const suggestions: (string | undefined)[] = [];
    const unit = data.data[0]?.measurement_unit || '';

    data.data.forEach(item => {
        const result = Number(item.result);
        const percentage = ((result - item.range_min) / (item.range_max - item.range_min)) * 100;
        results.push(item.result);
        percentages.push(percentage);
        dates.push(item.date || 'N/A');
        rangeMins.push(item.range_min);
        rangeMaxs.push(item.range_max);
        suggestions.push(item.suggestion);
    });

    const minPercentage = Math.min(...percentages);
    const maxPercentage = Math.max(...percentages);
    const rangeBuffer = 20;

    const yMin = minPercentage > 0 ? Math.max(0, minPercentage - rangeBuffer) : minPercentage - rangeBuffer;
    const yMax = Math.max(maxPercentage, 100 + rangeBuffer);

    return {
        tooltip: {
            trigger: 'axis',
            formatter: (params: any) => {
                const dataIndex = params[0].dataIndex;
                return `Date: ${dates[dataIndex]}<br/>
                        Result: ${results[dataIndex]} ${unit}<br/>
                        Range: ${rangeMins[dataIndex]} - ${rangeMaxs[dataIndex]} ${unit}<br/>
                        Suggestion: ${suggestions[dataIndex] || 'N/A'}`;
            }
        },
        xAxis: {
            type: 'category',
            data: dates,
            axisLabel: {
                formatter: (value: string) => value
            }
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                show: true,
                formatter: (value: number) => `${value.toFixed(0)}%`
            },
            min: yMin,
            max: yMax
        },
        visualMap: [
            {
                show: true,
                type: 'continuous',
                min: Math.min(-20, minPercentage),
                max: Math.max(120, maxPercentage),
                seriesIndex: 0,
                range: [0, 100],
                inRange: {
                    color: ['#ff6f7f', '#00ff00', '#ff6f7f']
                },
                outOfRange: {
                    color: '#ff6f7f'  // Darker shade of red for out-of-range
                },
                orient: 'horizontal',
                showLabel: true,
            }
        ],
        series: [
            {
                type: 'line',
                data: percentages,
                lineStyle: {
                    width: 2
                },
                symbolSize: 10
            }
        ],
        title: {
            text: data.name,
            left: 'center',
            top: 10,
            textStyle: {
                fontSize: 16
            }
        }
    };
} 
