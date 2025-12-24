from nicegui import ui
from typing import Callable

def SmartSplitter(
    left_factory: Callable[[], None], 
    right_factory: Callable[[], None],
    initial_split: int = 30,
    separator: bool = True
):
    """
    Responsive layout component that switches between column (mobile) and splitter (desktop).
    Restored ui.splitter for dragging functionality.
    """
    with ui.splitter(value=initial_split).classes('s-smart-splitter') as s:
        with s.before:
            left_factory()
        with s.after:
            right_factory()
                
    return s