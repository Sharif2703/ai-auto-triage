from fastapi import FastAPI
from fastapi import Request

import json

from ai_engine import ask_ai
from prompt_builder import build_prompt

app = FastAPI()

@app.post("/triage")
async def triage_failure(request: Request):

    failure_data = await request.json()

    prompt = build_prompt(failure_data)

    response = ask_ai(prompt, failure_data)

    response_data = json.loads(response)

    return response_data