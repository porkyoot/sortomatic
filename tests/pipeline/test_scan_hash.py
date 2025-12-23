
import pytest
import tempfile
from sortomatic.core.pipeline.manager import PipelineManager
from sortomatic.core.database import FileIndex

def test_hash_integration(test_db):
    """Test the run_hash pipeline pass with real files."""
    manager = PipelineManager()
    
    # Create real temporary files so hashing can read them
    with tempfile.NamedTemporaryFile(delete=False) as f1, \
         tempfile.NamedTemporaryFile(delete=False) as f2:
        
        f1.write(b"content1")
        f1.close()
        
        f2.write(b"content2")
        f2.close()
        
        # Pre-seed DB
        from datetime import datetime
        now = datetime.now()
        FileIndex.create(path=f1.name, filename="f1", size_bytes=8, entry_type='file', modified_at=now)
        FileIndex.create(path=f2.name, filename="f2", size_bytes=8, entry_type='file', modified_at=now)
        
        # Run hash pass
        count = manager.run_hash()
        
        assert count == 2
        
        # Verify hashes
        rec1 = FileIndex.get(path=f1.name)
        rec2 = FileIndex.get(path=f2.name)
        
        assert rec1.full_hash is not None
        assert rec2.full_hash is not None
        assert rec1.full_hash != rec2.full_hash

def test_hash_skip_bundles(test_db):
    """Test that hashing skips bundles."""
    manager = PipelineManager()
    
    # Bundle entry
    from datetime import datetime
    FileIndex.create(path="/tmp/app.app", filename="app.app", size_bytes=100, entry_type='bundle', modified_at=datetime.now())
    
    count = manager.run_hash()
    assert count == 0
