from fastapi import FastAPI
from pydantic import BaseModel
from refiner import generate_llm_response

app = FastAPI()

class GenerateRequest(BaseModel):
    text: str
    model: str = "gpt-4o-mini"  # Default model
    prompt: str = '''Refine the following text without altering my writing style. Correct grammar mistakes and keep the writing concise and clear. I should immediately recognize it as my own work, but with essential improvements. Text: {} '''

@app.post("/generate")
# run with curl -s -X POST "http://localhost:8000/generate" -H "Content-Type: application/json" -d '{"text": "my custom input textt", "model": "gpt-4o-mini"}'
def generate_text(request: GenerateRequest):
    return generate_llm_response(request.prompt.format(request.text), request.model)
