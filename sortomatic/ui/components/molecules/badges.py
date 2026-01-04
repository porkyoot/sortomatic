from nicegui import ui
from sortomatic.ui.style import theme
from sortomatic.ui.components import atoms
from typing import Optional, Callable, List
import humanize

def status_badge_row(metric_sources: dict[str, Callable[[], List[float]]]) -> ui.row:
    """
    StatusBadgeRow: Connectivity badges + system metrics (CPU, RAM, GPU, Disk).
    """
    with ui.row().classes('items-center h-full gap-2 px-2') as row:
        atoms.status_badge(text='Core Connected', state='connected')
        atoms.separator()
        
        # Helper to render metric block
        def render_metric(label: str, source: Callable[[], List[float]], val_formatter: Optional[Callable[[float], str]] = None, y_max: float = 100):
            with ui.row().classes('items-center gap-1'):
                 ui.label(label).classes('text-[10px] font-bold opacity-60')
                 atoms.sparkline_histogram(source, val_formatter=val_formatter, y_max=y_max)
                 
        # CPU
        if 'cpu' in metric_sources:
            render_metric('CPU', metric_sources['cpu'])
            atoms.separator()

        # RAM
        if 'ram' in metric_sources:
            render_metric('MEM', metric_sources['ram'])
            atoms.separator()
            
        # GPU (Optional)
        if 'gpu' in metric_sources:
            render_metric('GPU', metric_sources['gpu'])
            atoms.separator()

        # Disk
        if 'disk' in metric_sources:
            # DSK IO: Map MB/s to human formatted string
            # Value is in MB/s (MiB/s really). 
            # humanize.naturalsize expects bytes.
            render_metric('DSK', metric_sources['disk'], 
                val_formatter=lambda v: f"{humanize.naturalsize(v * 1024 * 1024, binary=True)}/s", 
                y_max=100
            )
        
    return row
