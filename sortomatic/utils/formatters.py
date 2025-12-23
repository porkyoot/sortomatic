from datetime import datetime, timedelta
from typing import Tuple

def format_size(size_bytes: int) -> Tuple[str, str, str]:
    """
    Returns (value, unit, color_var)
    Breakpoints:
    kB (Green): < 1024 * 1024
    MB (Yellow): < 1024 * 1024 * 1024
    GB (Red): >= 1024 * 1024 * 1024
    """
    kb = 1024
    mb = kb * 1024
    gb = mb * 1024
    
    if size_bytes < mb:
        return f"{size_bytes / kb:.1f}", "kB", "var(--q-success)"
    elif size_bytes < gb:
        return f"{size_bytes / mb:.1f}", "MB", "var(--q-warning)"
    else:
        return f"{size_bytes / gb:.1f}", "GB", "var(--q-error)"

def format_date_human(dt: datetime) -> Tuple[str, str]:
    """
    Returns (humanized_string, color_var)
    Breakpoints:
    Days (Green): < 30 days
    Months (Yellow): < 365 days
    Years (Red): >= 365 days
    """
    now = datetime.now()
    diff = now - dt
    
    days = diff.days
    
    if days < 30:
        if days == 0:
            return "Today", "var(--q-success)"
        if days == 1:
            return "Yesterday", "var(--q-success)"
        return f"{days} days ago", "var(--q-success)"
    elif days < 365:
        months = days // 30
        if months == 1:
            return "1 month ago", "var(--q-warning)"
        return f"{months} months ago", "var(--q-warning)"
    else:
        years = days // 365
        if years == 1:
            return "1 year ago", "var(--q-error)"
        return f"{years} years ago", "var(--q-error)"
