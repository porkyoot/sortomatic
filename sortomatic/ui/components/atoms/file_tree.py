from nicegui import ui
from sortomatic.ui.style import theme
from typing import List, Dict, Any, Optional, Callable

def simple_file_tree(data: List[Dict[str, Any]], on_select: Optional[Callable] = None) -> ui.tree:
    """
    A robust, themed file explorer tree component.
    Renders a provided tree structure.
    """
    with ui.scroll_area().classes('w-full h-full'):
         tree = ui.tree(data, label_key='label', on_select=on_select)
         tree.props('node-key=id tick-strategy=none')
         # Theme formatting can be done via classes instead of style injection for better consistency
         # but following old/file_tree.py which used style injection:
         # tree.style(f'color: {AppTheme.TEXT_PRIMARY}') -> We use Tailwind classes if possible
         tree.classes('text-main')
         
         # Restore expansion (timers from original code)
         ui.timer(0.1, tree.expand)
         ui.timer(0.5, tree.expand)
         
    return tree
