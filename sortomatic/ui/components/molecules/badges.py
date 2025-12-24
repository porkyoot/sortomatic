from nicegui import ui
from typing import List, Dict
from ...theme import Theme
from ..atoms.badges import StatusBadge

def StatusBadgeRow(items: List[Dict[str, str]], theme: Theme):
    """
    A unified row of status indicators with a glassmorphic container.
    Renders a group of minimal status badges separated by dividers.

    Args:
        items: List of dicts valid for creating status items. 
               Expected keys: 'label', 'state', 'tooltip'
        theme: Theme for styling
    """
    # Container style
    with ui.row().classes('s-status-badge-row'):
        for i, item in enumerate(items):
            # Add separator
            if i > 0:
                ui.element('div').classes('s-separator-vertical')
            
            label = item.get('label', '?')
            state = item.get('state', 'unknown')
            icon = item.get('icon')
            rotate = item.get('rotate', False)
            
            # Using 'simple' variant effectively mimics the "icon + text" look 
            # without a background, while leveraging the badge component logic.
            # Passing 'interactive=False' to ensure it's just a display.
            StatusBadge(
                label=label,
                state=state,
                theme=theme,
                variant='simple',
                icon=icon,
                rotate=rotate,
                interactive=False
            )
