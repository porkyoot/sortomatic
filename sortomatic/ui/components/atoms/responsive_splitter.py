from nicegui import ui
from typing import Tuple

# Define CSS for responsiveness
# We want to stack vertically on mobile (< 768px typically, matching md breakpoint)
# and hide the separator.
RESPONSIVE_CSS = """
<style>
    @media (max-width: 768px) {
        .responsive-splitter.q-splitter--vertical {
            flex-direction: column !important;
        }
        .responsive-splitter.q-splitter--vertical > .q-splitter__panel {
            width: 100% !important;
            height: auto !important;
            flex: none !important;
            min-height: 0 !important;
            display: flex !important;
            flex-direction: column !important;
            overflow: visible !important;
        }
        .responsive-splitter.q-splitter--vertical > .q-splitter__separator {
             display: none !important;
        }
        /* Ensure children card can take their declared height on mobile */
        .responsive-splitter.q-splitter--vertical > .q-splitter__panel > .nicegui-card {
            flex: none !important;
        }
    }
    
    /* Ensure panels are flex containers on desktop and allow overflow for 80vh cards */
    .responsive-splitter > .q-splitter__panel {
        display: flex !important;
        flex-direction: column !important;
        overflow: visible !important;
    }

    /* Custom Separator Styling (Scrollbar-like) */
    .responsive-splitter .q-splitter__separator {
        width: 10px !important; /* User requested 10px */
        background-color: transparent !important; /* User requested remove background */
        position: relative; /* Ensure ::after is positioned correctly */
    }
    
    /* The visible handle */
    .responsive-splitter .q-splitter__separator::after {
        content: '';
        position: absolute;
        top: 0; bottom: 0; left: 3px; right: 3px; /* Centered handle */
        background-color: var(--color-border); /* Match border color */
        border-radius: 2px; 
        transition: background-color 0.3s;
        opacity: 0.6;
    }
    
    .responsive-splitter .q-splitter__separator:hover::after {
        background-color: var(--color-primary); /* Highlight on hover */
        opacity: 0.8;
    }
</style>
"""

def responsive_splitter(
    value: float = 20.0, 
    limits: Tuple[float, float] = (10.0, 90.0),
    **kwargs
) -> ui.splitter:
    """
    A responsive splitter component that behaves like ui.splitter but switches
    to a stacked layout (one column) on mobile devices.
    
    Args:
        value: Initial split position in percentage (default: 20.0)
        limits: Tuple of minimum and maximum percentage values (default: (10.0, 90.0))
        **kwargs: Additional arguments passed to ui.splitter
        
    Returns:
        ui.splitter: The configured splitter element.
    """
    # Inject the responsive styles once
    ui.add_head_html(RESPONSIVE_CSS)
    
    splitter = ui.splitter(value=value, limits=limits, **kwargs)
    splitter.classes('responsive-splitter w-full h-full overflow-hidden bg-transparent')
    
    return splitter
