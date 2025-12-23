
import pytest
from typer.testing import CliRunner
from sortomatic.cli import app
from sortomatic.core.database import FileIndex

runner = CliRunner()

def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Sortomatic" in result.stdout

def test_cli_scan_all(temp_workspace, mocker):
    """Test 'scan all' command."""
    # Mock the internal _run_pipeline to verify CLI parsing works
    # without running the full threaded pipeline (which hangs in test env)
    mock_run = mocker.patch("sortomatic.cli._run_pipeline")
    
    result = runner.invoke(app, ["scan", "all", str(temp_workspace)])
    
    if result.exit_code != 0:
        print(f"CLI Output: {result.stdout}")
        print(f"Exception: {result.exc_info}")
        
    assert result.exit_code == 0
    mock_run.assert_called_once_with(str(temp_workspace), mode="all")

def test_cli_stats_no_db(temp_workspace):
    """Test stats fails gracefully without DB."""
    # Ensure no DB exists in this temp workspace's default location
    result = runner.invoke(app, ["stats", str(temp_workspace)])
    assert result.exit_code == 1
    assert "No database found" in result.stdout
