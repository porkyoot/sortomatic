from nicegui import ui
from sortomatic.ui.style import theme

def card() -> ui.card:
    """
    A generic container with a subtle border and a background slightly lighter than the body.
    """
    return ui.card().classes(f'bg-opacity-10 p-4 rounded-lg {theme.BORDER} {theme.SHADOW} backdrop-blur-md').style(f'background-color: {theme.SURFACE};')

def separator() -> ui.element:
    """
    A discreet, thin vertical divider.
    """
    return ui.element('div').classes(f'w-px h-full opacity-20 mx-2 {theme.BORDER}').style(f'background-color: {theme.BORDER_COLOR}')
