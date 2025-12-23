from nicegui import ui
from typing import List, Dict, Any, Optional, Callable, Union

def AppSelect(
    options: Union[List[str], Dict[Any, str]],
    label: str = "",
    value: Any = None,
    on_change: Optional[Callable] = None,
    multiple: bool = False,
    use_chips: bool = True,
    clearable: bool = True
):
    """
    A premium themed select component. 
    Supports multiple selection with chips and consistent rounding.
    """
    sel = ui.select(
        options=options, 
        label=label, 
        value=value, 
        on_change=on_change
    ).props(
        f'outlined dense hide-bottom-space rounded-app '
        f'{"multiple" if multiple else ""} {"use-chips" if use_chips else ""} '
        f'{"clearable" if clearable else ""}'
    ).classes('w-full transition-all')

    # Apply global rounding to the popup menu as well
    sel.props('popup-content-class="rounded-app shadow-lg border border-[var(--q-primary)]"')
    
    return sel
