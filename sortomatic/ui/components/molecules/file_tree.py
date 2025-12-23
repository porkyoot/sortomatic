from nicegui import ui
from typing import List, Dict, Optional, Callable
import os
from ...theme import ColorPalette, CategoryStyles
from ..atoms.badges import CategoryBadge, AppBadge
from ..atoms.icons import AppIcon
from ....utils.formatters import format_size, format_date_human
from ....core.bridge import bridge
from ....core.types import ScanContext

class FileTreeRow(ui.row):
    """
    A single row in the file tree with aligned columns.
    """
    def __init__(self, 
                 name: str, 
                 level: int, 
                 is_dir: bool, 
                 palette: ColorPalette,
                 file_data: Optional[ScanContext] = None,
                 show_category: bool = True,
                 show_size: bool = True,
                 show_date: bool = True,
                 expanded: bool = False,
                 toggle_func: Optional[Callable] = None):
        super().__init__()
        self.classes('w-full items-center py-1 px-4 hover:bg-white/5 transition-colors no-wrap shrink-0')
        self.style('min-width: 800px;') # Ensure columns don't squash
        
        with self:
            # 1. Name Column (Tree Column)
            indent = level * 24
            with ui.row().classes('items-center no-wrap').style(f'width: 40%; padding-left: {indent}px;'):
                if is_dir:
                    icon = "expand_more" if expanded else "chevron_right"
                    ui.button(icon=icon, on_click=toggle_func).props('flat dense size=sm').classes('mr-1 color-[var(--app-text-sec)]')
                    ui.icon("folder", color="var(--q-primary)").classes('mr-2')
                else:
                    ui.element('div').classes('w-8') # Placeholder for chevron
                    category = file_data.category if file_data else "Other"
                    ui.icon(CategoryStyles.get_icon(category), color=CategoryStyles.get_color(category, palette)).classes('mr-2')
                
                ui.label(name).classes('text-sm font-medium truncate')

            # 2. Category Column
            with ui.element('div').style('width: 15%;'):
                if show_category and not is_dir and file_data:
                    category = file_data.category or "Other"
                    CategoryBadge(category, palette, variant="glass")

            # 3. Size Column
            with ui.element('div').style('width: 20%;'):
                if show_size and not is_dir and file_data:
                    val, unit, color = format_size(file_data.size_bytes)
                    AppBadge(label=unit, value=val, color=color, variant="glass", icon="storage")

            # 4. Date Column
            with ui.element('div').style('width: 25%;'):
                if show_date and not is_dir and file_data:
                    date_str, color = format_date_human(file_data.modified_at)
                    AppBadge(label="", value=date_str, color=color, variant="glass", icon="calendar_month")

class FileTree(ui.column):
    """
    Powerful, lazy-loading file tree with sorting and configurable columns.
    """
    def __init__(self, 
                 root_path: str, 
                 palette: ColorPalette,
                 show_category: bool = True,
                 show_size: bool = True,
                 show_date: bool = True):
        super().__init__()
        self.classes('w-full border border-white/10 rounded-app overflow-hidden bg-white/5')
        self.root_path = root_path
        self.palette = palette
        self.show_category = show_category
        self.show_size = show_size
        self.show_date = show_date
        
        self.sort_by = "name"
        self.sort_desc = False
        self.filter_text: str = ""
        
        # State management for expansion
        self.expanded_paths = set()
        
        self.render()

    def set_filter(self, text: str):
        """Hook for external search components."""
        self.filter_text = text
        self.render()

    def sort_tree(self, field: str):
        if self.sort_by == field:
            self.sort_desc = not self.sort_desc
        else:
            self.sort_by = field
            self.sort_desc = False
        self.render()

    def render(self):
        self.clear()
        with self:
            # 1. Header
            with ui.row().classes('w-full items-center bg-white/10 py-2 px-4 no-wrap shrink-0 border-b border-white/5'):
                self._header_cell("Name", "name", "40%")
                self._header_cell("Category", "category", "15%")
                self._header_cell("Size", "size", "20%")
                self._header_cell("Modified", "date", "25%")
            
            # 2. Tree Container (Scroll Area)
            with ui.scroll_area().classes('w-full h-[600px]'):
                self.content_col = ui.column().classes('w-full gap-0')
                ui.timer(0.1, lambda: self._render_level(self.root_path, 0), once=True)

    def _header_cell(self, label: str, field: str, width: str):
        with ui.element('div').style(f'width: {width};').classes('cursor-pointer hover:text-white transition-colors group'):
            with ui.row().classes('items-center gap-1'):
                ui.label(label).classes('text-[10px] uppercase font-bold tracking-widest opacity-50')
                if self.sort_by == field:
                    icon = "arrow_upward" if not self.sort_desc else "arrow_downward"
                    ui.icon(icon, size='12px').classes('color-[var(--q-primary)]')
            ui.on('click', lambda: self.sort_tree(field))

    async def _render_level(self, path: str, level: int):
        response = await bridge.request("get_file_tree", {"path": path, "search": self.filter_text})
        if not response:
            return
            
        folders = response["folders"]
        # Convert dicts back to ScanContext for dot access in UI
        files = [ScanContext(**f) for f in response["files"]]
        
        # Apply sorting
        if self.sort_by == "name":
            folders.sort(reverse=self.sort_desc)
            files.sort(key=lambda f: f.filename, reverse=self.sort_desc)
        elif self.sort_by == "size":
            files.sort(key=lambda f: f.size_bytes, reverse=self.sort_desc)
        elif self.sort_by == "date":
            files.sort(key=lambda f: f.modified_at, reverse=self.sort_desc)
        elif self.sort_by == "category":
            files.sort(key=lambda f: f.category or "", reverse=self.sort_desc)

        with self.content_col:
            # Render Folders
            for folder in folders:
                folder_path = os.path.join(path, folder)
                is_expanded = folder_path in self.expanded_paths
                
                FileTreeRow(
                    name=folder, 
                    level=level, 
                    is_dir=True, 
                    palette=self.palette,
                    expanded=is_expanded,
                    toggle_func=lambda p=folder_path: self._toggle_expansion(p)
                )
                
                if is_expanded:
                    await self._render_level(folder_path, level + 1)
            
            # Render Files
            for fileinfo in files:
                FileTreeRow(
                    name=fileinfo.filename,
                    level=level,
                    is_dir=False,
                    palette=self.palette,
                    file_data=fileinfo,
                    show_category=self.show_category,
                    show_size=self.show_size,
                    show_date=self.show_date
                )

    def _toggle_expansion(self, path: str):
        if path in self.expanded_paths:
            self.expanded_paths.remove(path)
        else:
            self.expanded_paths.add(path)
        self.render()
