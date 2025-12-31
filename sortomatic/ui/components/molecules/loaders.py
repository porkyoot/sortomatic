from nicegui import ui
from sortomatic.ui.style import theme
from typing import Optional

def lazy_loader(height: str = '4rem') -> ui.element:
    """
    Lazy Loader: A loading state using 'Skeleton' animations.
    """
    # Using Quasar's Q-Skeleton
    return ui.element('q-skeleton').props(f'type="rect" height="{height}" animation="pulse"').classes('w-full opacity-50')
