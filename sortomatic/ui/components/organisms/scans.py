from nicegui import ui
from typing import Optional, Callable
from ...theme import Theme
from ..atoms.cards import AppCard
from ..atoms.separators import AppSeparator
from ..molecules.scan_controls import ScanControls

def ScanCard(
    name: str, 
    state: str = "idle", # "running", "idle", "paused", "completed", "error"
    progress: float = 0.0, # 0.0 to 100.0
    eta: str = "Calculating...",
    current_item: str = "",
    speed: str = "0",
    unit: str = "file/s",
    is_error: bool = False,
    theme: Theme = None,
    on_play: Optional[Callable] = None,
    on_pause: Optional[Callable] = None,
    on_resume: Optional[Callable] = None,
    on_restart: Optional[Callable] = None,
    on_fast_mode: Optional[Callable] = None
):
    """
    A comprehensive scan task card showing progress, dynamic status, and controls.
    """
    # Internal variables for state
    card_state = {
        'state': state,
        'progress': progress,
        'eta': eta,
        'speed': speed,
        'unit': unit,
        'current_item': current_item,
        'is_error': is_error
    }
    
    # Internal render function
    def _render_content():
        card.clear()
        
        # Internal state mapping to ScanControls states
        control_state = card_state['state']
        if card_state['state'] == "error":
            control_state = "idle" # Allow restart
            
        with card:
            # Row 1: Progress Bar and Controls
            with ui.row().classes('w-full items-center gap-4 no-wrap'):
                # Integrated Progress Bar
                with ui.element('div').classes('flex-grow s-progress-container'):
                    ui.linear_progress(value=card_state['progress']/100.0, show_value=False) \
                        .classes('s-progress s-progress--rect')
                    # We show the percentage here instead of the name
                    ui.label(f"{card_state['progress']:.1f}%").classes('s-progress__label')
                
                ScanControls(
                    state=control_state,
                    theme=theme,
                    on_play=on_play,
                    on_pause=on_pause,
                    on_resume=on_resume,
                    on_restart=on_restart,
                    on_fast_mode=on_fast_mode
                ).classes('shrink-0')

            # Row 2: Status (Left) and Indicators (Right)
            with ui.row().classes('w-full items-center justify-between gap-3 no-wrap'):
                # Status / Current Item
                ui.label(card_state['current_item']) \
                    .classes('s-scan-card__status truncate max-w-[50%]') \
                    .style(f"color: {'var(--c-error)' if card_state['is_error'] else 'inherit'};")

                # Indicators Row
                with ui.row().classes('items-center gap-4 shrink-0'):
                    # Speed
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('speed', size='16px').classes('opacity-40')
                        ui.label(f"{card_state['speed']}").classes('s-scan-card__eta')
                        ui.label(card_state['unit']).classes('s-scan-card__unit')

                    # Separator
                    AppSeparator()

                    # ETA
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('schedule', size='16px').classes('opacity-40')
                        ui.label(card_state['eta']).classes('s-scan-card__eta')

    def update_progress(new_progress: float, new_eta: str, new_speed: str = "0", new_unit: str = "file/s"):
        card_state['progress'] = new_progress
        card_state['eta'] = new_eta
        card_state['speed'] = new_speed
        card_state['unit'] = new_unit
        _render_content()

    def update_state(new_state: str):
        card_state['state'] = new_state
        _render_content()

    def update_status(new_status: str, is_error: bool = False):
        card_state['current_item'] = new_status
        card_state['is_error'] = is_error
        _render_content()

    card = AppCard(variant='glass')
    card.classes('s-scan-card')
    card.update_progress = update_progress
    card.update_state = update_state
    card.update_status = update_status
    
    _render_content()
    return card
