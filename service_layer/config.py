import os

from dotenv import load_dotenv


def get_postgres_uri():
    db_uri = os.environ.get("DB_URI")
    return db_uri


def get_api_url():
    api_url = os.environ.get("API_URL", "http://localhost:5005")
    return api_url