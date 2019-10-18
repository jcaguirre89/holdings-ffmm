from backend.settings.common import *

db_path = BASE_DIR / 'db.sqlite3'

DATABASES = {
    "default": dj_database_url.parse(f'sqlite:///{db_path}', conn_max_age=600)
}

ENVIRONMENT = os.getenv("DJANGO_ENVIRONMENT", "development")
print(ENVIRONMENT)
