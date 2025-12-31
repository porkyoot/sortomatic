from nicegui import ui
from sortomatic.ui.style import theme
from typing import Optional, Callable

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
