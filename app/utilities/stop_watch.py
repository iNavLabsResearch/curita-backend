"""
Stop Watch

Performance timing utility for measuring execution time.
"""

import time
from typing import Optional, Dict, Any
from contextlib import contextmanager

from app.telemetries.logger import logger


class StopWatch:
    """
    Utility for measuring execution time
    """
    
    def __init__(self, name: str = "Operation", auto_log: bool = True):
        """
        Initialize stopwatch
        
        Args:
            name: Name of the operation being timed
            auto_log: Whether to auto-log on stop
        """
        self.name = name
        self.auto_log = auto_log
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.lap_times: list[tuple[str, float]] = []
    
    def start(self) -> "StopWatch":
        """
        Start the stopwatch
        
        Returns:
            Self for chaining
        """
        self.start_time = time.time()
        self.lap_times = []
        logger.debug(f"⏱️  Started: {self.name}")
        return self
    
    def stop(self) -> float:
        """
        Stop the stopwatch
        
        Returns:
            Elapsed time in seconds
        """
        if self.start_time is None:
            logger.warning("StopWatch was never started")
            return 0.0
        
        self.end_time = time.time()
        elapsed = self.elapsed()
        
        if self.auto_log:
            logger.info(f"⏱️  Completed: {self.name} in {elapsed:.4f}s")
        
        return elapsed
    
    def lap(self, label: str = "Lap") -> float:
        """
        Record a lap time
        
        Args:
            label: Label for this lap
            
        Returns:
            Time since start
        """
        if self.start_time is None:
            logger.warning("StopWatch was never started")
            return 0.0
        
        lap_time = time.time() - self.start_time
        self.lap_times.append((label, lap_time))
        
        if self.auto_log:
            logger.debug(f"⏱️  {self.name} - {label}: {lap_time:.4f}s")
        
        return lap_time
    
    def elapsed(self) -> float:
        """
        Get elapsed time
        
        Returns:
            Elapsed time in seconds
        """
        if self.start_time is None:
            return 0.0
        
        end = self.end_time if self.end_time is not None else time.time()
        return end - self.start_time
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get timing statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            "name": self.name,
            "total_time": self.elapsed(),
            "lap_times": self.lap_times,
            "laps_count": len(self.lap_times)
        }
    
    def reset(self) -> None:
        """Reset the stopwatch"""
        self.start_time = None
        self.end_time = None
        self.lap_times = []


@contextmanager
def measure_time(operation_name: str, auto_log: bool = True):
    """
    Context manager for measuring execution time
    
    Args:
        operation_name: Name of the operation
        auto_log: Whether to auto-log results
        
    Yields:
        StopWatch instance
        
    Example:
        with measure_time("Database Query") as sw:
            # do something
            sw.lap("Fetched data")
            # do more
    """
    stopwatch = StopWatch(name=operation_name, auto_log=auto_log)
    stopwatch.start()
    
    try:
        yield stopwatch
    finally:
        stopwatch.stop()
