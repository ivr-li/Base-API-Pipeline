import time

from src.baseline import baseline
from src.config import config
from src.database import DATABASE

DATABASE.create_table()

if __name__ == "__main__":
    while True:
        baseline()
        time.sleep(config.REQUEST_INTERVAL)
