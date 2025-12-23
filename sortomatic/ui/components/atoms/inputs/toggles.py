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
    with ui.row().classes(
        f'items-center gap-2 cursor-pointer group px-2 py-1 rounded-app hover:bg-white/5 transition-all {classes}'
    ) as container:
        if tooltip:
            ui.tooltip(tooltip).classes('text-[10px] font-bold')
            
        if icon:
            ui.icon(icon, size='18px').classes('opacity-70 group-hover:opacity-100')
            
        if label:
            ui.label(label).classes('text-[10px] font-bold uppercase tracking-widest opacity-70 group-hover:opacity-100')

        # Custom Toggle Visual (-*) or (*-)
        bg_color = 'var(--q-primary)'
        
        with ui.row().classes('items-center no-wrap bg-white/10 rounded-full px-1.5 py-0.5 border border-white/10 relative w-12 transition-all') as toggle_bg:
            track = ui.label('-').classes('text-xs opacity-30 font-black absolute transition-all')
            thumb = ui.label('●').classes('text-sm transition-all absolute')
            
            def update_ui(v: bool):
                # Toggle logic for (-*) vs (*-)
                if v:
                    # (*-)
                    track.style('right: 8px; left: auto;')
                    thumb.style('right: auto; left: 6px;')
                    thumb.classes('color-[var(--q-primary)]', remove='color-[var(--app-text-sec)]')
                    toggle_bg.classes('border-[var(--q-primary)]/40 bg-[var(--q-primary)]/10')
                else:
                    # (-*)
                    track.style('left: 8px; right: auto;')
                    thumb.style('left: auto; right: 6px;')
                    thumb.classes('color-[var(--app-text-sec)]', remove='color-[var(--q-primary)]')
                    toggle_bg.classes('border-white/10 bg-white/10')

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

