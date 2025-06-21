import logging
from datetime import datetime
from pathlib import Path

class ErrorLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging system"""
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_dir / 'ai_errors.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('AIErrorLogger')

    def log_error(self, error: Exception, context: dict = None):
        """Log an error with context"""
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "message": str(error),
            "context": context or {}
        }
        self.logger.error(error_info)
