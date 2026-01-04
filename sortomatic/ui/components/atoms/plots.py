from nicegui import ui
from sortomatic.ui.style import theme
from typing import Optional, Callable, List
import math



def sparkline_histogram(data_source: Callable[[], List[float]], update_interval: float = 1.0, val_formatter: Optional[Callable[[float], str]] = None, y_max: float = 100) -> ui.echart:
    """
    An inline chart for performance monitoring. Bars move slowly from right to left.
    """
    
    options = {
        'grid': {'left': 0, 'right': 0, 'top': 0, 'bottom': 0},
        'xAxis': {'type': 'category', 'show': False, 'boundaryGap': False},
        'yAxis': {'type': 'value', 'show': False, 'min': 0, 'max': y_max},
        'tooltip': {'trigger': 'axis', 'formatter': '{b}', 'confine': True}, # {b} is the data item name
        'series': [{
            'data': [],
            'type': 'bar',
            'barWidth': '60%',
            'barMinHeight': 2, # Ensure near-0 values appear as small dots
            'itemStyle': {
                'barBorderRadius': [1, 1, 1, 1]
            }
        }]
    }
    
    chart = ui.echart(options).classes('h-8 w-16') # Smaller inline size
    
    def update():
        new_data = data_source()
        
        # Color each bar individually based on its value
        formatted_data = []
        for raw_val in new_data:
             
             # Format tooltip text
             if val_formatter:
                 tooltip_text = val_formatter(raw_val)
             else:
                 tooltip_text = f"{round(raw_val, 1)}%"
             
             # Determine color (thresholds mainly for 0-100 scale)
             val = raw_val
             if val < 10:
                 color = '#2aa198' # Info (Cyan) - Idle
             elif val < 40:
                 color = '#859900' # Success (Green)
             elif val < 60:
                 color = '#b58900' # Suggest (Yellow)
             elif val < 80:
                 color = '#cb4b16' # Warning (Orange)
             else:
                 color = '#dc322f' # Error (Red)
             
             formatted_data.append({
                 'value': raw_val,
                 'name': tooltip_text, # Passed to tooltip {b}
                 'itemStyle': {'color': color}
             })

        chart.options['series'][0]['data'] = formatted_data
        chart.update()
        
    ui.timer(update_interval, update)
    return chart
