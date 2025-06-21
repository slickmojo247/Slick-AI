import time
from datetime import datetime
from typing import Dict, Any
import logging
import pandas as pd

class PerformanceMonitor:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.metrics = {
            "response_times": [],
            "error_rates": [],
            "mode_usage": {}
        }
        self.log.info("Performance Monitor initialized")

    def track(self, func):
        """Decorator to track function performance"""
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            
            self.metrics["response_times"].append({
                "timestamp": datetime.now(),
                "function": func.__name__,
                "duration": duration
            })
            
            if "error" in result:
                self.metrics["error_rates"].append({
                    "timestamp": datetime.now(),
                    "function": func.__name__,
                    "error": result["error"]
                })
            
            return result
        return wrapper

    def record_mode_usage(self, mode: str):
        """Track personality mode usage"""
        self.metrics["mode_usage"][mode] = self.metrics["mode_usage"].get(mode, 0) + 1

    def get_report(self) -> Dict[str, Any]:
        """Generate performance report"""
        df_times = pd.DataFrame(self.metrics["response_times"])
        return {
            "avg_response_time": df_times["duration"].mean() if not df_times.empty else 0,
            "error_rate": len(self.metrics["error_rates"]) / max(1, len(self.metrics["response_times"])),
            "mode_distribution": self.metrics["mode_usage"]
        }
