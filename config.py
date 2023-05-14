from dotenv import load_dotenv
import os


load_dotenv()
FILEPATH = os.environ.get('FILEPATH')
RESULT_FILEPATH = os.environ.get('RESULT_FILEPATH')
SL_DB_NAME = os.environ.get('SL_DB_NAME')
