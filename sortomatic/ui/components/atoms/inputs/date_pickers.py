from nicegui import ui
from typing import Optional, Callable, Union

def AppDatePicker(
    label: str = "Date",
    value: Optional[Union[str, dict]] = None,
    mode: str = 'single', # 'single' or 'range'
    on_change: Optional[Callable] = None,
    icon: str = 'mdi-calendar',
    classes: str = "",
    props: str = ""
):
    """
    A premium themed date picker input.
    
    Args:
        label: Input label
        value: Initial value (ISO string for 'single', dict {'from': '...', 'to': '...'} for 'range')
        mode: 'single' for a specific day, 'range' for a period
        on_change: Callback when date is selected
        icon: Icon to show in the input
        classes: Additional CSS classes to apply
        props: Additional Quasar props to apply
    """
    with ui.input(label, value=value).props(
        f'outlined dense hide-bottom-space rounded-app {props}'
    ).classes(f'w-full {classes}') as date_input:
        with date_input.add_slot('append'):
            ui.icon(icon).classes('cursor-pointer').on('click', lambda: menu.open())
        
        with ui.menu() as menu:
            def handle_change(e):
                val = e.value
                if mode == 'range' and isinstance(val, dict):
                    display = f"{val['from']} → {val['to']}" if 'from' in val and 'to' in val else str(val)
                else:
                    display = str(val)
                
                date_input.set_value(display)
                if on_change:
                    on_change(val)
                if mode == 'single':
                    menu.close()

            date_picker = ui.date(value=value, on_change=handle_change)
            
            if mode == 'range':
                date_picker.props('range')
                # For range, we might want a manual "Apply" button inside the menu to close it
                with ui.row().classes('s-date-picker__actions'):
                    ui.button('Apply', on_click=menu.close).props('flat dense')

    # Apply global rounding and font if possible via classes
    date_input.classes('rounded-app')
    
    return date_input

