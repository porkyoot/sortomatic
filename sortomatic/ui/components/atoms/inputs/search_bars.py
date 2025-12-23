from nicegui import ui
from typing import Optional, Callable

def AppSearchBar(
    placeholder: str = "Search...",
    on_change: Optional[Callable] = None,
    value: str = ""
):
    """
    A premium themed search bar with a clear button and search icon.
    """
    search = ui.input(placeholder=placeholder, value=value, on_change=on_change).props(
        'outlined dense hide-bottom-space rounded-app'
    ).classes('w-full')
    
    with search.add_slot('prepend'):
        ui.icon('search').classes('text-opacity-50')
        
    with search.add_slot('append'):
        ui.icon('close').classes('cursor-pointer text-opacity-30 hover:text-opacity-100').on('click', lambda: search.set_value(''))
        
    return search
