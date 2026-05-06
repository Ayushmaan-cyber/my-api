from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///storage/api_keys.db")
KEY_PREFIX   = os.getenv("KEY_PREFIX", "sk-")
APP_SECRET   = os.getenv("APP_SECRET", "changeme")
ADMIN_TOKEN  = os.getenv("ADMIN_TOKEN", "admin-secret-token")
