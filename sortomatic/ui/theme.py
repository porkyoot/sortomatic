# --- 1. LOGIC ADAPTERS (Stateless) ---

class CategoryStyles:
    """Centralized management for category colors and ordering."""
    
    @staticmethod
    def get_color(category: str) -> str:
        from sortomatic.l8n import Strings
        
        # Map to CSS variables defined by nicetheme
        mapping = {
            Strings.CAT_IMAGE: "var(--nt-color-green)",
            Strings.CAT_VIDEO: "var(--nt-color-red)",
            Strings.CAT_DOCUMENT: "var(--nt-color-cyan)",
            Strings.CAT_MUSIC: "var(--nt-color-orange)",
            Strings.CAT_ARCHIVE: "var(--nt-color-yellow)",
            Strings.CAT_CODE: "var(--nt-color-blue)",
            Strings.CAT_3D: "var(--nt-color-magenta)",
            Strings.CAT_SOFTWARE: "var(--nt-color-violet)",
            Strings.CAT_OTHER: "var(--nt-color-base00)", # Fallback/Debug
        }
        return mapping.get(category, "var(--nt-color-base00)")

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
    def get_color(state: str) -> str:
        resolved = StatusStyles.resolve_state(state)
        mapping = {
            StatusStyles.UNKNOWN: "var(--nt-color-base00)",
            StatusStyles.PENDING: "var(--nt-warning)",
            StatusStyles.READY: "var(--nt-positive)",
            StatusStyles.ERROR: "var(--nt-negative)",
            StatusStyles.IDLE: "var(--nt-info)",
        }
        return mapping.get(resolved, "var(--nt-color-base00)")

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
