from nicegui import ui
from typing import List, Optional
from ..atoms.cards import AppCard

class AppTerminal(AppCard):
    """
    A premium monospaced log terminal with sticky auto-scroll behavior.
    Supports colored logs and high-contrast backgrounds.
    """
    def __init__(self, height: str = '300px', title: str = "System Logs"):
        # Terminal uses a very subtle, dark variant
        super().__init__(variant='subtle', padding='p-0', tight=True)
        self.classes('overflow-hidden border border-black/40 bg-black/40 shadow-inner')
        
        with self:
            # Header
            with ui.row().classes('w-full items-center justify-between px-4 py-1.5 bg-black/20 border-b border-white/5'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('terminal', size='14px').classes('opacity-50')
                    ui.label(title).classes('text-[10px] font-bold uppercase tracking-widest opacity-50')
                
                with ui.row().classes('gap-1'):
                    # Decorative dots
                    ui.element('div').classes('w-2 h-2 rounded-full bg-red-500/30')
                    ui.element('div').classes('w-2 h-2 rounded-full bg-yellow-500/30')
                    ui.element('div').classes('w-2 h-2 rounded-full bg-green-500/30')

            # Scroll Area
            self.scroll = ui.scroll_area().classes(f'w-full h-[{height}] bg-transparent')
            with self.scroll:
                self.content = ui.html('', sanitize=False).classes('p-4 font-mono text-[12px] leading-relaxed whitespace-pre-wrap break-all')
                self.content.style('color: #d1d1d1;') # Default light grey for logs
        
        # Internal state for stickiness
        self._is_sticky = True
        self._log_buffer: List[str] = []
        
        # JS to track scroll position and update stickiness
        # If user scrolls up, we disable auto-scroll. If they scroll to bottom, we re-enable.
        self.scroll.on('scroll', self._handle_scroll)

    def _handle_scroll(self, e):
        # e.vertical_percentage is 1.0 when at the bottom
        if e.vertical_percentage >= 0.99:
            self._is_sticky = True
        else:
            self._is_sticky = False

    def log(self, message: str, color: Optional[str] = None):
        """
        Append a message to the terminal.
        Supports HTML tags or a specific color argument.
        """
        timestamp = ui.label('').style('display:none') # Hidden placeholder for trigger
        
        styled_msg = message
        if color:
            styled_msg = f'<span style="color: {color};">{message}</span>'
        
        # Add to buffer and update HTML
        self._log_buffer.append(styled_msg)
        if len(self._log_buffer) > 500: # Limit history
            self._log_buffer.pop(0)
            
        self.content.set_content("<br>".join(self._log_buffer))
        
        # Auto-scroll if sticky
        if self._is_sticky:
            # We use a slight delay to ensure content is rendered
            ui.timer(0.05, lambda: self.scroll.scroll_to(percent=1.0), once=True)

    def clear_logs(self):
        self._log_buffer = []
        self.content.set_content("")
