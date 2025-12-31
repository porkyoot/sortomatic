from nicegui import ui
from sortomatic.ui.style import theme

def progress_bar() -> ui.linear_progress:
    """
    A fine, animated loading bar.
    """
    return ui.linear_progress().props('indeterminate size="2px" color="secondary" track-color="transparent"').classes('opacity-80')

def status_badge(active: bool = True, text: str = 'Active') -> ui.row:
    """
    StatusBadge: Simple visual indicator (colored dot + text) for activity/inactivity.
    """
    color = theme.PRIMARY if active else theme.TEXT_MUTED
    with ui.row().classes('items-center gap-2 text-xs') as badge:
        ui.element('div').classes('w-2 h-2 rounded-full').style(f'background-color: {color}')
        ui.label(text).classes(f'{theme.TEXT_MUTED}')
    return badge

def category_badge(category: str) -> ui.element:
    """
    CategoryBadge: Specific to file types, with distinct colors.
    """
    colors = {
        'image': 'var(--violet)',
        'video': 'var(--magenta)',
        'document': 'var(--blue)',
        'audio': 'var(--cyan)',
        'other': 'var(--base01)'
    }
    color = colors.get(category.lower(), colors['other'])
    
    return ui.label(category.upper()).classes('text-[10px] font-bold px-2 py-0.5 rounded-md border').style(f'color: {color}; border-color: {color}; background-color: rgba(0,0,0,0.1)')
