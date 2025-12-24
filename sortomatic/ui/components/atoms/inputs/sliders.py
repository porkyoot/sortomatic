from nicegui import ui
import math
from typing import Optional, Callable, Union

def AppSlider(
    min: float = 0,
    max: float = 100,
    step: float = 1,
    value: float = 0,
    label: str = "",
    unit: str = "",
    log: bool = False,
    log_dir: str = 'low', # 'low' (precision at bottom) or 'high' (precision at top)
    on_change: Optional[Callable] = None,
    show_markers: bool = False,
    classes: str = "",
    props: str = ""
):
    """
    A premium themed slider with logarithmic support and value display.
    
    Args:
        min: Minimum value
        max: Maximum value
        step: Step increment
        value: Initial value
        label: Label to display above slider
        unit: Unit suffix for value display
        log: Enable logarithmic scaling
        log_dir: 'low' (precision at bottom) or 'high' (precision at top)
        on_change: Callback when value changes
        show_markers: Show tick markers
        classes: Additional CSS classes to apply to container
        props: Additional props to apply to slider
    """
    
    def to_log(linear_val: float) -> float:
        """Convert 0-100 linear value to min-max log value."""
        p = linear_val / 100.0
        if log_dir == 'high':
            # Flip: 0 at start, but more 'room' at the high end
            # We invert the progress, calculate log, then invert back
            p = 1.0 - p
            val = max - (max - min) * (p**2) # Simple quadratic for 'zooming'
        else:
            # Standard 'low' log: more room at the small end
            val = min + (max - min) * (p**2)
        return val

    def from_log(log_val: float) -> float:
        """Convert min-max log value back to 0-100 linear for slider state."""
        if log_dir == 'high':
            # val = max - (max-min)*p^2  => p = sqrt((max-val)/(max-min))
            p = math.sqrt(abs(max - log_val) / abs(max - min))
            return (1.0 - p) * 100
        else:
            # val = min + (max-min)*p^2 => p = sqrt((val-min)/(max-min))
            p = math.sqrt(abs(log_val - min) / abs(max - min))
            return p * 100

    with ui.column().classes(f'w-full gap-1 {classes}'):
        if label:
            ui.label(label).classes('s-slider-label')
            
        with ui.row().classes('w-full items-center gap-4'):
            # Internal slider state
            initial_slider_val = from_log(value) if log else value
            
            slider = ui.slider(
                min=0 if log else min, 
                max=100 if log else max, 
                step=0.1 if log else step, 
                value=initial_slider_val
            ).classes('grow')
            
            # Value Label on the right
            value_display = ui.label('').classes('s-slider-value')
            
            def update_ui(e):
                raw = e.value
                current_val = to_log(raw) if log else raw
                
                # Format text
                if current_val >= 1000:
                    text = f"{current_val:,.0f}{unit}"
                else:
                    text = f"{current_val:.1f}{unit}"
                value_display.set_text(text)
                
                if on_change:
                    on_change(current_val)

            slider.on_value_change(update_ui)
            
            # Initialization
            update_ui(type('obj', (object,), {'value': initial_slider_val}))

    if show_markers and not log:
        slider.props('markers')
        
    slider.props(f'label-always color=primary {props}')
    
    return slider

def AppRangeSlider(
    min: float = 0,
    max: float = 100,
    value: Optional[dict] = None, # {'min': 0, 'max': 100}
    label: str = "",
    unit: str = "",
    log: bool = False,
    on_change: Optional[Callable] = None,
    classes: str = "",
    props: str = ""
):
    """
    A premium themed range slider with logarithmic support.
    
    Args:
        min: Minimum value
        max: Maximum value
        value: Initial value dict with 'min' and 'max' keys
        label: Label to display above slider
        unit: Unit suffix for value display
        log: Enable logarithmic scaling
        on_change: Callback when value changes
        classes: Additional CSS classes to apply to container
        props: Additional props to apply to slider
    """
    def to_log(linear_val: float) -> float:
        p = linear_val / 100.0
        return min + (max - min) * (p**2)

    def from_log(log_val: float) -> float:
        p = math.sqrt(abs(log_val - min) / abs(max - min))
        return p * 100

    with ui.column().classes(f'w-full gap-1 {classes}'):
        if label:
            ui.label(label).classes('s-slider-label')
            
        initial_min = value['min'] if value else min
        initial_max = value['max'] if value else max
        
        linear_min = from_log(initial_min) if log else initial_min
        linear_max = from_log(initial_max) if log else initial_max
        
        with ui.row().classes('w-full items-center gap-4'):
            slider = ui.range(
                min=0 if log else min, 
                max=100 if log else max, 
                value={'min': linear_min, 'max': linear_max}
            ).classes('grow')
            
            value_display = ui.label('').classes('s-slider-value')
            
            def update_ui(e):
                raw_min, raw_max = e.value['min'], e.value['max']
                curr_min = to_log(raw_min) if log else raw_min
                curr_max = to_log(raw_max) if log else raw_max
                
                def fmt(v):
                    if v >= 1000 * 1000 * 1024: return f"{v/(1024**3):.1f}GB"
                    if v >= 1000 * 1024: return f"{v/(1024**2):.1f}MB"
                    if v >= 1024: return f"{v/1024:.0f}kB"
                    return f"{v:.0f}B"

                value_display.set_text(f"{fmt(curr_min)} - {fmt(curr_max)}")
                
                if on_change:
                    on_change({'min': curr_min, 'max': curr_max})

            slider.on_value_change(update_ui)
            update_ui(type('obj', (object,), {'value': {'min': linear_min, 'max': linear_max}}))

    slider.props(f'label-always color=primary {props}')
    return slider
