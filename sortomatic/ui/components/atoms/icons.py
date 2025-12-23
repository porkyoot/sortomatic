from nicegui import ui
from typing import Optional

def AppIcon(
    name: str,
    color: str = 'var(--app-text)',
    size: str = 'sm', # xs, sm, md, lg, xl OR explicit size like '1.5em'
    tooltip: Optional[str] = None
):
    """
    A unified icon component with support for colors, tooltips, and standard sizes.
    """
    icon = ui.icon(name).style(f'color: {color};').props(f'size={size}')
    
    if tooltip:
        icon.tooltip(tooltip)
        
    return icon
