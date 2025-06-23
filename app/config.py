import json
from dotenv import load_dotenv
import os

CONFIG_PATH = "settings.json"
with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)
    load_dotenv(".env")
    config["secret_key"] = os.getenv("SECRET_KEY")

SQL_DATA = {
    "db_path": config["sqlite_database"],
    "users_table_name": config["users_sql_table"],
}

TEMPLATES_DIRECTORY: str = config["templates_directory"]
LOGS_DIRECTORY = config["logs_directory"]
SECRET_KEY = config["secret_key"]