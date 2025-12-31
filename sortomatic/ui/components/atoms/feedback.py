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
    color_class = 'bg-success' if active else 'bg-muted'
    with ui.row().classes('items-center gap-2 text-xs') as badge:
        ui.element('div').classes(f'w-2 h-2 rounded-full shadow-sm {color_class}')
        ui.label(text).classes(f'text-muted')
    return badge

def category_badge(category: str) -> ui.element:
    """
    CategoryBadge: Specific to file types, with distinct colors.
    """
    cat_keys = {
        'image': 'cat-image',
        'video': 'cat-video',
        'document': 'cat-doc',
        'audio': 'cat-audio',
        'other': 'cat-other'
    }
    key = cat_keys.get(category.lower(), 'cat-other')
    
    classes = f'text-[10px] font-bold px-2 py-0.5 rounded-md border category-badge-base text-{key} bg-{key}-light border-current'
    return ui.label(category.upper()).classes(classes)
