from nicegui import ui
from typing import Optional, Callable

def AppToggle(
    value: bool = False,
    label: str = "",
    icon: Optional[str] = None,
    tooltip: Optional[str] = None,
    on_change: Optional[Callable] = None,
    classes: str = ""
):
    """
    A premium toggle component that looks like (-*) or (*-).
    
    Args:
        value: Initial toggle state
        label: Label text to display
        icon: Optional icon to display
        tooltip: Optional tooltip text
        on_change: Callback when toggle state changes
        classes: Additional CSS classes to apply to container
    """
    # Outer Container
    with ui.row().classes(f's-toggle group {classes}') as container:
        if tooltip:
            ui.tooltip(tooltip).classes('text-[10px] font-bold')
            
        if icon:
            ui.icon(icon, size='18px').classes('opacity-70 group-hover:opacity-100')
            
        if label:
            ui.label(label).classes('text-[10px] font-bold uppercase tracking-widest opacity-70 group-hover:opacity-100')

        # Custom Toggle Visual (-*) or (*-)
        with ui.row().classes('s-toggle__switch').style('border-color: var(--c-text-subtle);') as toggle_bg:
            track = ui.label('-').classes('s-toggle__track')
            thumb = ui.label('●').classes('s-toggle__thumb')
            
            def update_ui(v: bool):
                # Toggle logic for (-*) vs (*-)
                if v:
                    # (*-)
                    track.style('right: 8px; left: auto;')
                    thumb.style('right: auto; left: 6px;')
                    thumb.style('color: var(--c-primary);')
                    
                    toggle_bg.classes('s-toggle__switch--active', remove='s-toggle__switch--inactive')
                    toggle_bg.style('border-color: var(--c-primary);') # Keep manual override for safety if classes fail or lag
                else:
                    # (-*)
                    track.style('left: 8px; right: auto;')
                    thumb.style('left: auto; right: 6px;')
                    thumb.style('color: var(--c-text-subtle);')
                    
                    toggle_bg.classes('s-toggle__switch--inactive', remove='s-toggle__switch--active')
                    toggle_bg.style('border-color: var(--c-text-subtle);')

            # Initial state
            state = {'value': value}
            update_ui(state['value'])

            def toggle():
                state['value'] = not state['value']
                update_ui(state['value'])
                if on_change:
                    on_change(state['value'])
            
            container.on('click', toggle)

    return container

