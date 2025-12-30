from nicegui import app, ui
from sortomatic.ui.style import theme

# Serve static files for themes
app.add_static_files('/themes', 'sortomatic/themes')

@ui.page('/')
def main_page():
    ui.add_head_html('<link href="/themes/app.css" rel="stylesheet">')
    
    with ui.column().classes('w-full h-screen items-center justify-center').style(f'background-color: {theme.BG}'):
        with ui.card().classes(f'{theme.GLASS} p-8 items-center'):
            ui.label('Sortomatic').classes('text-4xl font-bold text-gradient')
            ui.label('Premium File Organizer').classes(f'text-lg {theme.TEXT_MUTED}')

ui.run(title='Sortomatic')
