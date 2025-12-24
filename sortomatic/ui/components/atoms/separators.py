from nicegui import ui

def AppSeparator() -> ui.element:
    """A vertical separator pill."""
    return ui.element('div').classes('s-separator-vertical')