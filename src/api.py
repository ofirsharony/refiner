from fastapi import FastAPI
from pydantic import BaseModel
from refiner import refine, PROMPT, MODEL

# Start with: uvicorn api:app --host 0.0.0.0 --port 8005 --reload &
# Port 8005 matches Automations/replace_in_place.sh.

app = FastAPI()


class GenerateRequest(BaseModel):
    text: str
    model: str = MODEL
    prompt: str = PROMPT


# curl -s -X POST "http://localhost:8005/generate_post" -H "Content-Type: application/json" -d '{"text": "my text"}'
@app.post("/generate_post")
def generate_post(request: GenerateRequest):
    return refine(request.prompt.format(request.text), request.model)


# curl -s "http://localhost:8005/generate_get?text=${encoded_text}"
@app.get("/generate_get")
def generate_get(text: str, model: str = MODEL, prompt: str = PROMPT):
    return refine(prompt.format(text), model)
