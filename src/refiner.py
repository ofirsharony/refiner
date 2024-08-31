import os
import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage

openai_api_key = os.environ.get('OPENAI_API_KEY')

# Load configuration from JSON file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Extract prompt from the configuration
PROMPT = config["prompt"]
MODEL = config["model"]

def refine(input_text, model_name = MODEL):
    """Generate refined text response using ChatOpenAI."""
    chat = ChatOpenAI(temperature=0.3, openai_api_key=openai_api_key, model_name=model_name)
    messages = [SystemMessage(content=input_text)]
    response = chat(messages)

    # looks like a bug, probably a newer API version will resolve it. TODO fix this
    return response.content.replace("You are trained on data up to October 2023.", "")

