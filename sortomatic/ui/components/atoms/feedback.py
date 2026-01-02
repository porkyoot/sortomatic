from nicegui import ui
from sortomatic.ui.style import theme
from sortomatic.core.config import settings

def progress_bar() -> ui.linear_progress:
    """
    A fine, animated loading bar.
    """
    return ui.linear_progress().props('indeterminate size="2px" color="secondary" track-color="transparent"').classes('opacity-80')

def status_badge(active: bool = True, text: str = 'Active') -> ui.row:
    """
    StatusBadge: Simple visual indicator (colored dot + text) for activity/inactivity.
    """
    color_class = 'bg-success' if active else 'bg-muted'
    with ui.row().classes('items-center gap-2 text-xs') as badge:
        ui.element('div').classes(f'w-2 h-2 rounded-full shadow-sm {color_class}')
        ui.label(text).classes(f'text-muted')
    return badge

def category_badge(category: str) -> ui.element:
    """
    CategoryBadge: Specific to file types, with distinct colors.
    """
    # Get color from config (Source of Truth)
    color_name = settings.category_colors.get(category, "grey")
    
    classes = f'text-[10px] font-bold px-2 py-0.5 rounded-md border category-badge-base text-{color_name} bg-{color_name}-light border-current'
    return ui.label(category.upper()).classes(classes)
