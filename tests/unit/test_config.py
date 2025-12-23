
import pytest
from pathlib import Path
from sortomatic.core.config import Settings, settings
from sortomatic.l8n import Strings

def test_config_defaults(temp_home):
    """Test that default config files are created if missing."""
    # Re-initialize Settings to trigger _ensure_config_exists using the temp_home fixture
    new_settings = Settings()
    
    assert new_settings.config_dir.exists()
    assert (new_settings.config_dir / "settings.yaml").exists()
    assert (new_settings.config_dir / "filetypes.yaml").exists()

def test_category_lookup():
    """Test extension to category mapping."""
    # Known extensions
    assert settings.get_category(".jpg") == Strings.CAT_IMAGES
    assert settings.get_category(".JPG") == Strings.CAT_IMAGES
    assert settings.get_category(".pdf") == Strings.CAT_DOCUMENTS
    assert settings.get_category(".py") == Strings.CAT_CODE
    
    # Unknown extension
    assert settings.get_category(".xyz123") == Strings.CAT_OTHERS
    
    # No extension
    assert settings.get_category("Makefile") == Strings.CAT_OTHERS

def test_custom_overrides(temp_home):
    """Test loading settings from yaml."""
    # Write custom settings
    config_dir = temp_home / ".config" / "sortomatic"
    config_dir.mkdir(parents=True)
    
    (config_dir / "settings.yaml").write_text("""
    max_workers: 42
    batch_size: 999
    """)
    
    new_settings = Settings()
    assert new_settings.max_workers == 42
    assert new_settings.batch_size == 999
