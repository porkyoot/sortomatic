from nicegui import ui
from sortomatic.ui.style import theme
from sortomatic.ui.components import atoms, molecules
from typing import Callable, List

def status_bar(metric_sources: dict[str, Callable[[], List[float]]]) -> ui.row:
    """
    Status Bar: Global top bar with status, settings, and branding.
    """
    with ui.row().classes('w-full h-12 items-center justify-between px-4 border-b thin-border premium-glass bg-bg z-50') as row:
        # Left: Branding
        with ui.row().classes('items-center gap-2'):
            ui.icon('sort').classes('text-2xl text-primary')
            ui.label('SORTOMATIC').classes('font-bold tracking-[0.2em] text-sm')

        # Center: Status Badge Row (Connectivity + Metrics)
        molecules.status_badge_row(metric_sources)


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

def tab_bar() -> ui.row:
    """
    Tab Bar: Navigation and Action bar below Status Bar.
    Contains Nuke button and sectional navigation tabs.
    """
    with ui.row().classes('w-full items-center gap-1 px-4 py-2 bg-surface/50 backdrop-blur-sm border-b thin-border text-sm') as row:
        # Nuke Button
        atoms.nuclear_button(
            on_explode=lambda: ui.notify('NUKE EXECUTED!', type='negative'),
            text='',
            color='warning',
            icon='mdi-nuke',
            tooltip='Delete Database' # User requested tooltip
        )
        
        ui.separator().props('vertical').classes('mx-2 h-8')
        
        # Tabs
        # Input (Blue - Primary)
        atoms.button(text='Input', color='primary', icon='chevron_left', shape='chevron')
        
        # Category (Cyan - Info)
        atoms.button(text='Category', color='info', icon='chevron_right', shape='chevron')
        
        # Duplicate (Green - Positive)
        atoms.button(text='Duplicate', color='positive', icon='chevron_right', shape='chevron')
        
        # Context (Yellow - Suggest)
        atoms.button(text='Context', color='suggest', icon='chevron_right', shape='chevron')
        
        # War Room (Red - Negative)
        atoms.button(text='War Room', color='negative', icon='chevron_right', shape='chevron')
        
        # Architect (Pink - Custom)
        atoms.button(text='Architect', color='pink', icon='chevron_right', shape='chevron')
        
        # Views (Purple - Custom)
        atoms.button(text='Views', color='purple', icon='chevron_right', shape='chevron')
        
    return row
