from nicegui import ui

class Style:
    """
    Centralized style constants and helpers for the Sortomatic Premium Theme.
    """
    
    # Colors (Matching CSS variables for use in Python if needed)
    BG = 'var(--color-bg)'
    SURFACE = 'var(--color-surface)'
    PRIMARY = 'var(--color-primary)'
    SECONDARY = 'var(--color-secondary)'
    TEXT_MAIN = 'var(--color-text-main)'
    TEXT_MUTED = 'var(--color-text-muted)'
    
    # Utility Classes
    GLASS = 'premium-glass'
    SHADOW = 'soft-shadow'
    BORDER = 'thin-border'
    
    # Fonts
    FONT_MAIN = 'font-family: var(--font-main);'

    @staticmethod
    def load_theme():
        """Loads the app.css file."""
        ui.add_head_html('<link href="themes/app.css" rel="stylesheet">')
        # Alternatively, we can serve it or include it directly if specific path handling is needed.
        # For now, we assume it's served or accessible.
        # Since we are in a package, we might need to be careful with paths.
        # However, for a simple start:
        pass

theme = Style()
