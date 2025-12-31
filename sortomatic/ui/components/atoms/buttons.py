from nicegui import ui
from sortomatic.ui.style import theme
from typing import Optional, Callable, Literal

def button(text: str = '', 
           icon: Optional[str] = None, 
           on_click: Optional[Callable] = None, 
           variant: Literal['primary', 'secondary', 'ghost'] = 'primary',
           shape: Literal['default', 'pill', 'circle', 'chevron', 'chevron-first', 'chevron-last'] = 'default',
           disabled: bool = False) -> ui.button:
    """
    Buttons: Override the NiceGUI button with Variants and Shapes.
    """
    classes = 'transition-all duration-200 '
    props = ''
    
    # Variants
    if variant == 'primary':
        classes += f'bg-[{theme.PRIMARY}] text-white hover:bg-opacity-90 '
        props += 'unelevated '
    elif variant == 'secondary':
        classes += f'bg-[{theme.SECONDARY}] text-white hover:bg-opacity-90 '
        props += 'unelevated '
    elif variant == 'ghost':
        classes += f'text-[{theme.TEXT_MAIN}] hover:bg-white/10 '
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
        
    btn = ui.button(text, icon=icon, on_click=on_click).classes(classes).props(props)
    
    if disabled:
        btn.disable()
        
    return btn

def nuclear_button(on_explode: Callable) -> ui.element:
    """
    Nuclear Button: 'Dangerous Action' button with Click & Hold mechanism.
    """
    # Using a custom HTML structure for the SVG overlay
    with ui.element('div').classes('relative inline-flex items-center justify-center p-4 group') as container:
        # Tooltip for danger
        ui.tooltip('DANGER: Hold to execute!').classes('bg-red-700 text-white font-bold')
        
        # The button itself
        with ui.button(icon='delete_forever').classes('nuclear-btn bg-black text-red-500 rounded-full w-16 h-16 z-10 border-2 border-red-500/50').props('round flat type="button"') as btn:
            # SVG Ring for animation
            # We place it "behind" or "around" the icon but inside the button or container. 
            pass
        
        # SVG Ring overlay
        svg_html = '''
        <svg class="absolute top-0 left-0 w-full h-full pointer-events-none transform -rotate-90" viewBox="0 0 64 64">
             <circle class="nuclear-loader-circle" cx="32" cy="32" r="20" />
        </svg>
        '''
        ui.html(svg_html, sanitize=False).classes('absolute top-0 left-0 w-full h-full pointer-events-none z-20')

        container.on('mousedown', js_handler='''
            () => {
                window.nuclearTimer = setTimeout(() => {
                    emitEvent('explode');
                }, 2000); 
            }
        ''')
        
        container.on('mouseup', js_handler='''
            () => {
                if (window.nuclearTimer) clearTimeout(window.nuclearTimer);
            }
        ''')
        
        container.on('mouseleave', js_handler='''
            () => {
                if (window.nuclearTimer) clearTimeout(window.nuclearTimer);
            }
        ''')
        
        container.on('explode', on_explode)
        
    return container
