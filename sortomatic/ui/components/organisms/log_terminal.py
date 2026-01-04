from nicegui import ui
import logging
import asyncio
from typing import List, Tuple
from collections import deque
from datetime import datetime

from sortomatic.ui.components import atoms
from sortomatic.utils.logger import logger

class LogTerminalHandler(logging.Handler):
    """
    Custom logging handler that forwards records to a callback.
    """
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def emit(self, record):
        try:
            msg = self.format(record)
            # Use record.created for accurate timestamp, or just now()
            ts = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
            self.callback(ts, record.levelname, msg)
        except Exception:
            self.handleError(record)

def log_terminal(height: str = '200px') -> ui.card:
    """
    A persistent terminal-like component to show system logs.
    """
    
    # State
    log_queue: deque = deque()
    auto_scroll = [True] # Mutable wrapper
    is_scrolling = [False]
    
    # CSS Variable Mapping for Logs
    color_map = {
        "INFO": "var(--color-info)",
        "WARN": "var(--color-warning)",
        "WARNING": "var(--color-warning)",
        "ERROR": "var(--color-error)",
        "FAILURE": "var(--color-error)",
        "SUCCESS": "var(--color-success)",
        "DEBUG": "var(--color-debug)",
        "FATAL": "var(--color-error)",
        "CRITICAL": "var(--color-error)"
    }

    # Handler Callback
    def on_new_log(ts: str, level: str, msg: str):
        log_queue.append((ts, level, msg))

    # Setup Container
    # We use bg-bg (Base03) for the terminal, replacing the lighter glass effect.
    with atoms.card().classes('w-full relative overflow-hidden flex flex-col bg-bg thin-border', remove='p-4 premium-glass').style(f'height: {height};') as container:
        
        # Inner Terminal Area
        # Using bg-bg which is usually darker than surface in current theme setup? 
        # Actually surface is usually lighter. Let's use var(--color-bg) to have contrast on the card.
        terminal_area = ui.scroll_area().classes('w-full h-full p-2 font-mono text-xs bg-bg')
        
        with terminal_area:
            log_content = ui.column().classes('w-full gap-0').style('overflow-wrap: break-word; word-wrap: break-word;')
            
        # Scroll Handler
        def handle_scroll(e):
            if is_scrolling[0]:
                return
            
            # If user scrolls up significantly, disable auto-scroll
            if e.vertical_percentage >= 0.99:
                auto_scroll[0] = True
            elif e.vertical_percentage > 0.0:
                auto_scroll[0] = False
                
        terminal_area.on('scroll', handle_scroll)

        # UI Update Loop
        async def update_ui():
            if not log_queue:
                pass 
            else:
                # Process batch
                batch: List[Tuple[str, str, str]] = []
                while log_queue:
                    batch.append(log_queue.popleft())
                
                with log_content:
                    for ts, level, msg in batch:
                        color = color_map.get(level, "var(--color-text-main)")
                        msg = msg.rstrip()
                        if not msg:
                            continue
                        
                        # Format: [HH:MM:SS] [LEVEL] Message
                        # We use a row or just a label. Label with spans is efficient.
                        # ui.html might be faster for bulk, but label is safer.
                        # Let's use pre-wrap label.
                        text = f"[{ts}] [{level}] {msg}"
                        ui.label(text).style(f'color: {color}; white-space: pre-wrap; word-break: break-word; line-height: 1.2;').classes('w-full font-mono text-xs')

            # Auto-scroll
            if auto_scroll[0]:
                is_scrolling[0] = True
                try:
                    terminal_area.scroll_to(percent=1.0)
                except:
                    pass
                finally:
                    is_scrolling[0] = False

        timer = ui.timer(0.1, update_ui)

        # Logging integration
        handler = LogTerminalHandler(on_new_log)
        # We assume the user wants to see Sortomatic logs.
        # If we use the root logger, we might get too much noise.
        # But 'sortomatic' logger is what we want.
        logger.addHandler(handler)
        
        # Cleanup
        def cleanup():
            logger.removeHandler(handler)
            timer.cancel()
            
        container.on('delete', cleanup)

    return container
