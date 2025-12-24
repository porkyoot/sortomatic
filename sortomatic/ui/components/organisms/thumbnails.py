from nicegui import ui
from typing import Optional, Union, List
from ..atoms.cards import AppCard

class AppThumbnail(AppCard):
    """
    A premium square thumbnail component for diverse file previews.
    Supports Images, Raw Text, HTML/PDF samples, and Static Tree snapshots.
    """
    def __init__(self, 
                 type: str = 'image', # 'image', 'text', 'html', 'tree'
                 content: Union[str, List[str]] = "",
                 size: str = '180px'):
        
        # Use subtle variant for thumbnails to let the content shine
        # We replace the base card logic with our custom s-thumbnail class logic
        super().__init__(variant='', padding='', tight=True) # Reset base options
        
        # Override classes completely in favor of s-thumbnail
        # Size and aspect ratio must be enforced via style still as they are instance specific
        self.classes(remove='s-card rounded-app border w-full border-app glass shadow-md bg-app-surface shadow-none vibrant-shadow') # Clear potential AppCard defaults
        self.classes('s-thumbnail group') 
        self.style(f'width: {size}; height: {size}; aspect-ratio: 1/1;')

        with self:
            if type == 'image':
                # content = image URL or base64
                ui.image(content).classes('s-thumbnail__image')
            
            elif type == 'text':
                # content = string
                with ui.column().classes('s-thumbnail__content'):
                    ui.label(content).classes('s-thumbnail__text')
                    # Bottom-to-top fade to imply truncation
                    ui.element('div').classes('s-thumbnail__fade-overlay')

            elif type == 'html':
                # content = html string
                with ui.column().classes('s-thumbnail__content bg-[var(--c-surface-1)]'):
                    # We use a container that scales down the HTML to look like a document preview
                    with ui.element('div').classes('s-thumbnail__preview-scale'):
                        ui.html(content, sanitize=False).classes('text-[10px] prose prose-invert')
                    
            elif type == 'tree':
                # content = list of items
                items = content if isinstance(content, list) else ['src/', 'docs/', 'main.py', 'config.yaml']
                with ui.column().classes('s-thumbnail__content gap-1.5'):
                    # Root Folder (Static Open)
                    with ui.row().classes('items-center gap-2 mb-1'):
                        ui.icon('folder_open', size='18px', color='var(--c-primary)')
                        ui.label('Root').classes('text-[11px] font-bold tracking-tight')
                    
                    # Children
                    for item in items[:6]: # Limit to prevent overflow
                        with ui.row().classes('items-center gap-2 pl-4'):
                            is_dir = item.endswith('/')
                            icon = 'folder' if is_dir else 'insert_drive_file'
                            ui.icon(icon, size='14px').classes('s-thumbnail__tree-icon')
                            ui.label(item).classes('text-[10px] opacity-70')

            # Subtle Interactive Overlay
            with ui.column().classes('s-thumbnail__overlay'):
                ui.icon('visibility', size='28px').classes('drop-shadow-lg text-[var(--c-text-main)]')
