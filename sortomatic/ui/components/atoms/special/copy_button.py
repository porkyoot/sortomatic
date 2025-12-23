from nicegui import ui
from typing import Optional
from ..buttons import AppButton

def CopyButton(
    text_to_copy: str,
    label: str = "",
    icon: str = "content_copy",
    variant: str = "simple",
    size: str = "sm",
    color: str = "var(--q-primary)",
    tooltip: Optional[str] = None,
    success_message: str = "Copied to clipboard!"
):
    """
    A button that copies specific text to the clipboard on click.
    """
    def do_copy():
        ui.clipboard.write(text_to_copy)
        ui.notify(success_message, type='positive', color='var(--q-success)')
    
    btn = AppButton(
        text=label,
        icon=icon,
        variant=variant,
        size=size,
        color=color,
        on_click=do_copy,
        tooltip=tooltip or f"Copy: {text_to_copy}"
    )
    
    return btn
