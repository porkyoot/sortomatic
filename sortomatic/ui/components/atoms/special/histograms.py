from nicegui import ui
from typing import List, Optional

def AppHistogram(
    values: List[float], 
    color: str = 'var(--q-primary)',
    height: str = '24px',
    bar_width: str = '3px',
    gap: str = '1px',
    max_bars: int = 30,
    label: Optional[str] = None,
    icon: Optional[str] = None
):
    """
    A premium inline histogram (sparkline) for performance monitoring.
    Args:
        icon: Optional icon to display to the left of the histogram.
    """
    # Truncate values to max_bars
    display_values = values[-max_bars:] if len(values) > max_bars else values
    latest_val = display_values[-1] if display_values else 0
    
    # Tooltip text
    tooltip_text = f"{label}: {latest_val*100:.1f}%" if label else f"{latest_val*100:.1f}%"
    
    # Outer container with solid background color
    # We use var(--app-bg) for content to ensure contrast against the solid color
    with ui.row().classes('items-center gap-1 px-2 py-0.5 rounded-full shadow-sm bg-app-base').style(f'height: auto; color: {color};'):
        ui.tooltip(tooltip_text).classes('text-[10px] font-bold')
        
        if icon:
            from ..icons import AppIcon
            AppIcon(icon, size="1.2em", color=color).classes('opacity-80')

        # Bars Container
        with ui.row().classes('items-end no-wrap shrink-0 group').style(f'height: {height}; gap: {gap};'):
            for val in display_values:
                # Ensure value is clamped
                clamped_val = max(0.05, min(1.0, val)) # Min 5% height for visibility
                
                ui.element('div').classes('rounded-t-[1px] transition-all duration-300').style(
                    f'height: {clamped_val * 100}%; '
                    f'width: {bar_width}; '
                    f'background-color: currentColor; ' # Use parent text color (app-bg)
                    f'opacity: {0.4 + (clamped_val * 0.6)};' # Hotter values are more opaque
                )
