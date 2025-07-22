import os
import json
from openai import OpenAI

# To authenticate with the model you will need to generate a fined grained personal access token (PAT) in your GitHub settings, with "models read" permission
# Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
github_token = os.environ.get('GITHUB_TOKEN_PERSONAL')

# Load configuration from JSON file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Extract prompt from the configuration
PROMPT = config["prompt"]
MODEL = config["model"]

def refine(input_text, model_name = MODEL):
    """Generate refined text response using GitHub Models."""
    client = OpenAI(
        base_url="https://models.github.ai/inference",
        api_key=github_token,
    )

    print (f"calling {model_name} with: {input_text}\n")
    
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": input_text,
            }
        ],
        model=model_name,
        temperature=0.3,
        max_tokens=4096,
        top_p=1
    )
    
    response_content = response.choices[0].message.content
    print ("Response: ", response_content)
    return response_content.replace("You are trained on data up to October 2023.", "")
