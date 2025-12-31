from nicegui import ui
from sortomatic.ui.style import theme
from sortomatic.ui.components import atoms
from typing import Optional, Callable, List

def status_badge_row(sparkline_data: Callable[[], List[float]]) -> ui.row:
    """
    StatusBadgeRow: Connectivity badges + sparkline + separators.
    """
    with ui.row().classes('items-center h-full gap-2 px-2') as row:
        atoms.status_badge(text='Core Connected', active=True)
        atoms.separator()
        atoms.status_badge(text='Docker IO', active=True)
        atoms.separator()
        
        # Sparkline for performace
        ui.label('CPU').classes('text-[10px] font-bold opacity-60')
        atoms.sparkline_histogram(sparkline_data)
        
    return row
