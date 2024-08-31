from fastapi import FastAPI
from pydantic import BaseModel
from refiner import generate_llm_response

# activate by running
# uvicorn api:app --host 0.0.0.0 --port 8000

app = FastAPI()

class GenerateRequest(BaseModel):
    text: str
    model: str = "gpt-4o-mini"  # Default model
    prompt: str = '''Refine the following text without altering my writing style. Correct grammar mistakes and keep the writing concise and clear. I should immediately recognize it as my own work, but with essential improvements. Text: {} '''

# run with curl -s -X POST "http://localhost:8000/generate_post" -H "Content-Type: application/json" -d '{"text": "my custom input textt", "model": "gpt-4o-mini"}'
@app.post("/generate_post")
def generate_text(request: GenerateRequest):
    return generate_llm_response(request.prompt.format(request.text), request.model)

# run with curl -s "http://localhost:8000/generate_get?text=${encoded_text}&model=gpt-4o-mini"
@app.get("/generate_get")
def generate_text(text: str, model: str = "gpt-4o-mini", prompt: str = '''Refine the following text without altering my writing style. Correct grammar mistakes and keep the writing concise and clear. I should immediately recognize it as my own work, but with essential improvements. Text: {} '''):
    return generate_llm_response(prompt.format(text), model)
