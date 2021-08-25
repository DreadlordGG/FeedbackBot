import os
from dotenv import load_dotenv
class Config:
    def __init__(self):
        self.env = load_dotenv()

    def __getattr__(self, attr):
        value = os.getenv(attr)
        if value == "":
            return None
        return value
