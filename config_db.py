from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.environ.get("DB_NAME", "casting")
DB_USER = os.environ.get("DB_USER", "quyetcv1")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "abc")
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1:5432')

SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_NAME
)

SQLALCHEMY_TRACK_MODIFICATIONS = False