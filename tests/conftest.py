
import pytest
import os
import shutil
import tempfile
from pathlib import Path
from sortomatic.core.database import db, FileIndex, init_db
from sortomatic.core.config import settings

@pytest.fixture
def temp_home():
    """Creates a temporary directory acting as HOME for config testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        old_home = os.environ.get('HOME')
        os.environ['HOME'] = tmpdir
        yield Path(tmpdir)
        if old_home:
            os.environ['HOME'] = old_home

@pytest.fixture
def test_db():
    """Initializes an in-memory database for testing."""
    from peewee import SqliteDatabase
    
    # Initialize with in-memory DB
    database = SqliteDatabase(':memory:', pragmas={'foreign_keys': 1})
    db.initialize(database)
    
    db.connect()
    db.create_tables([FileIndex])
    
    yield db
    
    db.close()
    # Reset proxy for next test to ensure isolation
    db.obj = None
    
@pytest.fixture
def temp_workspace():
    """Creates a temporary workspace with some files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        
        # Create some structure
        (path / "documents").mkdir()
        (path / "images").mkdir()
        
        (path / "test.txt").write_text("Hello World")
        (path / "documents" / "report.pdf").write_text("Fake PDF content")
        (path / "images" / "photo.jpg").write_text("Fake JPG content")
        
        yield path

@pytest.fixture(autouse=True)
def mock_settings(test_db):
    """Ensure settings are isolated and DB is reset."""
    # Reset config for each test to avoid pollution
    settings.batch_size = 10
    settings.reset_db = False
    return settings
