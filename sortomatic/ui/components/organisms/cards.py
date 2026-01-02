from nicegui import ui
from sortomatic.ui.style import theme
from sortomatic.ui.components import atoms, molecules
from typing import Callable, Optional

def scan_card(
    on_play: Callable, on_pause: Callable, on_restart: Callable, on_ff: Callable,
    progress: float, eta: str, current_path: str, speed: str, error: Optional[str] = None,
    scan_state: str = 'idle'
) -> ui.card:
    """
    Scan Card: Monitor scanning progress.
    """
    # Use atom card as base but we reconstruct structure since we need header slot
    with atoms.card().classes('w-full flex flex-col gap-4') as card_container:
        
        # Header with controls
        header_slot = molecules.header_card("Active Scan")
        with header_slot:
            molecules.scan_controls(on_play, on_pause, on_restart, on_ff, scan_state=scan_state)
        
        # Body
        with ui.column().classes('w-full gap-2'):
            # Info Row
            with ui.row().classes('w-full justify-between items-end'):
                ui.label('Processing...').classes('text-xs font-bold uppercase text-muted')
                ui.label(speed).classes('text-xs font-mono text-secondary')
            
            # Progress Bar
            # Atom progress bar is indeterminate, let's allow value override or just use atom
            # Atom `progress_bar` returns a linear_progress. We can verify if it accepts value.
            # NiceGUI linear_progress uses `value` prop.
            pb = atoms.progress_bar()
            pb.props(f'query=false value={progress}') # switch specific props
            pb.classes('opacity-100')
            
            # Path & ETA & Error
            with ui.row().classes('w-full justify-between items-start mt-2'):
                with ui.column().classes('gap-0 flex-1'):
                    ui.label(current_path).classes('text-sm font-mono truncate w-full opacity-80').tooltip(current_path)
                    if error:
                        ui.label(f'Error: {error}').classes('text-xs font-bold text-error')
                
                ui.label(eta).classes('text-2xl font-light')

    return card_container
