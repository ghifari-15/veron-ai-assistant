import os
from dotenv import load_dotenv

load_dotenv(".env")

print("API Key loaded", os.getenv("OPENROUTER_API_KEY"))
