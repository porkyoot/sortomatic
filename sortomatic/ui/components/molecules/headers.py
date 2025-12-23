from nicegui import ui
from typing import Optional, Callable
from ..atoms.icons import AppIcon

def PanelHeader(
    title: str,
    subtitle: Optional[str] = None,
    icon: Optional[str] = None,
    color: str = 'var(--q-primary)',
    right_content: Optional[Callable] = None
):
    """
    A premium header molecule for panels and sections.
    
    Args:
        title: Main text heading.
        subtitle: Secondary descriptive text.
        icon: Icon name.
        color: Accent color for the icon and subtle borders.
        right_content: A callable that renders the right-side component.
    """
    with ui.row().classes('w-full items-center justify-between pb-4 border-b border-opacity-10').style(f'border-color: {color};'):
        # 1. Left Section: Icon + Title Group
        with ui.row().classes('items-center gap-4'):
            if icon:
                # Decorative background for icon
                with ui.element('div').classes('p-3 rounded-app bg-opacity-10').style(f'background-color: {color};'):
                    AppIcon(icon, color=color, size='md')
            
            with ui.column().classes('gap-0'):
                ui.label(title).classes('text-xl font-bold tracking-tight')
                if subtitle:
                    ui.label(subtitle).classes('text-xs opacity-60 uppercase tracking-widest font-medium')
                    
        # 2. Right Section: Arbitrary Component
        if right_content:
            with ui.row().classes('items-center'):
                right_content()
