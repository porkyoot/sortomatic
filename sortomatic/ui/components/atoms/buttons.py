from nicegui import ui
from sortomatic.ui.style import theme
from typing import Optional, Callable, Literal

def button(text: str = '', 
           icon: Optional[str] = None, 
           on_click: Optional[Callable] = None, 
           variant: Literal['full', 'ghost'] = 'full',
           color: Optional[str] = None,
           shape: Literal['default', 'pill', 'circle', 'chevron', 'chevron-first', 'chevron-last'] = 'default',
           disabled: bool = False) -> ui.button:
    """
    Buttons: Override the NiceGUI button with Variants, Colors, and Shapes.
    
    Args:
        text: Button text
        icon: Optional icon name
        on_click: Click handler callback
        variant: 'full' (filled background) or 'ghost' (transparent with hover)
        color: Semantic color ('primary', 'warning', etc.) OR any valid CSS/Quasar color name
        shape: Button shape style
        disabled: Whether button is disabled
    """
    # Default color logic based on variant
    if color is None:
        color = 'debug' if variant == 'ghost' else 'primary'

    classes = 'transition-all duration-200 '
    props = ''
    
    # Check if color is a known semantic variant (defined in CSS/Theme)
    semantic_colors = ['primary', 'secondary', 'warning', 'info', 'success', 'error', 'debug', 'suggest']
    is_semantic = color in semantic_colors
    
    # Variants
    if variant == 'full':
        if is_semantic:
            classes += f'btn-{color} '
        else:
            # For non-semantic colors (e.g. 'purple', 'pink'), let NiceGUI handle the background color
            # NiceGUI usually defaults to white text for dark colors, but we can force it if needed.
            # Assuming recent non-semantic buttons (Pink, Purple) were fine (White text), we leave them.
            pass 
            
        classes += 'hover:bg-opacity-90 '
        props += 'unelevated '
        
    elif variant == 'ghost':
        if is_semantic:
            classes += f'btn-{color}-text '
        else:
            # For ghost non-semantic, we might need manual text coloring classes or style
            classes += f'text-{color} '
            
        classes += 'hover:bg-surface hover:bg-opacity-10 '
        props += 'flat '
    
    # Shapes
    if shape == 'pill':
        classes += 'rounded-full '
    elif shape == 'circle':
        classes += 'rounded-full px-0 aspect-square ' 
    elif shape == 'chevron':
        classes += 'btn-chevron rounded-lg '
    elif shape == 'chevron-first':
        classes += 'btn-chevron-first rounded-lg '
    elif shape == 'chevron-last':
        classes += 'btn-chevron-last rounded-lg '
    else:
        classes += 'rounded-lg ' # Default
        
    # If it is semantic, we set color=None to avoid NiceGUI overriding our CSS classes with Quasar generic colors
    # If it is NOT semantic (e.g. 'purple'), we pass it to NiceGUI to handle
    ng_color = None if is_semantic else color
        
    btn = ui.button(text, icon=icon, on_click=on_click, color=ng_color).classes(classes).props(props)
    
    if disabled:
        btn.disable()
        
    return btn

def nuclear_button(on_explode: Callable, text: str = '', color: str = 'warning', icon: str = 'delete_forever', tooltip: str = 'DANGER: Hold to execute!') -> ui.element:
    """
    Nuclear Button: 'Dangerous Action' button with Click & Hold mechanism.
    Shows a border that draws clockwise around the button when pressed.
    """
    with ui.element('div').classes('relative inline-flex items-center justify-center') as container:
        # Tooltip for danger
        ui.tooltip(tooltip).classes('bg-opacity-80 font-bold nuclear-tooltip')
        
        # The button itself
        # We try to map the requested semantic color to a background class if possible, or use inline style/NiceGUI color
        # Since this is a custom div wrapper, we manually apply classes. 
        
        # User requested round button.
        # Removed text-bg to allow CSS to determine text color (usually var(--color-white)/Base3)
        btn_classes = f'nuclear-btn btn-{color} hover:bg-opacity-90 rounded-full transition-all aspect-square'
        
        btn = ui.button(text, icon=icon).classes(btn_classes).props('unelevated type="button"')
        
        # We need to ensure the button doesn't have the default NiceGUI color overriding our class
        btn.props(remove='color') 
        btn._props['color'] = None 

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
