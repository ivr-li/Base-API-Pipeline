import time

from src.baseline import baseline
from src.config import config
from src.database import DB

db = DB()
db.create_table()

if __name__ == "__main__":
    while True:
        baseline(db)
        time.sleep(config.REQUEST_INTERVAL)
