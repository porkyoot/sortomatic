from nicegui import ui
from typing import Optional, Callable
from ...theme import apply_theme
from ..atoms.buttons import AppButton

class ThemeSelector(ui.row):
    """
    A theme and dark-mode selector component.
    Features a theme dropdown and a dynamic Sun/Moon toggle.
    """
    def __init__(self, 
                 current_theme: str = "solarized", 
                 is_dark: bool = True, 
                 on_change: Optional[Callable] = None):
        super().__init__()
        self.classes('items-center gap-3 px-3 py-1 rounded-app bg-white/5 border border-white/5')
        
        self.current_theme = current_theme
        self.is_dark = is_dark
        self.on_change = on_change
        
        self.render()

    def render(self):
        self.clear()
        with self:
            # 1. Theme Dropdown
            # Hardcoded options for now based on available theme files
            ui.select(
                options=["solarized"], 
                value=self.current_theme,
                on_change=self._handle_theme_change
            ).props('dense borderless dark flat hide-underline').classes('text-[10px] uppercase font-bold tracking-widest opacity-60 w-24')

            # 2. Vertical Divider
            ui.element('div').classes('w-px h-4 bg-white/10')

            # 3. Dynamic Toggle Button
            # Dark Mode Enabled -> Show Sun (to switch to light)
            # Light Mode Enabled -> Show Moon with stars (to switch to dark)
            if self.is_dark:
                # Orange Sun
                btn = AppButton(
                    icon="wb_sunny",
                    on_click=self._toggle_mode,
                    shape="circle",
                    variant="glass",
                    tooltip="Switch to Light Mode"
                ).style('--q-primary: #ff9800;') # Material Orange
            else:
                # Blue Moon with Stars (nights_stay)
                btn = AppButton(
                    icon="nights_stay",
                    on_click=self._toggle_mode,
                    shape="circle",
                    variant="glass",
                    tooltip="Switch to Dark Mode"
                ).style('--q-primary: #2196f3;') # Material Blue

    def _toggle_mode(self):
        self.is_dark = not self.is_dark
        ui.dark_mode(self.is_dark)
        self.render()
        if self.on_change:
            self.on_change(self.current_theme, self.is_dark)

    def _handle_theme_change(self, e):
        self.current_theme = e.value
        self.render()
        if self.on_change:
            self.on_change(self.current_theme, self.is_dark)
