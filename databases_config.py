import os
from pathlib import Path
import dotenv

dotenv.load_dotenv(Path('.env'))

db_read = {
    'host': os.environ.get("host_read"),
    'user': os.environ.get("user_read"),
    'password': os.environ.get("password_read"),
    'database' : os.environ.get("database_read")
}

db_save = {
'host': os.environ.get("host_write"),
    'user': os.environ.get("user_write"),
    'password': os.environ.get("password_write"),
    'database' : os.environ.get("database_write")


}

