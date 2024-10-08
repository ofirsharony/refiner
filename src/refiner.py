import os
import json
from langchain_openai import ChatOpenAI
openai_api_key = os.environ.get('OPENAI_API_KEY')

# Load configuration from JSON file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Extract prompt from the configuration
PROMPT = config["prompt"]
MODEL = config["model"]

def refine(input_text, model_name = MODEL):
    """Generate refined text response using ChatOpenAI."""
    llm = ChatOpenAI(temperature=0.3, openai_api_key=openai_api_key, model_name=model_name)

    messages = [
        ( "system", input_text)
        # , ("human", "some prompt")
    ]

    print (f"calling {model_name} with: {input_text}")
    response = llm.invoke(messages).content
    print ("response: ", response)
    return response.replace("You are trained on data up to October 2023.", "")
