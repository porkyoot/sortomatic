from nicegui import app, ui
from sortomatic.ui.style import theme
from sortomatic.ui.components import organisms
from sortomatic.core.bridge import bridge
from sortomatic.core.resources import register_resource_handlers
from collections import deque

# Register backend handlers
register_resource_handlers()

# Serve static files for themes
app.add_static_files('/themes', 'sortomatic/themes')

@ui.page('/')
async def main_page():
    theme.load_theme()
    
    # Data State
    cpu_history = deque([0] * 20, maxlen=20)
    ram_history = deque([0] * 20, maxlen=20)
    gpu_history = deque([0] * 20, maxlen=20)
    disk_history = deque([0] * 20, maxlen=20)
    
    async def fetch_metrics():
        data = await bridge.request('get_resource_usage')
        if data:
            cpu_history.append(data['cpu'])
            ram_history.append(data['ram'])
            gpu_history.append(data['gpu'])
            disk_history.append(data['disk'])
            
    # Bridge Polling Timer
    ui.timer(1.0, fetch_metrics)

    # --- Layout ---
    with ui.column().classes('w-full h-screen gap-0 bg-bg text-main').style('overflow: hidden'):
        
        # 1. Status Bar
        # The sparkline components will poll these lambdas locally
        metric_sources = {
            'cpu': lambda: list(cpu_history),
            'ram': lambda: list(ram_history),
            'disk': lambda: list(disk_history),
            # Optional: Only show GPU if activity is detected or configured? 
            # For now, we always provide it, UI will render "0" flatline if unused.
            'gpu': lambda: list(gpu_history) 
        }
        organisms.status_bar(metric_sources)
        
        # 2. Tab Bar
        organisms.tab_bar()

def start_app(port: int = 8080, theme_name: str = 'default', dark_mode: bool = True, base_path: str | None = None):
    ui.run(title='Sortomatic Premium', port=port, reload=False, dark=dark_mode)

if __name__ in {"__main__", "__mp_main__"}:
    start_app()
