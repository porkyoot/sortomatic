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
    # Determine styles based on variant
    if variant == "simple":
        base_props = "dense borderless options-dense behavior='menu'"
        base_style = "background-color: transparent; min-height: unset;"
        # For simple variant, we might want to remove padding to align with text
        classes += " p-0"
    else:
        base_props = "outlined dense hide-bottom-space rounded-app"
        base_style = "background-color: var(--app-bg);"

    sel = ui.select(
        options=options, 
        label=label, 
        value=value, 
        on_change=on_change
    ).props(
        f'{base_props} '
        f'{"multiple" if multiple else ""} {"use-chips" if use_chips else ""} '
        f'{props}'
    ).classes(f'w-full transition-all {classes}').style(
        f'color: var(--app-text); {base_style}'
    )
    
    # Only add clearable prop if explicitly requested and NOT simple (usually)
    # But user might want clearable simple select? Default clearable=True in sig.
    if clearable:
        sel.props('clearable')

    # Apply theme colors to the popup menu
    sel.props('popup-content-class="rounded-app shadow-lg border"')
    sel.props('popup-content-style="background-color: var(--app-bg); color: var(--app-text);"')
    
    return sel


