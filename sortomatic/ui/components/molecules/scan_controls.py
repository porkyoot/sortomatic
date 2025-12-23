from nicegui import ui
from typing import Optional, Callable
from ...theme import ColorPalette
from ..atoms.buttons import AppButton
from ..atoms.inputs.toggles import AppToggle

class ScanControls(ui.row):
    """
    A context-aware scan control component.
    Switches buttons based on scan state and includes a fast-mode toggle.
    """
    
    # State constants
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"

    def __init__(self, 
                 state: str = "idle", 
                 palette: ColorPalette = None,
                 on_play: Optional[Callable] = None,
                 on_pause: Optional[Callable] = None,
                 on_resume: Optional[Callable] = None,
                 on_restart: Optional[Callable] = None,
                 on_fast_mode: Optional[Callable] = None):
        super().__init__()
        self.classes('items-center gap-4 py-2 px-4 rounded-app bg-white/5 border border-white/5')
        
        self.state = state
        self.palette = palette
        self.on_play = on_play
        self.on_pause = on_pause
        self.on_resume = on_resume
        self.on_restart = on_restart
        self.on_fast_mode = on_fast_mode
        
        self.render()

    def set_state(self, new_state: str):
        self.state = new_state
        self.render()

    def render(self):
        self.clear()
        with self:
            # 1. State-based Buttons
            with ui.row().classes('items-center gap-2'):
                if self.state == self.IDLE:
                    AppButton(
                        label="Start Scan",
                        icon="play_arrow",
                        variant="primary",
                        on_click=self.on_play
                    ).style(f'--q-primary: {self.palette.green if self.palette else "var(--q-success)"}')
                
                elif self.state == self.RUNNING:
                    AppButton(
                        label="Pause",
                        icon="pause",
                        variant="primary",
                        on_click=self.on_pause
                    ).style(f'--q-primary: {self.palette.yellow if self.palette else "var(--q-warning)"}')
                
                elif self.state == self.PAUSED:
                    AppButton(
                        label="Resume",
                        icon="play_arrow",
                        variant="primary",
                        on_click=self.on_resume
                    ).style(f'--q-primary: {self.palette.blue if self.palette else "var(--q-info)"}')
                    
                    AppButton(
                        label="Restart",
                        icon="refresh",
                        variant="primary",
                        on_click=self.on_restart
                    ).style(f'--q-primary: {self.palette.red if self.palette else "var(--q-error)"}')

                elif self.state == self.COMPLETED:
                    AppButton(
                        label="Restart Scan",
                        icon="refresh",
                        variant="primary",
                        on_click=self.on_restart
                    ).style(f'--q-primary: {self.palette.red if self.palette else "var(--q-error)"}')

            # 2. Separator
            ui.element('div').classes('w-px h-6 bg-white/10 mx-2')

            # 3. Fast Mode Toggle
            AppToggle(
                label="Fast Mode",
                icon="bolt",
                tooltip="Enable high-concurrency partial scanning",
                on_change=self.on_fast_mode
            )
