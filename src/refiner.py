import os
import json
import ssl

import httpx
from pathlib import Path
from openai import OpenAI

# Load config next to this file, so the app works from any working directory.
CONFIG_PATH = Path(__file__).with_name("config.json")
config = json.loads(CONFIG_PATH.read_text())

PROMPT = config["prompt"]
MODEL = config["model"]
MODELS = config.get("models", [MODEL])
# Any OpenAI-compatible endpoint works. Change these two keys to switch provider.
BASE_URL = config.get("base_url", "https://api.openai.com/v1")
API_KEY_ENV = config.get("api_key_env", "OPENAI_API_KEY")

# Some models add this sentence to the answer. Remove it.
NOISE = "You are trained on data up to October 2023."


def is_reasoning_model(model_name):
    """Reasoning models (gpt-5*, o*) reject temperature/top_p and need a low reasoning effort to be fast."""
    name = model_name.split("/")[-1]
    return name.startswith("gpt-5") or (name.startswith("o") and name[1:2].isdigit())


def reasoning_effort(model_name):
    """Lowest effort per model: the gpt-5 family accepts "minimal"; gpt-5.1 and later accept "none"."""
    name = model_name.split("/")[-1]
    return "minimal" if name.startswith("gpt-5-") or name == "gpt-5" else "none"


def build_request(input_text, model_name):
    """Return the kwargs for chat.completions.create()."""
    request = {
        "model": model_name,
        "messages": [{"role": "user", "content": input_text}],
        "max_completion_tokens": 4096,
    }
    if is_reasoning_model(model_name):
        request["reasoning_effort"] = reasoning_effort(model_name)
    else:
        request["temperature"] = 0.5
        request["top_p"] = 1
    return request


def get_client():
    api_key = os.environ.get(API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"Set {API_KEY_ENV} to your API key.")
    return OpenAI(base_url=BASE_URL, api_key=api_key, http_client=httpx.Client(verify=ssl_context()))


def ssl_context():
    """Verify certs as usual, but without Python 3.13's strict X.509 mode: corporate proxy CAs (Zscaler) fail it."""
    context = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE"))
    context.verify_flags &= ~ssl.VERIFY_X509_STRICT
    return context


def refine(input_text, model_name=MODEL, client=None):
    """Send the full prompt (instructions + text) to the model and return the refined text."""
    client = client or get_client()
    print(f"calling {model_name} with: {input_text}\n")

    response = client.chat.completions.create(**build_request(input_text, model_name))

    content = response.choices[0].message.content
    if content is None:
        raise RuntimeError(f"{model_name} returned an empty response")
    print("Response: ", content)
    return content.replace(NOISE, "").strip()
