from nicegui import ui
from sortomatic.ui.style import theme
from sortomatic.ui.components import atoms
from typing import Optional, Callable, List

def file_row(name: str, parent: str, size: str, date: str, file_type: str = 'other') -> ui.row:
    """
    File Row: Icon (color-coded), Name, Parent, Size, Date.
    """
    # Map types to icons
    icons = {
        'image': 'image',
        'video': 'movie',
        'audio': 'audiotrack',
        'document': 'description',
        'other': 'insert_drive_file'
    }
    icon_name = icons.get(file_type.lower(), icons['other'])
    
    # We use our atomic card but maybe lighter or just a row with hover effect
    with ui.row().classes('w-full items-center p-2 rounded cursor-pointer transition-colors border-b thin-border border-opacity-10 gap-4 file-row-hover') as row:
        
        # Icon
        # Re-using category badge logic for color? Or just style.
        # Let's use the same colors as category badge but apply to icon.
        cat_classes = {
            'image': 'text-cat-image',
            'video': 'text-cat-video',
            'document': 'text-cat-doc',
            'audio': 'text-cat-audio',
            'other': 'text-cat-other'
        }
        color_class = cat_classes.get(file_type.lower(), 'text-cat-other')
        ui.icon(icon_name).classes(f'text-xl {color_class}')
        
        # Name & Parent
        with ui.column().classes('flex-1 gap-0'):
            ui.label(name).classes('text-sm font-medium leading-tight')
            ui.label(parent).classes('text-xs text-muted')
            
        # Metadata
        ui.label(size).classes('text-xs font-mono opacity-70 w-16 text-right')
        ui.label(date).classes('text-xs font-mono opacity-50 w-24 text-right')
        
    return row
