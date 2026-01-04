from nicegui import ui
from sortomatic.ui.style import theme
from typing import Optional, Callable, List
import math



def sparkline_histogram(data_source: Callable[[], List[float]], update_interval: float = 1.0) -> ui.echart:
    """
    An inline chart for performance monitoring. Bars move slowly from right to left.
    
    Note: ECharts configurations are serialized to JSON and sent to the browser.
    CSS variable references like 'var(--color-primary)' won't be evaluated by ECharts.
    Therefore, we use the actual Solarized blue color (#268bd2) directly.
    If you change the theme primary color, update this value accordingly.
    """
    
    options = {
        'grid': {'left': 0, 'right': 0, 'top': 0, 'bottom': 0},
        'xAxis': {'type': 'category', 'show': False, 'boundaryGap': False},
        'yAxis': {'type': 'value', 'show': False, 'min': 0},
        'tooltip': {'trigger': 'axis', 'formatter': '{c}'},
        'series': [{
            'data': [],
            'type': 'bar',
            'barWidth': '60%',
            'itemStyle': {'color': '#268bd2'}  # Solarized blue (primary color)
        }]
    }
    
    chart = ui.echart(options).classes('h-8 w-32') # Small inline size
    
    def update():
        new_data = data_source()
        chart.options['series'][0]['data'] = new_data
        chart.update()
        
    ui.timer(update_interval, update)
    return chart
