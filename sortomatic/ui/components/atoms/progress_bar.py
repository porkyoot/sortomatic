from nicegui import ui
from typing import Optional

def AppProgressBar(
    value: Optional[float] = 0.0,
    color: str = 'var(--q-primary)',
    shape: str = 'pill',  # 'pill' or 'rectangle'
    size: str = '12px',
    show_label: bool = False
):
    """
    A styled linear progress bar.
    """
    """
    A styled linear progress bar.
    """
    # Base class for the progress bar container
    container_classes = ["s-progress"]
    if shape == 'pill':
        container_classes.append("s-progress--pill")
    else:
        container_classes.append("s-progress--rect")
        
    bar = ui.linear_progress(value=value).classes(" ".join(container_classes)).style(
        f'color: {color}; height: {size};'
    ).props('instant-feedback')
    
    # Track (background) styling often needs to be more subtle
    bar.style(f'background-color: color-mix(in srgb, {color}, transparent 85%);')
    
    if show_label and value is not None:
        with bar:
            # text-white is handled by the class now
            ui.label(f'{int(value * 100)}%').classes('s-progress__label')
            
    return bar
