import os

from dotenv import load_dotenv


load_dotenv(override=True)

TG_TOKEN = os.getenv("TG_TOKEN", "")
DOMAIN = os.getenv("DOMAIN", "")
