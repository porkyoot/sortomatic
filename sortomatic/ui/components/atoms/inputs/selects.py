from nicegui import ui
from typing import List, Dict, Any, Optional, Callable, Union

def AppSelect(
    options: Union[List[str], Dict[Any, str]],
    label: Optional[str] = None,
    value: Any = None,
    on_change: Optional[Callable] = None,
    multiple: bool = False,
    use_chips: bool = False,  # Default to False to prevent removable chips
    clearable: bool = True,
    variant: str = "default",  # default, simple
    classes: str = "",
    props: str = ""
):
    """
    A premium themed select component. 
    Supports multiple selection with chips and consistent rounding.
    
    Args:
        options: List of options or dict mapping values to labels
        label: Input label
        value: Initial value
        on_change: Callback when value changes
        multiple: Allow multiple selection
        use_chips: Show selected items as chips (when multiple=True)
        clearable: Show clear button
        variant: 'default' for standard input, 'simple' for text-only look
        classes: Additional CSS classes to apply
        props: Additional Quasar props to apply
    """
    # Determine variant classes
    select_classes = ["s-select"]
    base_props = "outlined dense hide-bottom-space rounded-app" # Quasar props that are structural
    
    if variant == "simple":
        select_classes.append("s-select--simple")
        base_props = "dense borderless options-dense behavior='menu'"
        classes += " p-0"
    
    # We still rely on Quasar props for structure (outlined, dense) as that's how Quasar inputs work
    
    sel = ui.select(
        options=options, 
        label=label, 
        value=value, 
        on_change=on_change
    ).props(
        f'{base_props} '
        f'{"multiple" if multiple else ""} {"use-chips" if use_chips else ""} '
        f'{props}'
    ).classes(f'{" ".join(select_classes)} {classes}')
    # No inline style() call needed as s-select handles color/bg
    
    if clearable:
        sel.props('clearable')

    # Apply theme colors to the popup menu via class
    sel.props('popup-content-class="s-select__popup"')
    # Removed popup-content-style, handled by CSS class
    
    return sel


