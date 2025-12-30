from nicegui import ui
from typing import Optional, Union, Dict
from .icons import AppIcon
from ...theme import CategoryStyles, StatusStyles
# from ...theme import Theme # REMOVED

def AppBadge(
    label: str,
    value: Optional[str] = None,
    icon: Optional[str] = None,
    color: str = 'var(--nt-primary)', # Updated to nicetheme var
    text_color: str = 'var(--nt-color-white)', # Updated to nicetheme var (or --nt-content-accent)
    variant: str = 'solid', # solid, glass, subtle
    on_click: Optional[callable] = None,
    interactive: bool = False,
    disabled: bool = False,
    icon_classes: str = "",
    tooltip: Optional[str] = None
):
    """
    A styled badge for displaying statuses, categories, or counts.
    Supports solid, glass (translucent), and subtle (no background) variants.
    """
    css_classes = ['s-badge']
    
    # Variants & State
    if variant:
        css_classes.append(f's-badge--{variant}')
        
    if (interactive or on_click) and not disabled:
        css_classes.append('s-badge--interactive')
        
    if disabled:
        css_classes.append('s-badge--disabled')
    
    # Dynamic Colors
    # We use CSS variables to pass the specific color to the semantic class logic
    style_vars = f"--badge-color: {color}; --badge-text: {text_color};"
    
    # Icon handling
    effective_icon_color = text_color
    if variant == 'simple':
        effective_icon_color = color
    
    with ui.row().classes(" ".join(css_classes)).style(style_vars) as badge:
        if on_click and not disabled:
            badge.on('click', on_click)
        elif on_click: # Still allow clicking for toggles even if disabled (e.g. to enable)
            badge.on('click', on_click)
            
        if icon:
            # We use the icon classes but let color be handled by parent or explicit
            AppIcon(icon, color=effective_icon_color, size='1.2em', classes=icon_classes)
        
        # Labels
        ui.label(label).classes('s-badge__label')
        
        if value:
            ui.label('|').classes('opacity-30')
            ui.label(value).classes('s-badge__value')
        
        if tooltip:
            ui.tooltip(tooltip).classes('text-[10px] font-bold')

def CategoryBadge(
    category: str,
    # theme: Theme, # REMOVED
    value: Optional[str] = None,
    icon: Optional[str] = None,
    interactive: bool = False,
    disabled: bool = False,
    on_click: Optional[callable] = None,
    variant: str = 'glass'
):
    """
    A specialized badge for categories with automatic coloring.
    """
    color = CategoryStyles.get_color(category) # Removed theme arg
    return AppBadge(
        label=category,
        value=value,
        icon=icon or CategoryStyles.get_icon(category),
        color=color,
        interactive=interactive,
        disabled=disabled,
        on_click=on_click,
        variant=variant
    )

def StatusBadge(
    label: str,
    state: str,
    # theme: Theme, # REMOVED
    value: Optional[str] = None,
    variant: str = 'solid',
    icon: Optional[Union[str, Dict[str, str]]] = None,
    rotate: bool = False,
    tooltip: Optional[str] = None,
    **kwargs
):
    """
    A specialized badge for statuses with automatic coloring and icon.
    Args:
        icon: Can be a single icon name (used for all states) or a dictionary mapping 
              state names (ready, error, pending, idle, unknown) to icon names.
        rotate: If True, applies rotation animation to the icon.
    """
    color = StatusStyles.get_color(state) # Removed theme arg
    
    # Resolve Icon
    effective_icon = None
    if isinstance(icon, dict):
        # Resolve state to canonical form (e.g. 'active' -> 'ready')
        resolved_state = StatusStyles.resolve_state(state)
        # Try specific state, then 'default', then fallback to standard styles
        effective_icon = icon.get(resolved_state) or icon.get('default')
    elif isinstance(icon, str):
        effective_icon = icon
        
    # Final fallback to standard status icons if no override provides one
    if not effective_icon:
        effective_icon = StatusStyles.get_icon(state)
        
    icon_cls = ""
    if rotate:
        icon_cls = "rotate-animation"

    return AppBadge(
        label=label,
        value=value,
        icon=effective_icon,
        color=color,
        text_color="var(--nt-color-white)",  # Use fixed light color or logic? For now white text is safe on colored badges
        variant=variant,
        icon_classes=icon_cls,
        tooltip=tooltip,
        **kwargs
    )

def CopyBadge(
    text_to_copy: str,
    label: str = "Copy",
    value: Optional[str] = None,
    icon: str = "mdi-content-copy",
    color: str = "var(--nt-primary)",
    variant: str = "glass",
    success_message: str = "Copied to clipboard!"
):
    """
    A badge that copies specific text to the clipboard when clicked.
    """
    def handle_copy():
        ui.clipboard.write(text_to_copy)
        ui.notify(success_message, type='positive', color='var(--nt-positive)')

    return AppBadge(
        label=label,
        value=value or (text_to_copy[:12] + "..." if len(text_to_copy) > 15 else text_to_copy),
        icon=icon,
        color=color,
        variant=variant,
        on_click=handle_copy,
        interactive=True
    )
