from nicegui import ui
from typing import Optional, Callable

def AppButton(
    label: str = "",
    icon: Optional[str] = None,
    on_click: Optional[Callable] = None,
    variant: str = 'primary', # primary, secondary, ghost
    shape: str = 'default',   # default, pill, square, circle, chevron, chevron-first, chevron-last
    size: str = 'md',         # xs, sm, md, lg
    state: str = 'enable',    # enable, disable, active
    tooltip: Optional[str] = None,
    color: Optional[str] = None,
):
    """
    Semantic Wrapper.
    No hardcoded styles here. Only semantic class names.
    """
    
    # 1. Base Class
    css_classes = ["s-btn"]
    
    # 2. Semantic Modifiers (BEM style naming convention)
    css_classes.append(f"s-btn--{variant}")
    css_classes.append(f"s-btn--{state}")
    
    if shape != 'default':
        css_classes.append(f"s-shape--{shape}")
        
    if size != 'md':
        css_classes.append(f"s-btn--{size}")

    # 3. Render
    # We use props('unelevated no-caps') to reset Quasar's defaults
    props = 'unelevated no-caps'
    
    # Map variants to native colors
    color_map = {
        'primary': 'primary',
        'secondary': 'secondary',
        'success': 'positive',
        'error': 'negative',
        'warning': 'warning',
        'info': 'info'
    }
    
    btn_color = color_map.get(variant)
    
    if variant in ['simple', 'ghost']:
        props += ' flat'
        btn_color = None
        
    # If explicit color is passed, it overrides the variant's color
    if color:
        btn_color = None # We'll set it via style

    btn = ui.button(label, icon=icon, on_click=on_click, color=btn_color) \
             .props(props) \
             .classes(" ".join(css_classes))
             
    if color:
        # For non-standard colors, we still use the CSS variable approach
        btn.style(f'background-color: {color} !important; color: white !important;')

    if state == 'disable':
        # Avoid Quasar's 'disabled' prop to prevent non-overridable dimming.
        # .s-btn--disable in CSS handles the visual state and pointer-events.
        pass

    if tooltip:
        btn.tooltip(tooltip)
        
    return btn