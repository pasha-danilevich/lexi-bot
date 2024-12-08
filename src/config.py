from dotenv import load_dotenv
import os

load_dotenv(override=True)

TG_TOKEN = os.getenv("TG_TOKEN", '')
HOST = os.getenv("HOST", '')

