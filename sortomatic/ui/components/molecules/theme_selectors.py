from nicegui import ui
from typing import Optional, Callable
from ..atoms.buttons import AppButton
from ..atoms.inputs.selects import AppSelect

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
        self.classes('s-theme-selector shadow-sm')

        self.current_theme = current_theme
        self.is_dark = is_dark
        self.on_change = on_change
        
        self.render()

    def render(self):
        self.clear()
        with self:
            # 1. Theme Dropdown (AppSelect)
            AppSelect(
                options={'solarized': 'Solarized'},
                value=self.current_theme,
                on_change=lambda e: self._handle_theme_change(e.value),
                variant="simple",
                clearable=False,
                classes='s-label-uppercase-bold'
            )

            # 2. Vertical Divider
            ui.element('div').classes('s-separator-vertical')

            # 3. Dynamic Toggle Button
            # Dark Mode Enabled -> Show Sun (to switch to light)
            # Light Mode Enabled -> Show Moon with stars (to switch to dark)
            if self.is_dark:
                # Orange Sun
                btn = AppButton(
                    icon="mdi-white-balance-sunny",
                    on_click=self._toggle_mode,
                    shape="circle",
                    size="xs",  # Reduced to XS to match dense badges
                    variant="simple",
                    tooltip="Switch to Light Mode"
                ).classes('s-theme-toggle--light')
            else:
                # Blue Moon with Stars (nights_stay)
                btn = AppButton(
                    icon="mdi-weather-night",
                    on_click=self._toggle_mode,
                    shape="circle",
                    size="xs",  # Reduced to XS
                    variant="simple",
                    tooltip="Switch to Dark Mode"
                ).classes('s-theme-toggle--dark')

    def _toggle_mode(self):
        self.is_dark = not self.is_dark
        ui.dark_mode(self.is_dark)
        self.render()
        if self.on_change:
            self.on_change(self.current_theme, self.is_dark)

    def _handle_theme_change(self, theme_name: str):
        self.current_theme = theme_name.lower()
        self.render()
        if self.on_change:
            self.on_change(self.current_theme, self.is_dark)
