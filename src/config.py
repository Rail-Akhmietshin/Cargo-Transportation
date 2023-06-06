from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.environ.get("POSTGRES_DB")

DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")

DB_HOST = os.environ.get("POSTGRES_HOST")
DB_PORT = os.environ.get("POSTGRES_PORT", 5678)

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", 5377)

broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}"
result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}"

timezone = 'Europe/Moscow'
enable_utc = True

imports = ('src.transportation.tasks',)
