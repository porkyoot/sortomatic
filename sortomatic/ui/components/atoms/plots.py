from nicegui import ui
from sortomatic.ui.style import theme
from typing import Optional, Callable, List
import math

def logarithmic_slider(min_val: float, max_val: float, value: float = 1.0, on_change: Optional[Callable] = None):
    """
    A slider where the visual representation is linear, but the underlying value is logarithmic.
    Returns a container with the slider and a label showing the current value.
    """
    
    # Helper to convert log scale value to linear position [0, 1]
    def val_to_pos(v):
        if v <= 0: return 0.0
        return math.log(v / min_val) / math.log(max_val / min_val)
    
    # Helper to convert linear position to log scale value
    def pos_to_val(p):
        return min_val * math.pow(max_val / min_val, p)

    # Format value for display
    def format_val(v):
        if v >= 100:
            return f'{v:.0f}'
        elif v >= 10:
            return f'{v:.1f}'
        else:
            return f'{v:.2f}'

    start_pos = val_to_pos(value)
    current_val = value
    
    with ui.row().classes('items-center gap-2 w-full') as container:
        def handle_change(e):
            nonlocal current_val
            real_val = pos_to_val(e.value)
            current_val = real_val
            value_label.text = format_val(real_val)
            if on_change:
                on_change(real_val)
        
        sl = ui.slider(min=0.0, max=1.0, step=0.01, value=start_pos, on_change=handle_change).classes('flex-grow')
        value_label = ui.label(format_val(current_val)).classes('text-sm font-mono min-w-16 text-right')
    
    return container

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
