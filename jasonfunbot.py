import os
from dotenv import load_dotenv

from bully import bully

bully.test()

load_dotenv()

token = os.getenv("BOT_TOKEN")

print(token)