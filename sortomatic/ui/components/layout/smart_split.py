from nicegui import ui
from typing import Callable

class SmartSplitter(ui.element):
    """
    Responsive layout component that switches between column (mobile) and splitter (desktop).
    
    Uses factory functions to defer rendering, preventing double-execution of component logic.
    The factories are called once for mobile and once for desktop, but should be lightweight
    and share state through global controllers to avoid duplication.
    
    Usage:
        def left_panel():
            MyComponent()  # Reads from global state
        
        def right_panel():
            AnotherComponent()  # Reads from global state
        
        SmartSplitter().render(left_panel, right_panel, initial_split=30)
    
    Best Practice:
        - Factories should be lightweight wrappers that call component constructors
        - Heavy state/data should live in Controllers, not in the components
        - Avoid side effects in factories (API calls, database queries, etc.)
    """
    def __init__(self):
        super().__init__('div')
        self.classes('w-full h-full')
        
    def render(self, 
               left_factory: Callable[[], None], 
               right_factory: Callable[[], None],
               initial_split: int = 30,
               separator: bool = True):
        """
        Renders the responsive splitter layout.
        
        Args:
            left_factory: Function that renders the left/top content
            right_factory: Function that renders the right/bottom content
            initial_split: Initial splitter position (0-100), default 30
            separator: Whether to show separator in mobile view, default True
        """
        # Mobile: Column layout (hidden on large screens)
        # Uses CSS Grid approach for performance
        with ui.column().classes('w-full lg:hidden gap-0'):
            left_factory()
            if separator:
                ui.separator().classes('my-2')
            right_factory()

        # Desktop: Splitter layout (hidden on small screens)
        # Note: Both views render, but only one is visible at a time via CSS
        with ui.splitter(value=initial_split).classes('w-full h-full hidden lg:flex') as s:
            with s.before:
                left_factory()
            with s.after:
                right_factory()
        
        return self