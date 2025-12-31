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
    with ui.row().classes(f'w-full items-center p-2 rounded cursor-pointer transition-colors border-b {theme.BORDER} border-opacity-10 gap-4').style(f'--hover-bg: {theme.SURFACE}80').classes('hover:bg-[var(--hover-bg)]') as row:
        
        # Icon
        # Re-using category badge logic for color? Or just style.
        # Let's use the same colors as category badge but apply to icon.
        colors = {
            'image': theme.CAT_IMAGE,
            'video': theme.CAT_VIDEO,
            'document': theme.CAT_DOC,
            'audio': theme.CAT_AUDIO,
            'other': theme.CAT_OTHER
        }
        color = colors.get(file_type.lower(), theme.CAT_OTHER)
        ui.icon(icon_name).style(f'color: {color}').classes('text-xl')
        
        # Name & Parent
        with ui.column().classes('flex-1 gap-0'):
            ui.label(name).classes('text-sm font-medium leading-tight')
            ui.label(parent).classes(f'text-xs {theme.TEXT_MUTED}')
            
        # Metadata
        ui.label(size).classes('text-xs font-mono opacity-70 w-16 text-right')
        ui.label(date).classes('text-xs font-mono opacity-50 w-24 text-right')
        
    return row
