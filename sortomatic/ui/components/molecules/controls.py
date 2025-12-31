from nicegui import ui
from sortomatic.ui.style import theme
from sortomatic.ui.components import atoms
from typing import Optional, Callable

def scan_controls(on_play: Callable, on_pause: Callable, on_restart: Callable, on_fast_forward: Callable) -> ui.row:
    """
    Scan Controls: Cassette Player style.
    """
    with ui.row().classes(f'items-center p-2 rounded-full {theme.GLASS} border {theme.BORDER} gap-1') as controls:
        
        # Restart (Skip Previous style)
        atoms.button(icon='skip_previous', on_click=on_restart, variant='ghost', shape='circle').props('dense size="sm"')
        
        # Play/Pause
        atoms.button(icon='play_arrow', on_click=on_play, variant='primary', shape='circle')
        atoms.button(icon='pause', on_click=on_pause, variant='secondary', shape='circle')
        
        # Fast Forward (Toggle)
        # We need state. Since this is a functional wrapper, we assume the caller handles logic or we use a toggle button.
        # NiceGUI toggle button? Or just a button that changes color.
        # Let's use a button that toggles its own local state visual or expects the callback to handle it.
        # For a "stays pressed" look, we might need a custom class or component state.
        # Simple approach: The user provides a reactive state or we just callback.
        # The prompt says "toggle state, stays pressed".
        
        def toggle_ff(e):
            e.sender.props(add='flat' if 'unelevated' in e.sender._props.get('props', '') else 'unelevated') # Toggle visual roughly? 
            # Better: Toggle color or opacity.
            # Let's just create a toggle-able button.
        ff_btn = atoms.button(icon='fast_forward', on_click=toggle_ff, variant='ghost', shape='circle').props('dense size="sm"')
        ff_state = {'active': False}
        
        # To make it "stay pressed", we toggle a semantic color class or style.
        # We'll use style for direct color binding to theme tokens.
        def toggle_style():
            ff_state['active'] = not ff_state['active']
            color = theme.WARNING if ff_state['active'] else theme.TEXT_MUTED
            ff_btn.style(f'color: {color}')
        
        ff_btn.on('click', toggle_style)
        ff_btn.style(f'color: {theme.TEXT_MUTED}')
        
    return controls
