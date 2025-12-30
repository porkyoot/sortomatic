from nicegui import ui
from typing import List, Dict, Any
# from ...theme import Theme
from ..atoms.badges import StatusBadge
from ..atoms.special.histograms import AppHistogram
from ..atoms.separators import AppSeparator

def StatusBadgeRow(items: List[Dict[str, Any]], theme: Any = None): # Theme arg kept optional for compat if needed, but unused
    """
    A unified row of status indicators with a glassmorphic container.
    Renders a group of minimal status badges or histograms separated by dividers.

    Args:
        items: List of dicts valid for creating status items. 
               Expected keys for badge: 'label', 'state', 'icon', 'rotate'
               Expected keys for histogram: 'label', 'history', 'color', 'icon'
    """
    # Container style
    with ui.row().classes('s-status-badge-row'):
        for i, item in enumerate(items):
            # Add separator
            if i > 0:
                AppSeparator()
            
            label = item.get('label', '?')
            history = item.get('history')
            
            if history is not None:
                # Render as histogram
                AppHistogram(
                    values=history,
                    color=item.get('color', 'var(--nt-primary)'),
                    height="16px",
                    bar_width="2px",
                    max_bars=10,
                    icon=item.get('icon'),
                    label=label,
                    transparent=True
                )
            else:
                # Render as standard status badge
                state = item.get('state', 'unknown')
                icon = item.get('icon')
                rotate = item.get('rotate', False)
                
                # Using 'simple' variant effectively mimics the "icon + text" look 
                # without a background, while leveraging the badge component logic.
                # Passing 'interactive=False' to ensure it's just a display.
                StatusBadge(
                    label=label,
                    state=state,
                    # theme=theme, # REMOVED
                    variant='simple',
                    icon=icon,
                    rotate=rotate,
                    interactive=False
                )

