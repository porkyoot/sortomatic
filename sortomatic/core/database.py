from peewee import *
from peewee import fn
from datetime import datetime
from pathlib import Path
from typing import Optional
from sortomatic.utils.logger import logger

# We use a Proxy to delay the actual DB connection until we run 'init_db'
db = DatabaseProxy()

class BaseModel(Model):
    class Meta:
        database = db

class FileIndex(BaseModel):
    path = CharField(unique=True, index=True, max_length=1024)
    filename = CharField(index=True)
    extension = CharField(null=True)
    size_bytes = IntegerField()
    modified_at = DateTimeField()
    
    # New Field: 'file' or 'bundle' (for atomic folders)
    entry_type = CharField(default='file', index=True) 
    
    # Analysis
    category = CharField(null=True, index=True)
    mime_type = CharField(null=True)  # Result of 'file' command check
    
    # Hashing
    fast_hash = CharField(null=True, index=True) # e.g. MD5 partial
    full_hash = CharField(null=True, index=True) # e.g. SHA-256
    perceptual_hash = CharField(null=True)       # For images
    
    is_duplicate = BooleanField(default=False)
    group_id = CharField(null=True, index=True)  # To group duplicates together
    
    # For the "War Room" (Review phase)
    action_pending = CharField(null=True) # e.g., 'KEEP', 'IGNORE', 'MERGE'

def init_db(db_path: str = "data/sortomatic.db"):
    """
    Initializes the SQLite connection with high-performance settings.
    """
    # WAL mode allows simultaneous reading and writing (crucial for concurrency)
    database = SqliteDatabase(db_path, pragmas={
        'journal_mode': 'wal',
        'cache_size': -1024 * 64,  # 64MB cache
        'synchronous': 0           # Risky but fast for local tools
    })
    
    # Bind the proxy to the real database
    db.initialize(database)
    logger.info(f"Database initialized at {db_path} (WAL mode). Proxy ID: {id(db)}")
    
    # Create tables if they don't exist
    db.connect()
    db.create_tables([FileIndex])
    
    return database

def get_children(parent_path: str, search: Optional[str] = None):
    """
    Returns (folders, files) for a given path.
    Folders are strings (names).
    Files are FileIndex instances.
    """
    if not parent_path.endswith('/'):
        parent_path += '/'
    
    if not db.obj:
        logger.error(f"DB ERROR: Proxy NOT initialized! ID: {id(db)}")
        return [], []

    logger.info(f"DB: Querying children for {parent_path} using Proxy ID: {id(db)}")
    
    # We fetch all matching files under this parent path and process them in Python 
    # to extract immediate children folders and files. This avoids complex 
    # SQL string manipulation that Varies across DB drivers in Peewee.
    query = FileIndex.select().where(FileIndex.path.startswith(parent_path))
    
    if search:
        query = query.where(FileIndex.filename.contains(search))
        
    folders = set()
    files = []
    
    prefix_len = len(parent_path)
    for index_entry in query:
        # Get the path relative to the current folder we are viewing
        rel_path = index_entry.path[prefix_len:]
        
        if '/' in rel_path:
            # It's inside a subfolder, extract the immediate subfolder name
            immediate_folder = rel_path.split('/')[0]
            folders.add(immediate_folder)
        else:
            # It's a file in the current folder
            files.append(index_entry)
            
    return sorted(list(folders)), sorted(files, key=lambda f: f.filename)

def close_db():
    """
    Closes the database connection.
    """
    try:
        if not db.is_closed():
            db.close()
            logger.debug("Database connection closed.")
    except AttributeError:
        # Proxy was never initialized
        pass