from nicegui import ui
from pathlib import Path
from nicetheme import nt

def start_app(port: int, theme: str, dark: bool, path: str = None):
    """Entry point for the NiceGUI application."""
    print(f"DEBUG: Starting app on port {port} with path {path}")
    
    # Initialize NiceTheme with local themes directory
    local_themes = Path(__file__).parent / 'themes'
    manager = nt.initialize(themes_dirs=[local_themes])
    
    # Set initial theme (fallback to sortomatic if 'solarized' requested for legacy reasons)
    initial_theme = 'sortomatic' if theme == 'solarized' else theme
    manager.select_theme(initial_theme)
    # Note: Dark mode is handled by NiceTheme via auto-detection or persistence, 
    # but we can force it if provided by CLI args
    # manager.set_mode('dark' if dark else 'light') 

    # Initialize Backend Bridge
    from sortomatic.core.bridge import bridge
    from sortomatic.core.service import init_bridge_handlers
    init_bridge_handlers()

    @ui.page('/')
    def main_page():
        # NiceTheme automatically injects styles via bridge/manager, 
        # but we ensure the manager is bound to this client context if needed
        # Actually, nt.initialize creates a global manager/bridge which uses ui.add_head_html
        # which works for the current page context.
        
        # Now get client for event handlers
        client = ui.context.client
        client.theme_name = initial_theme

        def handle_theme_change(theme_info):
            if not client.has_socket_connection:
                return
            # NiceTheme handles global updates, but if we have specific logic:
            pass

        bridge.on("theme_changed", handle_theme_change)
        
        # Cleanup bridge listener on disconnect
        client.on_disconnect(lambda: bridge.off("theme_changed", handle_theme_change))
        
        # Import badge components
        # Import StatusBar
        from .components.molecules.status_bars import StatusBar
        from sortomatic.core.database import db
        
        def on_theme_toggle(t, d):
            ui.notify(f"Theme switched", color="var(--nt-primary)")
            # bridge.emit("theme_changed", {'name': t, 'is_dark': d})
            # Start using NT manager for switching? 
            # For now, just logging or notifying
            pass

        # Instantiate the new top status bar
        # Status Bar needs refactoring to not accept 'theme' object or we pass a dummy
        # For now we pass 'manager' or 'nt'? 
        # Actually we need to refactor StatusBar to not take 'theme' arg.
        # But wait, I haven't refactored StatusBar yet. 
        # I should probably pass 'None' and let it use CSS vars, 
        # BUT StatusBar signature expects 'Theme' type.
        # I modified 'theme.py' to remove 'Theme' class... 
        # So 'from .theme import Theme' import in StatusBar will fail or import nothing?
        # Ah, I modified theme.py but I didn't verify if I kept the 'Theme' class or deleted it. 
        # I REPLACED the content of theme.py with helper classes. 'Theme' class is GONE.
        # So StatusBar.py import will fail. 
        # I MUST refactor StatusBar.py concurrently or before running this.
        status_bar = StatusBar(
            on_theme_change=on_theme_toggle
        )

        # Add the WorkflowMenu
        from .components.molecules.menus import WorkflowMenu
        with status_bar:
            workflow_menu = WorkflowMenu(
                on_step_click=lambda step: ui.notify(f"Switching to {step}", color="var(--nt-primary)"),
                on_nuke=lambda: ui.notify("Database Nuked!", type='negative')
            )


        
        # Metrics history buffers
        history = {
            'cpu': [0.0] * 50,
            'gpu': [0.0] * 50,
            'ram': [0.0] * 50,
            'disk': [0.0] * 50
        }

        # Update status badges periodically
        async def update_status_badges():
            if not client.has_socket_connection:
                return
            
            try:
                # 1. Update Metrics (Real Data)
                metrics = await bridge.request("get_system_metrics")
                if metrics:
                    for key in ['cpu', 'gpu', 'ram', 'disk']:
                         val = metrics.get(key, 0.0)
                         history[key].append(val)
                         history[key] = history[key][-50:] # Keep buffer limited
                    
                    status_bar.update_metrics(
                        history['cpu'], 
                        history['gpu'], 
                        history['ram'], 
                        history['disk']
                    )
                
                # 2. Update System Status
                status = await bridge.request("get_system_status")
                if status:
                    status_bar.refresh_status(
                        backend_state=status.get("backend", "unknown"),
                        db_state=status.get("database", "unknown"),
                        scan_state=status.get("scan", "unknown")
                    )

            except Exception:
                pass
        
        ui.timer(1.0, update_status_badges)  # Check every 1 second for smooth histograms
        
        # Main content area (empty for now)
        # Main content area
        from .components.layout.smart_split import SmartSplitter
        from .components.organisms.scans import ScanCard
        from .components.organisms.terminals import AppTerminal

        # We need to track instances to update them, as SmartSplitter creates duplicates for responsiveness
        active_terminals = []
        active_scancards = []
        
        def create_scan_card():
            # Create a ScanCard and track it
            card = ScanCard(
                name="File Discovery",
                state="idle",
                progress=0.0,
                eta="--:--",
                unit="file/s",
                on_play=lambda: ui.notify("Starting scan...", type='info'),
                on_restart=lambda: ui.notify("Restarting scan...", type='warning'),
            )
            # Layout is handled by CSS grid now
            card.classes('w-full h-full') 
            active_scancards.append(card)
            
        def create_terminal():
            # Create Terminal and track it
            term = AppTerminal(
                height='100%', 
                title="System Events"
            )
            term.classes('h-full')
            active_terminals.append(term)

        # Container for the main view content
        with ui.element('div').classes('s-main-view'):
            with ui.splitter(value=40).classes('w-full h-full p-2') as splitter:
                with splitter.before:
                     create_scan_card()
                with splitter.after:
                     create_terminal()

        # 3. Bridge Listeners for Updates
        def handle_log_record(record):
            if not client.has_socket_connection:
                return
            for term in active_terminals:
                term.log(record.get('message', ''), color=record.get('color'))
                
        bridge.on("log_record", handle_log_record)
        
        # Cleanup listeners
        client.on_disconnect(lambda: bridge.off("log_record", handle_log_record))

    ui.run(host='0.0.0.0', port=port, title="Sortomatic", dark=dark, reload=False)
