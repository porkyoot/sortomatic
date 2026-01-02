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
    TEXT_BG = 'var(--color-bg)'
    BORDER_COLOR = 'var(--color-border)'
    ERROR = 'var(--color-error)'
    WARNING = 'var(--color-warning)'
    SUCCESS = 'var(--color-success)'
    INFO = 'var(--color-info)'
    BG_NUCLEAR = 'var(--color-bg-nuclear)'
    CAT_IMAGE = 'var(--color-cat-image)'
    CAT_VIDEO = 'var(--color-cat-video)'
    CAT_DOC = 'var(--color-cat-document)'
    CAT_AUDIO = 'var(--color-cat-audio)'
    CAT_OTHER = 'var(--color-cat-other)'
    FOLDER = 'var(--color-folder)'
    FILE = 'var(--color-file)'
    WHITE = 'var(--color-white)'
    BLACK = 'var(--color-black)'
    
    # RGB Components for opacity support
    RGB_BG = 'var(--rgb-base03)'
    RGB_SURFACE = 'var(--rgb-base02)'
    RGB_TEXT_MAIN = 'var(--rgb-base1)'
    
    RGB_PRIMARY = 'var(--rgb-blue)'
    RGB_SECONDARY = 'var(--rgb-magenta)'
    RGB_ERROR = 'var(--rgb-red)'
    RGB_WARNING = 'var(--rgb-orange)'
    RGB_SUCCESS = 'var(--rgb-green)'
    RGB_INFO = 'var(--rgb-cyan)'
    
    RGB_CAT_IMAGE = 'var(--rgb-violet)'
    RGB_CAT_VIDEO = 'var(--rgb-magenta)'
    RGB_CAT_DOC = 'var(--rgb-blue)'
    RGB_CAT_AUDIO = 'var(--rgb-cyan)'
    RGB_CAT_OTHER = 'var(--rgb-base01)'
    GLASS = 'premium-glass'
    SHADOW = 'soft-shadow'
    BORDER = 'thin-border'
    
    # Fonts
    FONT_MAIN = 'font-family: var(--font-main);'

    @staticmethod
    def load_theme():
        """Loads the app.css file and sets up NiceGUI global colors."""
        import time
        ui.add_head_html(f'<link href="/themes/app.css?v={int(time.time())}" rel="stylesheet">')
        ui.colors(
            primary='#268bd2',    # blue
            secondary='#d33682',  # magenta
            accent='#2aa198',     # cyan
            dark='#002b36',       # base03
            positive='#859900',   # green
            negative='#dc322f',   # red
            info='#2aa198',       # cyan
            warning='#cb4b16',    # orange
        )

theme = Style()
