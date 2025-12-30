from nicegui import ui
from typing import Optional, Callable
from ...theme import Theme
from ..atoms.buttons import AppButton
from ..atoms.inputs.toggles import AppToggle
from ..atoms.separators import AppSeparator

def ScanControls(
    state: str = "idle", 
    theme: Theme = None,
    on_play: Optional[Callable] = None,
    on_pause: Optional[Callable] = None,
    on_resume: Optional[Callable] = None,
    on_restart: Optional[Callable] = None,
    on_fast_mode: Optional[Callable] = None
):
    """
    A context-aware scan control component.
    Switches buttons based on scan state and includes a fast-mode toggle.
    """
    # State constants
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"

    container = ui.row().classes('s-control-group')
    container.current_state = state

    def set_state(new_state: str):
        container.current_state = new_state
        _render()

    def _render():
        container.clear()
        with container:
            # 1. State-based Buttons
            with ui.row().classes('items-center'):
                if container.current_state == IDLE:
                    AppButton(
                        icon="play_arrow",
                        tooltip="Start Scan",
                        variant="success",
                        size="sm",
                        on_click=on_play
                    )
                
                elif container.current_state == RUNNING:
                    AppButton(
                        tooltip="Pause Scan",
                        icon="pause",
                        variant="warning",
                        size="sm",
                        on_click=on_pause
                    )
                
                elif container.current_state == PAUSED:
                    AppButton(
                        tooltip="Resume Scan",
                        icon="play_arrow",
                        variant="info",
                        size="sm",
                        on_click=on_resume
                    )
                    
                    AppButton(
                        tooltip="Restart Scan",
                        icon="refresh",
                        variant="error",
                        size="sm",
                        on_click=on_restart
                    )

                elif container.current_state == COMPLETED:
                    AppButton(
                        tooltip="Restart Scan",
                        icon="refresh",
                        variant="error",
                        size="sm",
                        on_click=on_restart
                    )

            # 2. Separator
            AppSeparator()

            # 3. Fast Mode Toggle
            AppToggle(
                icon="bolt",
                tooltip="Fast Mode",
                on_change=on_fast_mode,
                color=theme.colors.yellow if theme else "var(--c-accent-yellow)"
            )

    container.set_state = set_state
    _render()
    return container
