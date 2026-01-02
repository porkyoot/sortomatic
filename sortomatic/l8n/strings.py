class Strings:
    # CLI Help and Prompts
    APP_HELP = "Sortomatic: The Elegant File Organizer"
    SCAN_PATH_HELP = "The folder to scan"
    SCAN_RESET_HELP = "Clear database before scanning"
    SCAN_DOC = "Scanning pipeline commands."
    SCAN_ALL_DOC = "Run the full indexing pipeline (Index -> Categorize -> Hash)."
    SCAN_INDEX_DOC = "Pass 1: Just index file paths and metadata (Fastest)."
    SCAN_CAT_DOC = "Pass 2: Categorize files that were just indexed."
    SCAN_HASH_DOC = "Pass 3: Compute hashes for deduplication."
    WIPE_CONFIRM = "Are you sure you want to wipe the database?"
    WIPE_SUCCESS = "Database wiped."
    STATS_DOC = "Show insights about your files."
    STATS_TITLE = "File Distribution"
    CATEGORY_LABEL = "Category"
    COUNT_LABEL = "Count"
    USER_ABORT = "Operation cancelled by user."

    # Engine messages
    PATH_NOT_FOUND = "Path '{path}' does not exist."
    INDEXING_MSG = "Indexing ..."
    CATEGORIZING_MSG = "Categorizing ..."
    HASHING_MSG = "Hashing ..."
    SCAN_COMPLETE = "✨ Scan Complete! Indexed {total_files} files."
    SCAN_INTERRUPTED = "⚠️  Scan interrupted! Progress saved. Run the same command again to resume."
    SCAN_ERROR = "❌ Scan failed with error. Check logs for details."

    # Categories (Source of Truth for Casing from config)
    CAT_IMAGE = "Image"
    CAT_VIDEO = "Video"
    CAT_DOCUMENT = "Document"
    CAT_MUSIC = "Music"
    CAT_ARCHIVE = "Archive"
    CAT_CODE = "Code"
    CAT_3D = "3D"
    CAT_SOFTWARE = "Software"
    CAT_OTHER = "Other"
    CAT_UNSORTED = "Unsorted"
    
    DEFAULT_MIME = "application/octet-stream"

    @classmethod
    def get_category_name(cls, key: str) -> str:
        mapping = {
            "Image": cls.CAT_IMAGE,
            "Images": cls.CAT_IMAGE,
            "Video": cls.CAT_VIDEO,
            "Document": cls.CAT_DOCUMENT,
            "Music": cls.CAT_MUSIC,
            "Archive": cls.CAT_ARCHIVE,
            "Archives": cls.CAT_ARCHIVE,
            "Code": cls.CAT_CODE,
            "3D": cls.CAT_3D,
            "Software": cls.CAT_SOFTWARE,
            "Other": cls.CAT_OTHER
        }
        return mapping.get(key, key)
