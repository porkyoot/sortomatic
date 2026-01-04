from sortomatic.core.bridge import bridge
from sortomatic.core.metrics import metrics_monitor
from typing import Dict

def register_resource_handlers():
    """Validates and registers resource monitoring handlers with the bridge."""
    
    @bridge.handle_request('get_resource_usage')
    def get_resource_usage(_) -> Dict[str, float]:
        """
        Returns system resource usage percentages (0-100).
        """
        raw = metrics_monitor.get_all_metrics()
        # Convert 0.0-1.0 to 0-100 for UI consistency if needed, 
        # but metrics.py returns 0.0-1.0. 
        # Let's check:
        # metrics.py: cpu_percent() / 100.0 -> 0.0-1.0
        # UI (Plots): Previous psutil call returned 0-100.
        # Plots.py logic: if val < 50 (expects 0-100).
        # So I should multiply by 100 here.
        # Disk returns speed in MB/s now, so we pass it raw (or maybe apply scaling if graph expects it?)
        # Let's pass it raw and let UI handle scaling/units.
        return {
            'cpu': raw['cpu'] * 100,
            'ram': raw['ram'] * 100,
            'disk': raw['disk'], # Use raw MB/s
            'gpu': raw['gpu'] * 100
        }
