import os
from dotenv import load_dotenv
import json

load_dotenv()

def parseEnvFile(itemName):
    itemSecret = os.getenv(str(itemName))

    if itemSecret:
        try:
            jsonFormat = json.loads(itemSecret)
            return jsonFormat

        except:
            return itemSecret
    else:
        return itemSecret

