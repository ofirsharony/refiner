from fastapi import FastAPI
from pydantic import BaseModel
from refiner import refine, PROMPT

# Run the below to start an event loop that handles incoming HTTP requests asynchronously, where 'api' is the python file and 'app' is the FastAPI instance that will handle requests
# uvicorn api:app --host 0.0.0.0 --port 8000 --reload &

app = FastAPI()

class GenerateRequest(BaseModel):
    text: str
    model: str = "gpt-4o-mini"  # Default model
    prompt: str = PROMPT

# run with curl -s -X POST "http://localhost:8000/generate_post" -H "Content-Type: application/json" -d '{"text": "my custom input text", "model": "gpt-4o-mini"}'
@app.post("/generate_post")
def generate_text(request: GenerateRequest):
    return refine(request.prompt.format(request.text), request.model)

# run with curl -s "http://localhost:8000/generate_get?text=${encoded_text}&model=gpt-4o-mini"
@app.get("/generate_get")
def generate_text(text: str, model: str = "gpt-4o-mini", prompt: str = PROMPT):
    return refine(prompt.format(text), model)
