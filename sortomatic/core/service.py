from sortomatic.core.bridge import bridge
from sortomatic.core.database import get_children
from sortomatic.utils.logger import logger

def init_bridge_handlers():
    """
    Registers backend handlers for the bridge.
    This connects the decoupled UI requests to the actual database/logic.
    """
    
    # 1. File Tree Children Request
    @bridge.handle_request("get_file_tree")
    async def handle_get_file_tree(payload):
        """
        Payload: { 'path': str, 'search': Optional[str] }
        """
        path = payload.get('path', '/')
        search = payload.get('search')
        
        logger.debug(f"Service: Fetching tree for {path} (search: {search})")
        folders, files = get_children(path, search=search)
        
        # We can format the data here if needed to make it pure JSON-like,
        # but for now we'll pass the model instances or dictionaries.
        return {
            "folders": folders,
            "files": [
                {
                    "filename": f.filename,
                    "path": f.path,
                    "category": f.category,
                    "size_bytes": f.size_bytes,
                    "modified_at": f.modified_at,
                } for f in files
            ]
        }

    logger.info("Bridge handlers initialized.")
