import os
from dotenv import load_dotenv
load_dotenv('./.env')


TOKEN = os.environ.get('TOKEN')
ADMINS = os.environ.get('ADMINS')
SUPER_ADMINS = os.environ.get('SUPER_ADMINS')


