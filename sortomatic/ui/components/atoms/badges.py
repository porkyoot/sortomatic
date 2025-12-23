from nicegui import ui
from typing import Optional
from .icons import AppIcon

def AppBadge(
    label: str,
    value: Optional[str] = None,
    icon: Optional[str] = None,
    color: str = 'var(--q-primary)',
    text_color: str = 'var(--app-text)'
):
    """
    A styled badge for displaying statuses, categories, or counts.
    Format: [Icon] Label [: Value]
    """
    with ui.row().classes('items-center gap-1.5 px-3 py-1 rounded-app shadow-sm').style(
        f'background-color: {color}; color: {text_color}; width: fit-content;'
    ):
        if icon:
            AppIcon(icon, color=text_color, size='1.2em')
        
        ui.label(label).classes('text-xs font-medium uppercase tracking-wider')
        
        if value:
            ui.label('|').classes('opacity-30')
            ui.label(value).classes('text-xs font-bold')
