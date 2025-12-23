from nicegui import ui
from typing import List, Optional

def AppHistogram(
    values: List[float], 
    color: str = 'var(--q-primary)',
    height: str = '24px',
    bar_width: str = '3px',
    gap: str = '1px',
    max_bars: int = 30,
    label: Optional[str] = None
):
    """
    A premium inline histogram (sparkline) for performance monitoring.
    
    Args:
        values: List of floats between 0.0 and 1.0.
        color: CSS color for the bars.
        height: Total height of the component.
        bar_width: Width of each individual bar.
        gap: Space between bars.
        max_bars: Maximum number of bars to display (truncates from the left).
        label: Tooltip prefix.
    """
    # Truncate values to max_bars
    display_values = values[-max_bars:] if len(values) > max_bars else values
    latest_val = display_values[-1] if display_values else 0
    
    # Tooltip text
    tooltip_text = f"{label}: {latest_val*100:.1f}%" if label else f"{latest_val*100:.1f}%"
    
    with ui.row().classes('items-end no-wrap px-1 shrink-0 group').style(f'height: {height}; gap: {gap};'):
        ui.tooltip(tooltip_text).classes('text-[10px] font-bold')
        
        for val in display_values:
            # Ensure value is clamped
            clamped_val = max(0.05, min(1.0, val)) # Min 5% height for visibility
            
            ui.element('div').classes('rounded-t-[1px] transition-all duration-300').style(
                f'height: {clamped_val * 100}%; '
                f'width: {bar_width}; '
                f'background-color: {color}; '
                f'opacity: {0.4 + (clamped_val * 0.6)};' # Hotter values are more opaque
            )
