
import pytest
from sortomatic.core.pipeline.manager import PipelineManager
from sortomatic.core.database import FileIndex
from sortomatic.l8n import Strings

def test_categorize_integration(test_db):
    """Test the run_categorize pipeline pass."""
    manager = PipelineManager()
    
    # Pre-seed DB with uncategorized files
    from datetime import datetime
    now = datetime.now()
    FileIndex.create(path="/tmp/test.jpg", filename="test.jpg", size_bytes=100, entry_type='file', modified_at=now)
    FileIndex.create(path="/tmp/doc.pdf", filename="doc.pdf", size_bytes=200, entry_type='file', modified_at=now)
    FileIndex.create(path="/tmp/unknown.xyz", filename="unknown.xyz", size_bytes=300, entry_type='file', modified_at=now)
    
    # Run categorize pass
    count = manager.run_categorize()
    
    assert count == 3
    
    # Verify updates
    img = FileIndex.get(filename="test.jpg")
    assert img.category == Strings.CAT_IMAGES
    
    doc = FileIndex.get(filename="doc.pdf")
    assert doc.category == Strings.CAT_DOCUMENTS
    
    unk = FileIndex.get(filename="unknown.xyz")
    assert unk.category == Strings.CAT_OTHERS
