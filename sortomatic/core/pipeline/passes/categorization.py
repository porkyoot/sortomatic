try:
    import filetype
except ImportError:
    filetype = None

import threading
import os
from pathlib import Path
from ...config import settings
from ....l8n import Strings
from ....utils.logger import logger

def detect_type(ctx: dict):
    """
    Pass 1: Detects category and mime type.
    """
    if not os.path.isfile(ctx['path']):
        return ctx
        
    path = Path(ctx['path'])
    
    # 1. Extension Strategy
    ext = path.suffix.lower()
    category = settings.get_category(ext)
    
    # 2. Magic Bytes Strategy (if unknown or suspicious)
    mime = Strings.DEFAULT_MIME
    
    # Capture a local reference to the global filetype module.
    # This prevents issues if the module-level variable is temporarily None 
    # (e.g. during a weird reload or thread closure lookup).
    ft_module = filetype 
    
    if ft_module and (category == Strings.CAT_OTHER or category == Strings.CAT_UNSORTED):
        # Use a thread to enforce a timeout on magic byte detection.
        # This prevents the whole pipeline from hanging on slow I/O or malformed files.
        result_container = {"kind": None}
        
        def target():
            try:
                # Double-check ft_module within the thread scope
                if ft_module is not None:
                    result_container["kind"] = ft_module.guess(str(path))
            except Exception as e:
                # We use a broad catch here because filetype can be buggy on weird file headers
                logger.debug(f"Filetype detection failed for {path}: {e}")

        detect_thread = threading.Thread(target=target, daemon=True)
        detect_thread.start()
        
        warning_timeout = settings.categorization_timeout * 0.8
        detect_thread.join(timeout=warning_timeout)
        
        if detect_thread.is_alive():
            logger.warning(f"⚠️ Categorization is slow for: {path}. Reached 80% of timeout...")
            detect_thread.join(timeout=settings.categorization_timeout - warning_timeout)
        
        kind = result_container["kind"]
        if kind:
            try:
                mime = kind.mime
                # Reverse lookup category from mime if possible
                if kind.mime.startswith("image"): 
                    category = Strings.CAT_IMAGE
                elif kind.mime.startswith("video"): 
                    category = Strings.CAT_VIDEO
                elif kind.mime.startswith("audio"):
                    category = Strings.CAT_MUSIC
                elif kind.mime in ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                    category = Strings.CAT_DOCUMENT
                elif kind.mime in ["application/zip", "application/x-tar", "application/x-rar-compressed", "application/x-7z-compressed"]:
                    category = Strings.CAT_ARCHIVE
            except Exception:
                pass
            
    ctx['extension'] = ext
    ctx['category'] = category
    ctx['mime_type'] = mime
    return ctx