from nicegui import ui
from sortomatic.ui.style import theme
from sortomatic.ui.components import atoms
from typing import Optional, Callable

def scan_controls(
    on_play: Callable, 
    on_pause: Callable, 
    on_restart: Callable, 
    on_fast_forward: Callable, 
    scan_state: str = 'idle'
) -> ui.row:
    """
    Scan Controls: Cassette Player style.
    
    scan_state: 'idle', 'running', 'paused', 'completed'
    """
    with ui.row().classes('items-center p-2 rounded-full premium-glass border thin-border gap-1') as controls:
        
        # Visibility Logic
        can_restart = scan_state in ['running', 'paused', 'completed']
        can_pause = scan_state == 'running'
        can_play = scan_state != 'running'

        # Restart (Skip Previous style)
        atoms.button(icon='skip_previous', on_click=on_restart, variant='ghost', color='error', shape='circle') \
            .props('dense size="sm"') \
            .set_visibility(can_restart)
        
        # Play/Pause
        # We render both but toggle visibility to keep position or just one?
        # If we hide one, the other takes its place. This is fine for Play/Pause toggle.
        
        atoms.button(icon='play_arrow', on_click=on_play, variant='full', color='success', shape='circle') \
            .set_visibility(can_play)
            
        atoms.button(icon='pause', on_click=on_pause, variant='full', color='warning', shape='circle') \
            .set_visibility(can_pause)
        
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
        ff_btn = atoms.button(icon='fast_forward', on_click=toggle_ff, variant='ghost', color='info', shape='circle').props('dense size="sm"')
        ff_state = {'active': False}
        
        # To make it "stay pressed", we toggle a semantic color class or style.
        def toggle_style():
            ff_state['active'] = not ff_state['active']
            if ff_state['active']:
                ff_btn.classes(replace='text-warning').classes(remove='text-muted')
            else:
                ff_btn.classes(replace='text-muted').classes(remove='text-warning')
        
        ff_btn.on('click', toggle_style)
        ff_btn.classes('text-muted')
        
    return controls
