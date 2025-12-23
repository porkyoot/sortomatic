from nicegui import ui
from typing import Optional, Callable

def AppSearchBar(
    placeholder: str = "Search...",
    on_change: Optional[Callable] = None,
    value: str = "",
    classes: str = "",
    props: str = ""
):
    """
    A premium themed search bar with a clear button and search icon.
    
    Args:
        placeholder: Placeholder text
        on_change: Callback when value changes
        value: Initial value
        classes: Additional CSS classes to apply
        props: Additional Quasar props to apply
    """
    search = ui.input(placeholder=placeholder, value=value, on_change=on_change).props(
        f'outlined dense hide-bottom-space rounded-app {props}'
    ).classes(f'w-full {classes}')
    
    with search.add_slot('prepend'):
        ui.icon('mdi-magnify').classes('text-opacity-50')
        
    with search.add_slot('append'):
        ui.icon('mdi-close').classes('cursor-pointer text-opacity-30 hover:text-opacity-100').on('click', lambda: search.set_value(''))
        
    return search

