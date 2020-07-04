import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(dotenv_path=join(dirname(__file__), '.env'))

TBB_DB = {
    'user': os.environ.get('DBUSER'),
    'pwd': os.environ.get('PASSWORD'),
    'host': os.environ.get('HOST'),
    'port': os.environ.get('PORT'),
    'db_name': os.environ.get('DB')
}
