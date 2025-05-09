import React, { useEffect, useRef } from 'react';
import { createChart, ColorType } from 'lightweight-charts';

interface PriceChartProps {
  data: {
    time: string;
    open: number;
    high: number;
    low: number;
    close: number;
  }[];
  height?: number;
}

const PriceChart: React.FC<PriceChartProps> = ({ data, height = 300 }) => {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    if (!chartContainerRef.current || !data.length) return;
    
    const chartContainer = chartContainerRef.current;
    
    // Clear any existing chart
    chartContainer.innerHTML = '';
    
    // Create the chart
    const chart = createChart(chartContainer, {
      height,
      layout: {
        background: { color: '#ffffff' },
        textColor: '#333',
      },
      grid: {
        vertLines: { color: '#f0f0f0' },
        horzLines: { color: '#f0f0f0' },
      },
      timeScale: {
        borderColor: '#d1d5db',
      },
    });
    
    // Add the candlestick series
    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#4CAF50',
      downColor: '#FF5252',
      borderVisible: false,
      wickUpColor: '#4CAF50',
      wickDownColor: '#FF5252',
    });
    
    // Set the data
    candlestickSeries.setData(data);
    
    // Fit content to container
    chart.timeScale().fitContent();
    
    // Handle resizing
    const handleResize = () => {
      chart.applyOptions({ width: chartContainer.clientWidth });
    };
    
    window.addEventListener('resize', handleResize);
    
    // Cleanup on unmount
    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [data, height]);
  
  return <div ref={chartContainerRef} className="w-full"></div>;
};

export default PriceChart;
