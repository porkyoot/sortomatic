from nicegui import ui
from sortomatic.ui.style import theme
from sortomatic.ui.components import atoms, molecules
from typing import Callable, List

def status_bar(sparkline_data: Callable[[], List[float]]) -> ui.row:
    """
    Status Bar: Global top bar with status, settings, and branding.
    """
    with ui.row().classes(f'w-full h-12 items-center justify-between px-4 border-b {theme.BORDER} {theme.GLASS}').style(f'background-color: {theme.BG}; z-index: 50;') as row:
        # Left: Branding
        with ui.row().classes('items-center gap-2'):
            ui.icon('sort').classes(f'text-2xl text-[{theme.PRIMARY}]')
            ui.label('SORTOMATIC').classes('font-bold tracking-[0.2em] text-sm')

        # Center: Status Badge Row (Connectivity + CPU)
        molecules.status_badge_row(sparkline_data)

        # Right: Settings
        with ui.row().classes('items-center gap-2'):
            atoms.button(icon='settings', variant='ghost', shape='circle').props('dense')
            ui.avatar('img:https://cdn.quasar.dev/img/boy-avatar.png').classes('w-8 h-8 opacity-80 border').style(f'border-color: {theme.BORDER_COLOR}')
            
    return row
