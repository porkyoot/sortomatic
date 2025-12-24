from nicegui import ui
from typing import List, Dict, Optional, Callable
from ...theme import Theme


class StatusBar(ui.header):
    """
    A premium status bar for the top of the application.
    Provides system metrics, connectivity status, and global settings.
    """
    def __init__(self, theme: Theme, on_theme_change: Optional[Callable] = None):
        super().__init__()
        # Glassmorphism header
        self.classes('s-status-bar')
        self.theme = theme
        self.on_theme_change = on_theme_change
        
        # Internal State
        self.backend_state = "ready"
        self.db_state = "ready"
        self.scan_state = "idle"
        self.cpu_history = [0.0] * 10
        self.gpu_history = [0.0] * 10
        self.ram_history = [0.0] * 10
        self.disk_history = [0.0] * 10
        
        # Icon definitions
        self.WEB_ICONS = {
            'ready': 'mdi-cloud-check',
            'error': 'mdi-cloud-alert',
            'pending': 'mdi-cloud-sync',
            'default': 'mdi-cloud'
        }
        self.DB_ICONS = {
            'ready': 'mdi-database-check',
            'error': 'mdi-database-alert',
            'pending': 'mdi-database-sync',
            'default': 'mdi-database'
        }
        self.SCAN_ICONS = {
            'ready': 'mdi-progress-check',
            'error': 'mdi-progress-alert',
            'pending': 'mdi-progress-helper',
            'default': 'mdi-progress-clock'
        }

        with self:
            # 1. Left Section: Logo / App Name
            with ui.row().classes('items-center gap-2'):
                ui.label('Sortomatic').classes('s-text-h1 text-sm tracking-widest').tag = 'h1'

            # 2. Middle Section: Connectivity & Status (Unified with Metrics)
            self.status_container = ui.row().classes('absolute-center')
            self._init_pill()

            # 3. Right Section: Global Controls
            with ui.row().classes('items-center gap-4'):
                from .theme_selectors import ThemeSelector
                ThemeSelector(is_dark=True, on_change=self.on_theme_change)

    def _init_pill(self):
        """Initialize the unified status pill components once."""
        from ..atoms.badges import StatusBadge
        from ..atoms.special.histograms import AppHistogram
        
        with self.status_container:
            with ui.row().classes('s-status-badge-row'):
                # -- Status Badges --
                self.web_badge_container = ui.row()
                ui.element('div').classes('s-separator-vertical')
                self.scan_badge_container = ui.row()
                ui.element('div').classes('s-separator-vertical')
                self.db_badge_container = ui.row()
                
                ui.element('div').classes('s-separator-vertical')
                
                # -- Histograms --
                self.cpu_hist = AppHistogram([0]*6, label='CPU', color='var(--c-primary)', icon='mdi-cpu-64-bit', transparent=True, height='16px', bar_width='2px', max_bars=6)
                ui.element('div').classes('s-separator-vertical')
                self.gpu_hist = AppHistogram([0]*6, label='GPU', color='var(--c-success)', icon='mdi-expansion-card-variant', transparent=True, height='16px', bar_width='2px', max_bars=6)
                ui.element('div').classes('s-separator-vertical')
                self.ram_hist = AppHistogram([0]*6, label='RAM', color='var(--c-warning)', icon='mdi-memory', transparent=True, height='16px', bar_width='2px', max_bars=6)
                ui.element('div').classes('s-separator-vertical')
                self.disk_hist = AppHistogram([0]*6, label='Disk', color='var(--c-error)', icon='mdi-harddisk', transparent=True, height='16px', bar_width='2px', max_bars=6)


        self._update_badges()

    def _update_badges(self):
        """Update only the status badge contents with descriptive tooltips."""
        from ..atoms.badges import StatusBadge
        
        # Web
        self.web_badge_container.clear()
        with self.web_badge_container:
            web_tooltip = f"Backend Connection: {self.backend_state.capitalize()}"
            StatusBadge('Web', self.backend_state, self.theme, icon=self.WEB_ICONS, variant='simple', interactive=False, tooltip=web_tooltip)
            
        # Scan
        self.scan_badge_container.clear()
        with self.scan_badge_container:
            scan_tooltip = f"System Scan: {self.scan_state.capitalize()}"
            StatusBadge('Scan', self.scan_state, self.theme, icon=self.SCAN_ICONS, rotate=self.scan_state == 'pending', variant='simple', interactive=False, tooltip=scan_tooltip)
            
        # DB
        self.db_badge_container.clear()
        with self.db_badge_container:
            db_tooltip = f"Database Status: {self.db_state.capitalize()}"
            StatusBadge('DB', self.db_state, self.theme, icon=self.DB_ICONS, variant='simple', interactive=False, tooltip=db_tooltip)

    def refresh_status(self, backend_state: str, db_state: str, scan_state: str):
        """Update system status badges."""
        if (backend_state, db_state, scan_state) == (self.backend_state, self.db_state, self.scan_state):
            return # No change
            
        self.backend_state = backend_state
        self.db_state = db_state
        self.scan_state = scan_state
        self._update_badges()

    def update_metrics(self, 
                       cpu_history: List[float], 
                       gpu_history: List[float],
                       ram_history: List[float],
                       disk_history: List[float]):
        """Update histogram data without re-creating elements."""
        self.cpu_hist.update_data(cpu_history)
        self.gpu_hist.update_data(gpu_history)
        self.ram_hist.update_data(ram_history)
        self.disk_hist.update_data(disk_history)
