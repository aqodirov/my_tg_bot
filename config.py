import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
TOKEN = os.getenv("TOKEN")
OpenAI_KEY = os.getenv("OPENAI_KEY")