from nicegui import ui
from typing import Optional, Callable

def AppToggle(
    value: bool = False,
    label: str = "",
    icon: Optional[str] = None,
    tooltip: Optional[str] = None,
    on_change: Optional[Callable] = None,
    color: Optional[str] = None,
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
    container = ui.row().classes(f's-toggle group {classes}')
    if color:
        container.style(f'--c-primary: {color}')

    with container:
        if tooltip:
            ui.tooltip(tooltip).classes('text-[10px] font-bold')
            
        if icon:
            ui.icon(icon, size='18px') \
                .classes('opacity-70 group-hover:opacity-100') \
                .style('color: var(--c-primary)')
            
        if label:
            ui.label(label) \
                .classes('text-[10px] font-bold uppercase tracking-widest opacity-70 group-hover:opacity-100') \
                .style('color: var(--c-primary)')

        # Custom Toggle Visual
        with ui.row().classes('s-toggle__switch') as toggle_bg:
            track = ui.element('div').classes('s-toggle__track')
            thumb = ui.label('●').classes('s-toggle__thumb')
            
            def update_ui(v: bool):
                if v:
                    # Active State (-●)
                    # Thumb on right, Track on left
                    thumb.style('right: 6px; left: auto; color: var(--c-primary);')
                    track.style('left: 8px; right: 14px; opacity: 0.4; background-color: var(--c-primary);')
                    
                    toggle_bg.classes('s-toggle__switch--active', remove='s-toggle__switch--inactive')
                    toggle_bg.style('border-color: var(--c-primary);')
                else:
                    # Inactive State (●-)
                    # Thumb on left, Track on right
                    thumb.style('left: 6px; right: auto; color: var(--c-text-subtle);')
                    track.style('left: 14px; right: 8px; opacity: 0.2; background-color: var(--c-text-subtle);')
                    
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

