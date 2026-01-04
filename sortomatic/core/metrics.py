import psutil
import time
import shutil
from typing import Dict, Any, List

class SystemMetrics:
    """
    Fetches system performance metrics: CPU, RAM, Disk IO, GPU.
    Maintains internal state for differential metrics (Disk IO).
    """
    def __init__(self):
        # Initial disk counters for rate calculation
        self.last_disk_io = psutil.disk_io_counters()
        self.last_disk_time = time.time()
        
        # Determine main disk path for usage stats if needed, or just use broad IO
        self.has_gpu = self._check_nvidia_gpu()

    def _check_nvidia_gpu(self) -> bool:
        """Check if nvidia-smi is available."""
        return shutil.which('nvidia-smi') is not None

    def get_cpu_percent(self) -> float:
        """Returns CPU usage as float 0.0-1.0"""
        # interval=None is non-blocking but requires previous call. 
        # First call returns 0.0.
        return psutil.cpu_percent(interval=None) / 100.0

    def get_ram_percent(self) -> float:
        """Returns RAM usage as float 0.0-1.0"""
        return psutil.virtual_memory().percent / 100.0

    def get_disk_speed_mbs(self) -> float:
        """
        Returns Disk IO speed in MB/s.
        """
        current_io = psutil.disk_io_counters()
        current_time = time.time()
        
        if not self.last_disk_io or not current_io:
            return 0.0
            
        dt = current_time - self.last_disk_time
        if dt < 0.1: # Avoid division by zero or super-fast calls
            return 0.0
            
        # Calculate delta bytes (read + write)
        read_bytes = current_io.read_bytes - self.last_disk_io.read_bytes
        write_bytes = current_io.write_bytes - self.last_disk_io.write_bytes
        total_bytes = read_bytes + write_bytes
        
        # Calculate speed in MB/s
        speed_mb_s = (total_bytes / dt) / (1024 * 1024)
        
        # Update state
        self.last_disk_io = current_io
        self.last_disk_time = current_time
        
        return speed_mb_s

    def get_gpu_percent(self) -> float:
        """
        Returns GPU usage as float 0.0-1.0. 
        Requires nvidia-smi. Returns 0.0 if not available.
        """
        if not self.has_gpu:
            return 0.0
            
        try:
            # Simple query for utilization.gpu
            import subprocess
            result = subprocess.check_output(
                ['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'],
                stderr=subprocess.DEVNULL
            )
            # result looks like b'45\n'
            usage = int(result.strip())
            return usage / 100.0
        except Exception:
            return 0.0

    def get_all_metrics(self) -> Dict[str, float]:
        """Aggregate all current metrics."""
        return {
            'cpu': self.get_cpu_percent(),
            'ram': self.get_ram_percent(),
            'disk': self.get_disk_speed_mbs(),
            'gpu': self.get_gpu_percent()
        }

# Global instance
metrics_monitor = SystemMetrics()
