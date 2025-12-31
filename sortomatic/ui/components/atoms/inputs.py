from nicegui import ui
from sortomatic.ui.style import theme
from typing import Optional, Callable

def search_bar(placeholder: str = 'Search...', on_change: Optional[Callable] = None) -> ui.input:
    """
    An elegant text input with a search icon.
    """
    inp = ui.input(placeholder=placeholder, on_change=on_change).classes(f'rounded-full px-4 py-1 text-sm bg-opacity-20')
    inp.props('standout dense rounded item-aligned input-class="text-sm"')
    with inp.add_slot('prepend'):
        ui.icon('search').classes(f'text-xs {theme.TEXT_MUTED}')
    return inp

def date_picker(on_change: Optional[Callable] = None) -> ui.input:
    """
    A wrapper around the nicegui Date Picker to select a date range (start/end).
    """
    with ui.input('Date Range').classes('text-sm') as date_input:
        with date_input.add_slot('append'):
            ui.icon('event').classes('cursor-pointer')
            with ui.menu().props('no-parent-event') as menu:
                # Range picker
                ui.date(on_change=on_change).props('range')
    return date_input
