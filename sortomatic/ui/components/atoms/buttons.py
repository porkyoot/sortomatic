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
    if variant in ['simple', 'ghost']:
        props += ' flat'
        btn_color = None
    else:
        # If a custom color is provided, we set color=None to prevent Quasar 
        # from adding 'bg-primary' which is hard to override.
        btn_color = None if color else 'primary'
        
    btn = ui.button(label, icon=icon, on_click=on_click, color=btn_color) \
             .props(props) \
             .classes(" ".join(css_classes))
             
    if color:
        btn.style(f'--c-primary: {color}')

    if state == 'disable':
        btn.props('disabled')

    if tooltip:
        btn.tooltip(tooltip)
        
    return btn