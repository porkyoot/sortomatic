from nicegui import ui
from typing import List, Optional
from ..atoms.cards import AppCard

class AppTerminal(AppCard):
    """
    A premium monospaced log terminal with sticky auto-scroll behavior.
    Supports colored logs and high-contrast backgrounds.
    
    Uses buffering and throttling to handle high-volume logging (100+ lines/sec)
    without crashing the websocket connection.
    """
    def __init__(self, 
                 height: str = '300px', 
                 title: str = "System Logs",
                 flush_interval: float = 0.1,
                 max_history: int = 500):
        """
        Args:
            height: Terminal height (CSS value)
            title: Terminal header title
            flush_interval: How often to flush buffered logs (seconds), default 100ms
            max_history: Maximum number of log lines to keep in history
        """
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
        self._log_buffer: List[str] = []  # Persistent log history
        self._pending_logs: List[str] = []  # Buffered logs waiting to be flushed
        self._max_history = max_history
        
        # JS to track scroll position and update stickiness
        # If user scrolls up, we disable auto-scroll. If they scroll to bottom, we re-enable.
        self.scroll.on('scroll', self._handle_scroll)
        
        # Start the flush timer
        ui.timer(flush_interval, self._flush_logs)

    def _handle_scroll(self, e):
        """Track user scroll position to enable/disable auto-scroll."""
        # e.vertical_percentage is 1.0 when at the bottom
        if e.vertical_percentage >= 0.99:
            self._is_sticky = True
        else:
            self._is_sticky = False

    def log(self, message: str, color: Optional[str] = None):
        """
        Queue a message to be displayed in the terminal.
        Messages are buffered and flushed periodically to prevent websocket overload.
        
        Args:
            message: Log message text
            color: Optional CSS color for the message
        """
        styled_msg = message
        if color:
            styled_msg = f'<span style="color: {color};">{message}</span>'
        
        # Add to pending queue (NOT to UI yet)
        self._pending_logs.append(styled_msg)

    def _flush_logs(self):
        """
        Internal method called by timer to flush buffered logs to the UI.
        Combines all pending messages into a single UI update.
        """
        if not self._pending_logs:
            return
        
        # Move all pending logs to the main buffer
        self._log_buffer.extend(self._pending_logs)
        
        # Trim history if needed
        if len(self._log_buffer) > self._max_history:
            # Remove oldest messages
            overflow = len(self._log_buffer) - self._max_history
            self._log_buffer = self._log_buffer[overflow:]
        
        # Update UI once with all messages
        self.content.set_content("<br>".join(self._log_buffer))
        
        # Clear pending queue
        self._pending_logs.clear()
        
        # Auto-scroll if sticky
        if self._is_sticky:
            # We use a slight delay to ensure content is rendered
            ui.timer(0.05, lambda: self.scroll.scroll_to(percent=1.0), once=True)

    def push(self, message: str, color: Optional[str] = None):
        """
        Alias for log() to match NiceGUI's ui.log().push() API.
        
        Args:
            message: Log message text
            color: Optional CSS color for the message
        """
        self.log(message, color)

    def clear_logs(self):
        """Clear all logs and pending messages."""
        self._log_buffer = []
        self._pending_logs = []
        self.content.set_content("")

    def flush_immediately(self):
        """
        Force an immediate flush of all pending logs.
        Useful when you need to ensure logs are visible right away.
        """
        self._flush_logs()

