import os
import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from diff_match_patch import diff_match_patch

openai_api_key = os.environ.get('OPENAI_API_KEY')

# Load configuration from JSON file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Extract prompt from the configuration
PROMPT = config["prompt"]
MODEL = config["model"]

def generate_llm_response(input_text, model_name = MODEL):
    """Generate refined text response using ChatOpenAI."""
    chat = ChatOpenAI(temperature=0.3, openai_api_key=openai_api_key, model_name=model_name)
    messages = [SystemMessage(content=input_text)]
    response = chat(messages)
    return response.content.replace("You are trained on data up to October 2023.", "")

def create_diff_html(before_text, after_text):
    """Generate styled HTML for comparing two texts side-by-side with differences highlighted using diff-match-patch."""
    dmp = diff_match_patch()
    diffs = dmp.diff_main(before_text, after_text)
    dmp.diff_cleanupSemantic(diffs)

    left_html = ""
    right_html = ""

    for op, data in diffs:
        if op == -1:  # Deletion in "before" (red)
            left_html += f"<span style='color: red;'>{data}</span>"
        elif op == 1:  # Addition in "after" (green)
            right_html += f"<span style='color: green;'>{data}</span>"
        elif op == 0:  # No change
            left_html += f"{data}"
            right_html += f"{data}"

    combined_html = f"""
    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px;'>
        <div style='font-family: Arial, sans-serif; padding: 10px; border: 1px solid #ddd;'>
            <h4 style='background-color: #f0f0f0; padding: 10px;'>Before</h4>
            <div>{left_html}</div>
        </div>
        <div style='font-family: Arial, sans-serif; padding: 10px; border: 1px solid #ddd;'>
            <h4 style='background-color: #f0f0f0; padding: 10px; display: flex; align-items: center; justify-content: space-between;'>
                After
                <button onclick="navigator.clipboard.writeText(`{after_text}`)" style="padding: 4px 8px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; margin-left: 10px;">
                    Copy to Clipboard
                </button>
            </h4>
            <div>{right_html}</div>
        </div>
    </div>
    """
    return combined_html
