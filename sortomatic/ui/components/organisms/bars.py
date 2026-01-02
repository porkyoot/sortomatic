from nicegui import ui
from sortomatic.ui.style import theme
from sortomatic.ui.components import atoms, molecules
from typing import Callable, List

def status_bar(sparkline_data: Callable[[], List[float]]) -> ui.row:
    """
    Status Bar: Global top bar with status, settings, and branding.
    """
    with ui.row().classes('w-full h-12 items-center justify-between px-4 border-b thin-border premium-glass bg-bg z-50') as row:
        # Left: Branding
        with ui.row().classes('items-center gap-2'):
            ui.icon('sort').classes('text-2xl text-primary')
            ui.label('SORTOMATIC').classes('font-bold tracking-[0.2em] text-sm')

        # Center: Status Badge Row (Connectivity + CPU)
        molecules.status_badge_row(sparkline_data)

        # Right: Settings
        with ui.row().classes('items-center gap-2'):
            # Default to Dark Mode
            dark = ui.dark_mode(value=True)
            
            def update_dark_mode_icon(e):
                if e.value: # Dark Mode Active -> Show Sun
                    mode_btn.props('icon=wb_sunny')
                    mode_btn.classes('btn-warning-text', remove='btn-info-text')
                else: # Light Mode Active -> Show Moon
                    mode_btn.props('icon=dark_mode')
                    mode_btn.classes('btn-info-text', remove='btn-warning-text')

            dark.on_value_change(update_dark_mode_icon)

            mode_btn = atoms.button(
                icon='wb_sunny', 
                variant='ghost', 
                color='warning', 
                shape='circle',
                on_click=dark.toggle
            )
            
    return row
