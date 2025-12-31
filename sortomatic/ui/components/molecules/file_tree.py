from nicegui import ui
from sortomatic.ui.style import theme
from sortomatic.ui.components import atoms
from typing import List, Dict, Callable, Optional, Any
from dataclasses import dataclass

@dataclass
class FileNode:
    id: str
    name: str
    category: str
    size: str # formatted
    size_bytes: int
    date: str
    children: Optional[List['FileNode']] = None
    expanded: bool = True
    
    @property
    def is_folder(self):
        return self.children is not None

def file_tree(data: List[Dict]) -> ui.element:
    """
    Complex Molecule: Tabular File Tree.
    Hybrid between Tree and Table with aligned columns, sorting, and inline filtering.
    
    data: List of dictionaries representing the file structure.
          Expected keys: id, name, category, size_str, size_bytes, date, children (list of dicts, optional)
    """
    
    # --- State Management ---
    
    # We parse input dicts into generic objects for easier handling
    root_nodes = []
    
    def parse_nodes(nodes_data):
        res = []
        for d in nodes_data:
            node = FileNode(
                id=d.get('id', d.get('name')), # Fallback
                name=d['name'],
                category=d.get('category', 'other'),
                size=d.get('size_str', ''),
                size_bytes=d.get('size_bytes', 0),
                date=d['date'],
                children=parse_nodes(d['children']) if 'children' in d else None,
                expanded=True # Default expanded for now
            )
            res.append(node)
        return res

    all_nodes = parse_nodes(data)
    
    state = {
        'sort_col': 'name',
        'sort_asc': True,
        'filters': {
            'name': '',
            'category': '',
            'size': '',
            'date': ''
        }
    }
    
    # --- Logic ---

    def get_tree_nodes():
        """
        Parses state and returns filtered/sorted nodes for ui.tree.
        """
        def matches(node):
            f = state['filters']
            if f['name'] and f['name'].lower() not in node.name.lower(): return False
            if f['category'] and f['category'].lower() not in node.category.lower(): return False
            if f['date'] and f['date'].lower() not in node.date.lower(): return False
            return True

        def transform_recursive(nodes):
            res = []
            
            # 1. Sort neighbors
            sort_key = state['sort_col']
            try:
                nodes_sorted = sorted(nodes, key=lambda n: str(getattr(n, sort_key)).lower(), reverse=not state['sort_asc'])
            except AttributeError:
                # Fallback for size_bytes or other non-string mapping if col is 'size'
                nodes_sorted = sorted(nodes, key=lambda n: n.size_bytes if sort_key == 'size' else n.name.lower(), reverse=not state['sort_asc'])
            
            for node in nodes_sorted:
                visible_children = transform_recursive(node.children) if node.is_folder else []
                
                if matches(node) or visible_children:
                    d = {
                        'id': node.id,
                        'label': node.name,
                        'category': node.category,
                        'size': node.size,
                        'date': node.date,
                        'icon': 'folder' if node.is_folder else 'insert_drive_file',
                    }
                    if node.is_folder:
                        d['children'] = visible_children
                    res.append(d)
            return res

        return transform_recursive(all_nodes)

    # --- UI Building ---
    
    container = ui.column().classes('w-full h-full gap-0')
    grid_templ = 'minmax(200px, 3fr) minmax(100px, 1fr) minmax(100px, 1fr) minmax(120px, 1fr)'
    
    def on_sort(col):
        if state['sort_col'] == col:
            state['sort_asc'] = not state['sort_asc']
        else:
            state['sort_col'] = col
            state['sort_asc'] = True
        refresh_tree.refresh()

    def on_filter(col, val):
        state['filters'][col] = val
        refresh_tree.refresh()

    with container:
        # Header Row
        with ui.element('div').style(f'display: grid; grid-template-columns: {grid_templ}; gap: 1rem; padding-left: 2.5rem;').classes(f'w-full p-2 border-b {theme.BORDER} bg-white/5 uppercase text-xs font-bold tracking-wider {theme.TEXT_MUTED} items-center'):
            def header_cell(key, label):
                with ui.column().classes('gap-1'):
                    with ui.row().classes('items-center cursor-pointer group').on('click', lambda: on_sort(key)):
                        ui.label(label)
                        ui.icon('arrow_upward').bind_visibility_from(state, 'sort_asc').classes('text-[10px]').props('size=xs')
                        ui.icon('arrow_downward').bind_visibility_from(state, 'sort_asc', backward=lambda x: not x).classes('text-[10px]').props('size=xs')
                    ui.input(placeholder='Filter', on_change=lambda e: on_filter(key, e.value)).props('dense borderless input-class="text-xs py-0"').classes(f'bg-black/20 rounded px-1 w-full h-6')
            
            header_cell('name', 'Name')
            header_cell('category', 'Category')
            header_cell('size', 'Size')
            header_cell('date', 'Date')

        # Tree Body
        with ui.scroll_area().classes('h-full w-full'):
            @ui.refreshable
            def refresh_tree():
                nodes = get_tree_nodes()
                t = ui.tree(nodes=nodes, label_key='label').classes('w-full source-code-pro text-sm')
                t.props('dense transition-show="fade" transition-hide="fade"')
                
                t.add_slot('default-header', f'''
                    <div class="row items-center full-width q-gutter-x-md" style="display: grid; grid-template-columns: minmax(150px, 3fr) minmax(100px, 1fr) minmax(100px, 1fr) minmax(120px, 1fr); gap: 1rem; width: 100%;">
                        <div class="row items-center no-wrap overflow-hidden">
                            <q-icon :name="props.node.icon" :color="props.node.icon === 'folder' ? 'yellow-8' : 'grey-5'" class="q-mr-sm" size="18px" />
                            <div class="ellipsis">{{{{ props.node.label }}}}</div>
                        </div>
                        <div class="q-badge q-badge--outline" :style="'border-color: var(--primary); color: var(--primary); opacity: 0.8; font-size: 10px; padding: 2px 6px; text-transform: uppercase;'">
                            {{{{ props.node.category }}}}
                        </div>
                        <div class="text-mono text-caption opacity-70">{{{{ props.node.size }}}}</div>
                        <div class="text-mono text-caption opacity-50">{{{{ props.node.date }}}}</div>
                    </div>
                ''')
            
            refresh_tree()

    return container
