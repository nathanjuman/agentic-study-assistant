import logging
import structlog
from logging.handlers import RotatingFileHandler

from settings import Settings


def configure_logging(settings: Settings) -> None:
    """
    Central logging setup function.

    Converts 'INFO' or 'DEBUG' into logging constant.
    Enables console logging and grabs root logger so
    handlers can be attached globally.
    'app_handler' writes activity logs to logs/app.log.
    'error_handler' writes error logs to logs/error.log.
    Avoids attaching duplicate file handlers if logging gets
    configured twice.
    """
    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    logging.basicConfig(level=level, format="%(message)s")
    root_logger = logging.getLogger()

    app_handler = RotatingFileHandler(
        settings.logs_dir / "app.log",
        maxBytes=1_000_000, # Rotates logs to
        backupCount=3,      # rollover at length threshold
        encoding="utf-8",
    )
    app_handler.setLevel(level)
    app_handler.setFormatter(logging.Formatter("%(message)s"))

    error_handler = RotatingFileHandler(
        settings.logs_dir / "error.log",
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter("%(message)s"))

    if not any(getattr(handler, "baseFilename", "").endswith("app.log") for handler in root_logger.handlers):
        root_logger.addHandler(app_handler)
    if not any(getattr(handler, "baseFilename", "").endswith("error.log") for handler in root_logger.handlers):
        root_logger.addHandler(error_handler)

    # Configure global default wrapper
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
    )
