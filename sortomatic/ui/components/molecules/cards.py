from nicegui import ui
from sortomatic.ui.style import theme
from sortomatic.ui.components import atoms
from typing import Optional, Callable, List

def header_card(title: str) -> ui.row:
    """
    Header Card: Card title + horizontal separator + Slot on the right (via context).
    """
    with atoms.card().classes('w-full flex-row items-center gap-4 py-2 px-4') as card:
        with ui.row().classes('flex-1 items-center gap-4'):
            ui.label(title).classes('text-xl font-bold uppercase tracking-wider')
            # Horizontal separator usually
            ui.element('div').classes(f'h-px flex-1 bg-slate-700 opacity-20 {theme.BORDER}')
        
        # The return value acts as the "right slot" container effectively if the user appends to it? 
        # Or we return a container for the right slot.
        # Impl: Return the row so user can add items to it? 
        # But we want the user to add items to the *right*.
        # Let's create a specific container for the right slot.
        right_slot = ui.row().classes('items-center gap-2')
        
    return right_slot
