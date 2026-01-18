from openai import OpenAI
from dotenv import load_dotenv
import os
import logging
logger = logging.getLogger(__name__)

load_dotenv()

api_key = os.getenv("OPENAI_KEY")

client = OpenAI(api_key=api_key)

def moderation_check(serializer):
    data = serializer.validated_data
    description = data["description"] if data.get("description") else ""
    content = data["title"] + " | " + ", ".join(data["options"]) + " | " + description
    try:
        response = client.moderations.create(
            model="omni-moderation-latest",
            input=content
        )
        return response.results[0].flagged
    except Exception as e:
        logger.exception("OpenAI automoderation failed.")
        return True
