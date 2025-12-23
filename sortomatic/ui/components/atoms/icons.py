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

def StatusIcon(
    state: str,
    palette: 'ColorPalette',
    size: str = 'sm',
    tooltip: Optional[str] = None,
    animate: bool = False
):
    """
    A specialized icon for displaying statuses with automatic coloring,
    icon selection, and optional animations.
    """
    from ...theme import StatusStyles
    
    name = StatusStyles.get_icon(state)
    color = StatusStyles.get_color(state, palette)
    
    icon = AppIcon(name, color=color, size=size, tooltip=tooltip)
    
    # Simple rotation for pending states if requested
    if animate and state.lower() == StatusStyles.PENDING:
        icon.classes('rotate-animation')
        
    return icon
