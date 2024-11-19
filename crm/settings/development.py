from .base import *
import os
from dotenv import load_dotenv

load_dotenv()

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# SQLite
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "media/"
STATIC_URL = "/static/"
