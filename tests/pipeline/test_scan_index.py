
import pytest
from sortomatic.core.pipeline.manager import PipelineManager
from sortomatic.core.database import FileIndex

def test_index_pass_logic():
    """Test the _index_pass method logic."""
    manager = PipelineManager()
    
    # Needs a real file to stat
    import tempfile
    with tempfile.NamedTemporaryFile() as f:
        item = (f.name, 'file')
        ctx = manager._index_pass(item)
        
        assert ctx is not None
        assert ctx['path'] == f.name
        assert ctx['entry_type'] == 'file'
        assert ctx['size_bytes'] == 0
        assert ctx['category'] is None

def test_run_index(temp_workspace, test_db):
    """Test the full run_index pipeline."""
    manager = PipelineManager()
    
    # Run index on temp workspace
    result = manager.run_index(str(temp_workspace))
    
    # Check result summary
    assert result['count'] == 3  # test.txt, report.pdf, photo.jpg
    
    # Verify DB contents
    files = list(FileIndex.select())
    assert len(files) == 3
    
    filenames = {f.filename for f in files}
    assert "test.txt" in filenames
    assert "report.pdf" in filenames
    assert "photo.jpg" in filenames
    
    # Verify initial state (categorize/hash should be empty/null from index pass unless bundle)
    for f in files:
        assert f.category is None
        assert f.full_hash is None
