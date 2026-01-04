from nicegui import ui
from sortomatic.ui.style import theme
from typing import Optional, Callable
import math
import humanize

def search_bar(placeholder: str = 'Search...', on_change: Optional[Callable] = None) -> ui.input:
    """
    An elegant text input with a search icon.
    """
    inp = ui.input(placeholder=placeholder, on_change=on_change).classes('rounded-full px-4 py-1 text-sm bg-bg bg-opacity-20')
    inp.props('standout dense rounded item-aligned input-class="text-sm"')
    with inp.add_slot('prepend'):
        ui.icon('search').classes('text-xs text-muted')
    return inp

def date_picker(label: str = 'Range', value: str = '', on_change: Optional[Callable] = None):
    """
    A thin wrapper around the NiceGUI date_input component for selecting a date range.
    """
    date = ui.date_input(label, value=value, range_input=True, on_change=on_change)
    date.classes('w-60')
    return date

def format_file_size(bytes_size: int) -> str:
    """Format file size in human-readable format."""
    if bytes_size is None:
        return "—"
    return humanize.naturalsize(bytes_size, binary=True)

def file_size_slider(
    min_bytes: int = 0,
    max_bytes: int = 100 * 1024 * 1024 * 1024,  # 100 GB
    on_change: Optional[Callable] = None
) -> ui.column:
    """
    Range slider with logarithmic scale for file sizes.
    """
    
    def _index_to_bytes(idx: float) -> int:
        if idx <= 0:
            return 0
        if idx >= 9:
            return 100 * 1024 * 1024 * 1024
        return int(10**(idx + 2))

    def _bytes_to_index(b: int) -> float:
        if b <= 0:
            return 0.0
        return max(0.0, min(9.0, math.log10(b) - 2))

    with ui.column().classes('w-full gap-0') as container:
        # Header with labels
        with ui.row().classes('w-full justify-between items-center'):
            ui.label('Size').classes('text-xs opacity-70')
            with ui.row().classes('gap-1 items-center'):
                min_label = ui.label(format_file_size(min_bytes)).classes('text-xs font-bold')
                ui.label('-').classes('text-xs opacity-50')
                max_label = ui.label(format_file_size(max_bytes)).classes('text-xs font-bold')
        
        def _handle_change(e):
            val = e.value
            new_min = _index_to_bytes(val['min'])
            new_max = _index_to_bytes(val['max'])
            
            min_label.text = format_file_size(new_min)
            max_label.text = format_file_size(new_max)
            
            if on_change:
                on_change({'min': new_min, 'max': new_max})

        # Range slider
        slider = ui.range(
            min=0, max=9, step=0.1,
            value={'min': _bytes_to_index(min_bytes), 'max': _bytes_to_index(max_bytes)},
            on_change=_handle_change
        ).classes('w-full')
        slider.props('label-always') # Optional: shows value tooltip, but logarithmic index might be confusing. 
        # Actually existing design didn't use label-always for the slider itself, but updated separate labels.
        # Removing props('label-always') to match old design.
        slider.props('remove=label-always') # Just to be sure

        # Scale labels
        with ui.row().classes('w-full justify-between responsive-text-xs opacity-60 mt-[-8px] px-1'):
            for label in ['0B', '1KB', '100KB', '10MB', '1GB', '100GB']:
                ui.label(label)

    return container
