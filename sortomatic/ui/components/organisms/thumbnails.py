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
        super().__init__(variant='subtle', padding='p-0', tight=True)
        
        # Enforce square aspect ratio and hide overflows to prevent scrollbars
        self.style(f'width: {size}; height: {size}; aspect-ratio: 1/1; overflow: hidden;')
        self.classes('relative group cursor-pointer border-white/5 bg-white/5 hover:border-white/20 transition-all')

        with self:
            if type == 'image':
                # content = image URL or base64
                ui.image(content).classes('w-full h-full object-cover transition-transform group-hover:scale-110 duration-500')
            
            elif type == 'text':
                # content = string
                with ui.column().classes('w-full h-full p-3 font-mono bg-black/10'):
                    ui.label(content).classes('text-[8px] leading-[1.2] opacity-60 break-all whitespace-pre-wrap')
                    # Bottom-to-top fade to imply truncation
                    ui.element('div').classes('absolute bottom-0 left-0 w-full h-1/3').style('background: linear-gradient(to top, rgba(0,0,0,0.5), transparent);')

            elif type == 'html':
                # content = html string
                with ui.column().classes('w-full h-full p-4 bg-white/[0.03]'):
                    # We use a container that scales down the HTML to look like a document preview
                    with ui.element('div').style('transform: scale(0.6); transform-origin: top left; width: 166%;'):
                        ui.html(content, sanitize=False).classes('text-[10px] prose prose-invert')
                    
            elif type == 'tree':
                # content = list of items
                items = content if isinstance(content, list) else ['src/', 'docs/', 'main.py', 'config.yaml']
                with ui.column().classes('w-full h-full p-4 gap-1.5 bg-black/5'):
                    # Root Folder (Static Open)
                    with ui.row().classes('items-center gap-2 mb-1'):
                        ui.icon('folder_open', size='18px', color='var(--q-primary)')
                        ui.label('Root').classes('text-[11px] font-bold tracking-tight')
                    
                    # Children
                    for item in items[:6]: # Limit to prevent overflow
                        with ui.row().classes('items-center gap-2 pl-4'):
                            is_dir = item.endswith('/')
                            icon = 'folder' if is_dir else 'insert_drive_file'
                            ui.icon(icon, size='14px').classes('opacity-30')
                            ui.label(item).classes('text-[10px] opacity-70')

            # Subtle Interactive Overlay
            with ui.column().classes('absolute inset-0 bg-primary/10 opacity-0 group-hover:opacity-100 transition-opacity items-center justify-center'):
                ui.icon('visibility', size='28px', color='white').classes('drop-shadow-lg')
