from nicegui import ui
from sortomatic.ui.style import theme
from sortomatic.core.config import settings

def progress_bar() -> ui.linear_progress:
    """
    A fine, animated loading bar.
    """
    return ui.linear_progress().props('indeterminate size="2px" color="secondary" track-color="transparent"').classes('opacity-80')

def status_badge(text: str, state: str = 'unknown') -> ui.icon:
    """
    StatusBadge: Connectivity indicator icon with tooltip.
    States: unknown, disconnected, connecting, connected.
    """
    state_map = {
        'unknown': {'icon': 'mdi-cloud-question', 'class': 'text-grey'},        # debug
        'disconnected': {'icon': 'mdi-cloud-off-outline', 'class': 'text-negative'}, # error
        'connecting': {'icon': 'mdi-cloud-sync', 'class': 'text-warning'},     # warning
        'connected': {'icon': 'mdi-cloud-check', 'class': 'text-positive'},     # success
    }
    
    config = state_map.get(state, state_map['unknown'])
    
    # Icon with state color and tooltip
    # Using size='1.5rem' (24px) to match standard icon button size roughly
    icon = ui.icon(config['icon'], size='1.5rem').classes(config['class'])
    icon.tooltip(text)
    
    if state == 'connecting':
        icon.classes('animate-pulse')
        
    return icon

def category_badge(category: str) -> ui.element:
    """
    CategoryBadge: Specific to file types, with distinct colors.
    """
    # Get color from config (Source of Truth)
    color_name = settings.category_colors.get(category, "grey")
    
    classes = f'text-[10px] font-bold px-2 py-0.5 rounded-md border category-badge-base text-{color_name} bg-{color_name}-light border-current'
    return ui.label(category.upper()).classes(classes)
