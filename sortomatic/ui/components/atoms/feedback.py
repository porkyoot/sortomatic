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
    color = theme.SUCCESS if active else theme.TEXT_MUTED
    with ui.row().classes('items-center gap-2 text-xs') as badge:
        ui.element('div').classes('w-2 h-2 rounded-full shadow-sm').style(f'background-color: {color}')
        ui.label(text).classes(f'text-[{theme.TEXT_MUTED}]')
    return badge

def category_badge(category: str) -> ui.element:
    """
    CategoryBadge: Specific to file types, with distinct colors.
    """
    colors = {
        'image': theme.CAT_IMAGE,
        'video': theme.CAT_VIDEO,
        'document': theme.CAT_DOC,
        'audio': theme.CAT_AUDIO,
        'other': theme.CAT_OTHER
    }
    color = colors.get(category.lower(), theme.CAT_OTHER)
    
    return ui.label(category.upper()).classes('text-[10px] font-bold px-2 py-0.5 rounded-md border').style(f'color: {color}; border-color: {color}; background-color: {color}15')
