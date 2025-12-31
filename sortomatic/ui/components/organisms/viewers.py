from nicegui import ui
from sortomatic.ui.style import theme
from sortomatic.ui.components import atoms
from typing import Dict

def thumbnail_viewer(file_type: str, file_path: str, extra_data: Dict = {}) -> ui.card:
    """
    Thumbnail Viewer: Smart media preview.
    """
    with atoms.card().classes('w-full aspect-video flex items-center justify-center relative overflow-hidden group p-0') as container:
        
        ft = file_type.lower()
        
        # Image
        if ft == 'image':
            ui.image(file_path).classes('w-full h-full object-cover transition-transform duration-700 group-hover:scale-105')
            
        # Audio (Album Art)
        elif ft == 'audio':
            # Background blur
            ui.image(extra_data.get('album_art', 'https://placehold.co/400')).classes('absolute w-full h-full object-cover opacity-30 blur-md')
            # Foregroung
            ui.image(extra_data.get('album_art', 'https://placehold.co/400')).classes('w-32 h-32 rounded-lg shadow-2xl z-10')
            
            # Waveform visualization (fake for now)
            with ui.element('div').classes('absolute bottom-4 left-0 w-full flex items-end justify-center gap-1 h-8 opacity-50'):
                for i in range(10):
                    ui.element('div').classes('w-1 bg-white rounded-t animate-bounce').style(f'height: {20 + (i%3)*10}%; animation-delay: {i*0.1}s')

        # Video
        elif ft == 'video':
            # Display frame or video element muted
            ui.video(file_path).props('muted loop autoplay').classes('w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity')
            ui.icon('play_circle_outline').classes('absolute text-6xl opacity-50 group-hover:opacity-100 transition-opacity z-10')

        # Archive (Zip/Rar) -> Mini Tree
        elif ft in ['archive', 'zip', 'rar']:
            with ui.column().classes('w-full h-full bg-black/20 p-4 gap-1 overflow-hidden'):
                ui.label('Archive Contents').classes('text-xs font-bold uppercase opacity-50 mb-2')
                # Fake items
                for f in ['setup.exe', 'readme.txt', 'data.bin']:
                    with ui.row().classes('items-center gap-2 opacity-70'):
                        ui.icon('insert_drive_file').classes('text-xs')
                        ui.label(f).classes('text-xs font-mono')

        # Default
        else:
            ui.icon('insert_drive_file').classes(f'text-6xl text-[{theme.TEXT_MUTED}] opacity-20')
            ui.label(ft.upper()).classes('absolute bottom-4 text-xs font-bold opacity-30 tracking-widest')
            
    return container
