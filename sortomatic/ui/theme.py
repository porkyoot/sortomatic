from dataclasses import dataclass, field
from nicegui import ui

# --- 1. DESIGN TOKENS (The "DNA") ---

@dataclass
class ThemeColors:
    """Semantic color names, not just 'blue' or 'red'."""
    surface_1: str  # Main background
    surface_2: str  # Secondary background (cards)
    surface_3: str  # Tertiary (hovers, inputs)
    text_main: str
    text_subtle: str
    primary: str
    secondary: str
    
    # Accents
    green: str
    red: str
    cyan: str
    orange: str
    yellow: str
    blue: str
    magenta: str
    violet: str

    # Functional
    debug: str
    info: str
    success: str
    warning: str
    error: str

    # Accents for visualization
    accents: dict[str, str] = field(default_factory=dict)

@dataclass
class ThemeLayout:
    """Responsive spacing and sizing tokens (using REM)."""
    # Spacing scale: 0=0, 1=0.25rem, 2=0.5rem, 4=1rem, etc.
    spacing_unit: str = "0.25rem" 
    
    # Radii
    radius_sm: str = "0.25rem"  # 4px
    radius_md: str = "0.5rem"   # 8px
    radius_lg: str = "1rem"     # 16px
    radius_full: str = "9999px"
    
    # Typography
    font_sans: str = "'Recursive', 'Inter', system-ui, sans-serif"
    font_mono: str = "'Recursive', 'JetBrains Mono', monospace"


@dataclass
class Theme:
    colors: ThemeColors
    layout: ThemeLayout = field(default_factory=ThemeLayout)


# --- 2. CSS GENERATOR (The "Compiler") ---
# Moved to styles.py to keep concerns separated (Theme=Data, Styles=Implementation)


# --- 3. LOGIC ADAPTERS (For Backward Compatibility & Helper Logic) ---

class CategoryStyles:
    """Centralized management for category colors and ordering."""
    
    @staticmethod
    def get_color(category: str, theme: Theme) -> str:
        from sortomatic.l8n import Strings
        
        # Map to accents or theme colors
        mapping = {
            Strings.CAT_IMAGE: theme.colors.green,
            Strings.CAT_VIDEO: theme.colors.red,
            Strings.CAT_DOCUMENT: theme.colors.cyan,
            Strings.CAT_MUSIC: theme.colors.orange,
            Strings.CAT_ARCHIVE: theme.colors.yellow,
            Strings.CAT_CODE: theme.colors.blue,
            Strings.CAT_3D: theme.colors.magenta,
            Strings.CAT_SOFTWARE: theme.colors.violet,
            Strings.CAT_OTHER: theme.colors.debug,
        }
        return mapping.get(category, theme.colors.debug)

    @staticmethod
    def get_icon(category: str) -> str:
        from sortomatic.l8n import Strings
        mapping = {
            Strings.CAT_IMAGE: "mdi-image",
            Strings.CAT_VIDEO: "mdi-video",
            Strings.CAT_DOCUMENT: "mdi-file-document",
            Strings.CAT_MUSIC: "mdi-music",
            Strings.CAT_ARCHIVE: "mdi-archive",
            Strings.CAT_CODE: "mdi-console",
            Strings.CAT_3D: "mdi-cube-outline",
            Strings.CAT_SOFTWARE: "mdi-apps",
            Strings.CAT_OTHER: "mdi-file",
        }
        return mapping.get(category, "mdi-file")

    @staticmethod
    def get_order() -> list[str]:
        from ..l8n import Strings
        return [
            Strings.CAT_OTHER,
            Strings.CAT_DOCUMENT,
            Strings.CAT_IMAGE,
            Strings.CAT_ARCHIVE,
            Strings.CAT_MUSIC,
            Strings.CAT_VIDEO,
            Strings.CAT_3D,
            Strings.CAT_SOFTWARE,
            Strings.CAT_CODE,
        ]

class StatusStyles:
    """Centralized management for status colors and icons."""
    
    # Generic state constants
    UNKNOWN = "unknown"
    PENDING = "pending"
    READY = "ready"
    ERROR = "error"
    IDLE = "idle"
    
    # Synonyms mapping
    _SYNONYMS = {
        "refreshing": PENDING,
        "active": READY,
        "busy": PENDING,
        "available": READY,
        "unavailable": ERROR,
        "inactive": ERROR,
        "running": PENDING,
        "stopped": UNKNOWN,
    }

    @staticmethod
    def resolve_state(state: str) -> str:
        s = state.lower()
        if s in [StatusStyles.UNKNOWN, StatusStyles.PENDING, StatusStyles.READY, StatusStyles.ERROR, StatusStyles.IDLE]:
            return s
        return StatusStyles._SYNONYMS.get(s, StatusStyles.UNKNOWN)

    @staticmethod
    def get_color(state: str, theme: Theme) -> str:
        resolved = StatusStyles.resolve_state(state)
        mapping = {
            StatusStyles.UNKNOWN: theme.colors.debug,
            StatusStyles.PENDING: theme.colors.warning,
            StatusStyles.READY: theme.colors.success,
            StatusStyles.ERROR: theme.colors.error,
            StatusStyles.IDLE: theme.colors.info,
        }
        return mapping.get(resolved, theme.colors.debug)

    @staticmethod
    def get_icon(state: str) -> str:
        resolved = StatusStyles.resolve_state(state)
        mapping = {
            StatusStyles.UNKNOWN: "mdi-help-circle-outline",
            StatusStyles.PENDING: "mdi-sync",
            StatusStyles.READY: "mdi-check-circle",
            StatusStyles.ERROR: "mdi-alert-circle-outline",
            StatusStyles.IDLE: "mdi-pause-circle",
        }
        return mapping.get(resolved, "mdi-help-circle-outline")
