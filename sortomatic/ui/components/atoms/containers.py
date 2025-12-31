from nicegui import ui
from sortomatic.ui.style import theme

def card() -> ui.card:
    """
    A generic container with a subtle border and a background slightly lighter than the body.
    """
    return ui.card().classes('p-4 rounded-lg premium-glass')

def separator() -> ui.element:
    """
    A discreet, thin vertical divider.
    """
    return ui.element('div').classes('w-px h-full opacity-20 mx-2 thin-border bg-border')
