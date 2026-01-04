from nicegui import ui
from sortomatic.ui.style import theme
from sortomatic.ui.components import atoms
from typing import List, Dict, Callable, Optional, Any, Set
from dataclasses import dataclass

@dataclass
class FileNode:
    id: str
    name: str
    category: str
    size: str 
    size_bytes: int
    date: str
    thumbnail: Optional[str] = None
    children: Optional[List['FileNode']] = None
    
    @property
    def is_folder(self):
        return self.children is not None

def file_tree(data: List[Dict]) -> ui.element:
    """
    Refactored File Tree Molecule.
    Mirrors the logic of the old FileSystemExplorerPanel but uses new atoms.
    """
    
    # --- Data Parsing ---
    def parse_nodes(nodes_data):
        res = []
        for d in nodes_data:
            node = FileNode(
                id=d.get('id', d.get('name')),
                name=d['name'],
                category=d.get('category', 'other'),
                size=d.get('size_str', ''),
                size_bytes=d.get('size_bytes', 0),
                date=d['date'],
                thumbnail=d.get('thumbnail'),
                children=parse_nodes(d['children']) if 'children' in d else None
            )
            res.append(node)
        return res

    all_nodes = parse_nodes(data)
    
    # --- State ---
    state = {
        'search_query': '',
        'selected_categories': set(),
        'min_size': 0,
        'max_size': 100 * 1024 * 1024 * 1024, # 100 GB
        'date_range': None
    }
    
    # --- Logic ---
    def get_filtered_nodes(nodes):
        res = []
        for node in nodes:
            # Recursively filter children first to include folders containing matching items
            visible_children = []
            if node.is_folder and node.children:
                visible_children = get_filtered_nodes(node.children)
            
            # Match current node
            match = True
            
            # 1. Search
            if state['search_query'] and state['search_query'].lower() not in node.name.lower():
                match = False
                
            # 2. Categories
            if match and state['selected_categories']:
                # Simple string matching since we don't have the Enum
                # Logic: if ANY selected category matches the node's category
                if node.category not in state['selected_categories']:
                     match = False
            
            # 3. Size (only for files)
            if match and not node.is_folder:
                if not (state['min_size'] <= node.size_bytes <= state['max_size']):
                    match = False
            
            # 4. Date (TODO: Implement robust date parsing/comparison if needed, strict string check for now)
            # if match and state['date_range']: ...

            # Include if matches OR has matching children
            if match or visible_children:
                d = {
                    'id': node.id,
                    'label': node.name,
                    'icon': 'folder' if node.is_folder else 'insert_drive_file',
                }
                if node.is_folder:
                    d['children'] = visible_children
                res.append(d)
        return res

    # --- UI ---
    container = ui.column().classes('w-full flex-1 gap-0 border rounded-lg overflow-hidden bg-surface')
    
    with container:
        # Header
        with ui.row().classes('w-full items-center justify-between py-2 px-3 gap-2 border-b bg-surface-half'):
             # Left: Icon + Title
            with ui.row().classes('items-center gap-2 flex-shrink-0'):
                ui.icon('folder_open', size='sm').classes('text-primary')
                ui.label('File System').classes('text-sm font-bold')

            # Right: Controls
            with ui.row().classes('items-center gap-2 flex-shrink-0'):
                # Search
                atoms.search_bar(on_change=lambda e: update_search(e.value))
                
                # Filter Menu
                with atoms.button(icon='filter_list', variant='ghost').props('size=sm') as btn:
                    ui.tooltip('Filters')
                    with ui.menu().props('anchor="bottom right" self="top right"').classes('bg-surface p-4 shadow-xl border w-72'):
                        with ui.column().classes('gap-4'):
                            with ui.row().classes('w-full justify-between items-center'):
                                ui.label('Filters').classes('font-bold')
                                atoms.button(icon='restart_alt', variant='ghost', on_click=lambda: clear_filters()).props('size=sm')
                            
                            # Categories
                            ui.label('Categories').classes('text-xs opacity-70')
                            categories = ['document', 'image', 'audio', 'video', 'archive', 'code', 'other']
                            
                            @ui.refreshable
                            def refresh_filters():
                                with ui.row().classes('gap-1 flex-wrap'):
                                    for cat in categories:
                                        is_sel = cat in state['selected_categories']
                                        def toggle_cat(e, _cat=cat):
                                            if _cat in state['selected_categories']:
                                                state['selected_categories'].remove(_cat)
                                            else:
                                                state['selected_categories'].add(_cat)
                                            refresh_tree.refresh()
                                            refresh_filters.refresh()

                                        ui.chip(cat, color='primary' if is_sel else 'grey-8', 
                                                on_click=toggle_cat).props('clickable dense square size=sm')
                            refresh_filters()

                            # Size
                            ui.label('Size Range').classes('text-xs opacity-70')
                            atoms.file_size_slider(
                                min_bytes=state['min_size'], 
                                max_bytes=state['max_size'],
                                on_change=lambda e: update_size(e)
                            )

                            # Date
                            ui.label('Date Modified').classes('text-xs opacity-70')
                            atoms.date_picker(on_change=lambda e: update_date(e))

    
        # Tree Body
        tree_container = ui.column().classes('w-full flex-1 relative')
        with tree_container:
            @ui.refreshable
            def refresh_tree():
                filtered_data = get_filtered_nodes(all_nodes)
                if not filtered_data:
                    with ui.column().classes('w-full h-full items-center justify-center opacity-50'):
                        ui.icon('search_off', size='xl')
                        ui.label('No files match current filters')
                else:
                    atoms.simple_file_tree(filtered_data, on_select=lambda e: ui.notify(f"Selected: {e.value}"))
            
            refresh_tree()
            
        # --- Logic Helpers ---
        def update_search(val):
            state['search_query'] = val
            refresh_tree.refresh()

        def update_size(val):
            state['min_size'] = val['min']
            state['max_size'] = val['max']
            refresh_tree.refresh()
            
        def update_date(val):
            state['date_range'] = val
            # Date logic implementation pending
            refresh_tree.refresh()

        def clear_filters():
            state['search_query'] = ''
            state['selected_categories'] = set()
            state['min_size'] = 0
            state['max_size'] = 100 * 1024 * 1024 * 1024
            state['date_range'] = None
            refresh_tree.refresh()
            # Note: We can't easily reset the internal state of atoms components (slider, search bar) 
            # without binding which complicates this specific "simple" refactor.
            # Ideally atoms should expose bindable props.
            
    return container
