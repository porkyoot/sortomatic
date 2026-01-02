from nicegui import app, ui
from sortomatic.ui.style import theme
from sortomatic.ui.components import atoms, molecules, organisms
import random 

# Serve static files for themes
app.add_static_files('/themes', 'sortomatic/themes')

@ui.page('/')
def main_page():
    theme.load_theme()
    
    # Fake Data Sources
    def get_sparkline_data():
        return [random.randint(10, 100) for _ in range(20)]
    
    files_data = [
        {'id': '1', 'name': 'Documents', 'category': 'other', 'size_str': '-', 'size_bytes': 0, 'date': '2023-10-27', 'children': [
            {'id': '2', 'name': 'Resume.pdf', 'category': 'document', 'size_str': '1.2 MB', 'size_bytes': 1200000, 'date': '2023-10-26'},
            {'id': '3', 'name': 'Budget.xlsx', 'category': 'document', 'size_str': '45 KB', 'size_bytes': 45000, 'date': '2023-10-25'},
        ]},
        {'id': '4', 'name': 'Images', 'category': 'other', 'size_str': '-', 'size_bytes': 0, 'date': '2023-10-27', 'children': [
            {'id': '5', 'name': 'Vacation.jpg', 'category': 'image', 'size_str': '3.4 MB', 'size_bytes': 3400000, 'date': '2023-09-01', 'thumbnail': 'https://picsum.photos/id/15/48/48'},
            {'id': '6', 'name': 'Logo.png', 'category': 'image', 'size_str': '500 KB', 'size_bytes': 500000, 'date': '2023-01-15', 'thumbnail': 'https://picsum.photos/id/20/48/48'},
        ]},
        {'id': '7', 'name': 'Music.mp3', 'category': 'audio', 'size_str': '5.6 MB', 'size_bytes': 5600000, 'date': '2023-10-20'},
    ]

    # --- Layout ---
    
    with ui.column().classes('w-full h-screen gap-0 bg-bg text-main').style('overflow: hidden'):
        
        # 1. Status Bar
        organisms.status_bar(lambda: [float(x) for x in get_sparkline_data()])
        
        with ui.row().classes('w-full flex-1 p-4 gap-4 overflow-hidden'):
            
            # Left Column (Explorer) - 60%
            with ui.column().classes('flex-[3] h-full gap-4'):
                
                # Scan Card
                organisms.scan_card(
                    on_play=lambda: ui.notify('Play'),
                    on_pause=lambda: ui.notify('Pause'),
                    on_restart=lambda: ui.notify('Restart'),
                    on_ff=lambda: ui.notify('Fast Forward Toggled'),
                    progress=0.45,
                    eta="1h 20m",
                    current_path="/home/user/downloads/very_large_collection_of_iso_files/linux_distro.iso",
                    speed="45 MB/s",
                    error="Sample Error",
                    scan_state='running'
                )
                
                # File Tree
                with atoms.card().classes('w-full flex-1 p-0 overflow-hidden flex flex-col'):
                    molecules.header_card('File Explorer')
                    molecules.file_tree(files_data)
            
            # Right Column (Preview & Atoms Showcase) - 40%
            with ui.column().classes('flex-[2] h-full gap-4 overflow-y-auto'):
                 
                 # Thumbnail Showcase
                 with ui.column().classes('w-full gap-2'):
                     ui.label('Smart Previews').classes('text-xs uppercase font-bold opacity-50')
                     with ui.element('div').classes('w-full grid gap-2').style('grid-template-columns: repeat(auto-fit, minmax(140px, 1fr))'):
                         # 1. Image
                         organisms.thumbnail_viewer('image', 'https://picsum.photos/400/300?random=1')
                         
                         # 2. Audio
                         organisms.thumbnail_viewer('audio', '', {'album_art': 'https://picsum.photos/200?random=2'})
                         
                         # 3. Video (Mock)
                         organisms.thumbnail_viewer('video', '') 
                         
                         # 4. Archive
                         archive_files = [{'id': 'root', 'label': 'Project_Backup', 'children': [
                             {'id': 'src', 'label': 'src', 'children': [{'id': 'main', 'label': 'main.py'}]},
                             {'id': 'readme', 'label': 'README.md'}
                         ]}]
                         organisms.thumbnail_viewer('archive', 'backup.zip', {'files': archive_files})
                         
                         # 5. Unknown / Default
                         organisms.thumbnail_viewer('unknown_type', 'unknown_file.xyz')
                 
                 # Atoms Showcase Card
                 with atoms.card().classes('w-full gap-4'):
                     ui.label('Atoms Showcase').classes('text-xl font-bold')
                     atoms.separator().classes('w-full h-px my-2')
                     
                     with ui.row().classes('items-center gap-2'):
                         atoms.button('Primary', color='primary')
                         atoms.button('Secondary', color='secondary')
                         atoms.button('Ghost', variant='ghost')
                    
                         with ui.row().classes('items-center gap-2'):
                          atoms.button('Pill', shape='pill', color='primary')
                          atoms.button(icon='add', shape='circle', color='secondary')
                          atoms.button('First', shape='chevron-first')
                          atoms.button('Middle', shape='chevron')
                          atoms.button('Last', shape='chevron-last')
                         
                     with ui.row().classes('w-full items-center gap-4'):
                         ui.label('Nuclear:').classes('text-xs font-bold')
                         atoms.nuclear_button(lambda: ui.notify('BOOM! Database Dropped!'))
                         
                     with ui.column().classes('w-full gap-2 mt-4'):
                         ui.label('Logarithmic Slider').classes('text-xs font-bold')
                         atoms.logarithmic_slider(1, 1000, 100, lambda x: ui.notify(f'Val: {x:.2f}'))
                         
                     with ui.column().classes('w-full gap-2 mt-2'):
                         atoms.search_bar()
                         atoms.date_picker()

def start_app(port: int = 8080, theme_name: str = 'default', dark_mode: bool = True, base_path: str | None = None):
    # Note: theme_name and dark_mode args can be used to tweak style.py or app.css injection ideally.
    # For now, we stick to the premium theme but we honor the port.
    ui.run(title='Sortomatic Premium', port=port, reload=False, dark=dark_mode)

if __name__ in {"__main__", "__mp_main__"}:
    start_app()
