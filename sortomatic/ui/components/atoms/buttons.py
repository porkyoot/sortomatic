from nicegui import ui
from typing import Optional, Callable

def AppButton(
    text: str = "",
    icon: Optional[str] = None,
    on_click: Optional[Callable] = None,
    color: str = 'var(--q-primary)',
    variant: str = 'primary', # 'primary', 'secondary', 'simple', 'ghost'
    shape: str = 'rectangle', # 'rectangle', 'pill', 'circle', 'chevron-left', 'chevron-mid', 'chevron-right'
    size: str = 'md',        # 'xs', 'sm', 'md', 'lg', 'xl'
    rounded: bool = True,
    tooltip: Optional[str] = None
):
    """
    A unified button component for the application.
    
    Shapes:
    - rectangle: Standard button.
    - pill: Fully rounded ends.
    - circle: Square aspect ratio, 50% radius.
    - chevron-left: Process step (Start).
    - chevron-mid: Process step (Middle).
    - chevron-right: Process step (End).
    """
    btn = ui.button(text, icon=icon, on_click=on_click).props(f'unelevated no-caps size={size}')
    
    # Base classes
    classes = "transition-transform hover:scale-105 active:scale-95 "
    styles = []
    
    # 1. SHAPE LOGIC
    if shape == 'pill':
        classes += "rounded-full px-6 "
    elif shape == 'circle':
        classes += "rounded-full aspect-square p-0 min-w-[3em] "
    elif shape == 'rectangle':
        if rounded:
            classes += "rounded-app "
        else:
            classes += "rounded-none "
    elif 'chevron' in shape:
        classes += "rounded-none px-8 "
        # Chevron clip paths
        # x-offset for the triangle is 15%
        if shape == 'chevron-left':
            styles.append('clip-path: polygon(0% 0%, 85% 0%, 100% 50%, 85% 100%, 0% 100%)')
        elif shape == 'chevron-mid':
            styles.append('clip-path: polygon(15% 0%, 85% 0%, 100% 50%, 85% 100%, 15% 100%, 0% 50%)')
        elif shape == 'chevron-right':
            styles.append('clip-path: polygon(15% 0%, 100% 0%, 100% 100%, 0% 100%, 15% 50%)')

    # 2. VARIANT LOGIC
    if variant == 'primary':
        styles.append(f'background-color: {color} !important; color: var(--app-bg);')
        classes += "shadow-sm "
    elif variant == 'secondary':
        styles.append(f'background-color: var(--q-secondary) !important; color: var(--app-bg);')
        classes += "shadow-sm "
    elif variant == 'simple':
        btn.props('flat')
        styles.append(f'color: {color} !important;')
    elif variant == 'ghost':
        btn.props('outline')
        styles.append(f'color: {color} !important; border-color: {color} !important;')
        
    if tooltip:
        btn.tooltip(tooltip)
        
    return btn.classes(classes).style(';'.join(styles))