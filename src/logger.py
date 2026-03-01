import logging

# Errors
logger_errors = logging.getLogger("api_error")
logger_errors.setLevel(logging.ERROR)

file_log_errors = logging.FileHandler("src/log/baseline_errors.log")
file_log_errors.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

logger_errors.addHandler(file_log_errors)

# Critical
logger_critical = logging.getLogger("db_critical")
logger_critical.setLevel(logging.CRITICAL)

file_log_critical = logging.FileHandler("src/log/baseline_critical.log")
file_log_critical.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

logger_critical.addHandler(file_log_critical)
