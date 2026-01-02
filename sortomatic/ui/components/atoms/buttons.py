from nicegui import ui
from sortomatic.ui.style import theme
from typing import Optional, Callable, Literal

def button(text: str = '', 
           icon: Optional[str] = None, 
           on_click: Optional[Callable] = None, 
           variant: Literal['full', 'ghost'] = 'full',
           color: Optional[Literal['primary', 'secondary', 'warning', 'info', 'success', 'error', 'debug']] = None,
           shape: Literal['default', 'pill', 'circle', 'chevron', 'chevron-first', 'chevron-last'] = 'default',
           disabled: bool = False) -> ui.button:
    """
    Buttons: Override the NiceGUI button with Variants, Colors, and Shapes.
    
    Args:
        text: Button text
        icon: Optional icon name
        on_click: Click handler callback
        variant: 'full' (filled background) or 'ghost' (transparent with hover)
        color: Semantic color - 'primary', 'secondary', 'warning', 'info', 'success', 'error', 'debug'
        shape: Button shape style
        disabled: Whether button is disabled
    """
    # Default color logic based on variant
    if color is None:
        color = 'debug' if variant == 'ghost' else 'primary'
    classes = 'transition-all duration-200 '
    props = ''
    
    # Variants - use semantic button classes from CSS (respects design token hierarchy)
    if variant == 'full':
        classes += f'btn-{color} text-bg hover:bg-opacity-90 '
        props += 'unelevated '
    elif variant == 'ghost':
        classes += f'btn-{color}-text hover:bg-surface hover:bg-opacity-10 '
        props += 'flat '
    
    # Shapes
    if shape == 'pill':
        classes += 'rounded-full '
    elif shape == 'circle':
        classes += 'rounded-full px-0 aspect-square ' # aspect-square helps but might need w/h fixing if content varies
    elif shape == 'chevron':
        classes += 'btn-chevron rounded-lg '
    elif shape == 'chevron-first':
        classes += 'btn-chevron-first rounded-lg '
    elif shape == 'chevron-last':
        classes += 'btn-chevron-last rounded-lg '
    else:
        classes += 'rounded-lg ' # Default
        
    btn = ui.button(text, icon=icon, on_click=on_click, color=None).classes(classes).props(props)
    
    if disabled:
        btn.disable()
        
    return btn

def nuclear_button(on_explode: Callable) -> ui.element:
    """
    Nuclear Button: 'Dangerous Action' button with Click & Hold mechanism.
    Shows a border that draws clockwise around the button when pressed.
    """
    with ui.element('div').classes('relative inline-flex items-center justify-center') as container:
        # Tooltip for danger
        ui.tooltip('DANGER: Hold to execute!').classes('bg-opacity-80 font-bold nuclear-tooltip')
        
        # The button itself - CSS will handle the border animation
        btn_classes = 'nuclear-btn bg-primary text-white hover:bg-opacity-90 rounded-lg transition-all'
        btn = ui.button(icon='delete_forever').classes(btn_classes).props('unelevated type="button"')

        # JavaScript to add/remove 'nuclear-active' class and handle timing
        container.on('mousedown', js_handler='''
            (e) => {
                const btn = e.currentTarget.querySelector('.nuclear-btn');
                btn.classList.add('nuclear-active');
                window.nuclearTimer = setTimeout(() => {
                    emitEvent('explode');
                    btn.classList.remove('nuclear-active');
                }, 2000); 
            }
        ''')
        
        container.on('mouseup', js_handler='''
            (e) => {
                const btn = e.currentTarget.querySelector('.nuclear-btn');
                btn.classList.remove('nuclear-active');
                if (window.nuclearTimer) clearTimeout(window.nuclearTimer);
            }
        ''')
        
        container.on('mouseleave', js_handler='''
            (e) => {
                const btn = e.currentTarget.querySelector('.nuclear-btn');
                btn.classList.remove('nuclear-active');
                if (window.nuclearTimer) clearTimeout(window.nuclearTimer);
            }
        ''')
        
        container.on('explode', on_explode)
        
    return container
