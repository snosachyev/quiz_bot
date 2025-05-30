import logging

logger = logging.getLogger(__name__)

formatter = logging.Formatter(
    fmt="%(levelname)s %(name)s - %(asctime)s - %(message)s"
)

file_handler = logging.FileHandler("loger.log")
file_handler.setFormatter(formatter)

logger.handlers = [file_handler]

logger.setLevel(logging.INFO)
