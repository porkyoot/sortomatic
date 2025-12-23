from nicegui import ui
from .theme import apply_theme
from .themes.solarized import SOLARIZED_DARK, SOLARIZED_LIGHT

def start_app(port: int, theme: str, dark: bool, path: str = None):
    """Entry point for the NiceGUI application."""
    print(f"DEBUG: Starting app on port {port} with path {path}")
    
    # Select Palette
    if theme == "solarized":
        palette = SOLARIZED_DARK if dark else SOLARIZED_LIGHT
    else:
        # Fallback or other themes
        palette = SOLARIZED_DARK if dark else SOLARIZED_LIGHT

    @ui.page('/')
    def main_page():
        apply_theme(palette)
        
        with ui.header().classes('bg-[var(--q-primary)] text-white p-4'):
            ui.label('Sortomatic').classes('text-2xl font-bold')
            
        with ui.column().classes('w-full items-center p-8 gap-6'):
            ui.label(f'Sortomatic Web Interface').classes('text-3xl font-black italic tracking-tighter color-[var(--q-primary)]')
            
            with ui.row().classes('gap-4'):
                from .components.atoms.badges import AppBadge
                from .components.atoms.buttons import AppButton
                
                AppBadge(label="Status", value="Ready", color="var(--q-success)")
                AppBadge(label="Directory", value=path or "Not Set", color="var(--q-primary)")

            with ui.card().classes('p-8 rounded-app shadow-xl border border-opacity-10 w-full max-w-lg'):
                ui.label("Hello World!").classes('text-2xl font-bold mb-4')
                ui.label("The GUI components are now initialized and themed.").classes('opacity-70 mb-6')
                
                AppButton(
                    "Launch Scan", 
                    icon="rocket_launch", 
                    variant="primary", 
                    shape="pill",
                    on_click=lambda: ui.notify("Scan triggered!", color="var(--q-primary)")
                )

    ui.run(host='0.0.0.0', port=port, title="Sortomatic", dark=dark, reload=False)
