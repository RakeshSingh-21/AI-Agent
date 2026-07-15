from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import platform

from llama_cpp import Llama

# -----------------------------
# Load Local Model
# -----------------------------
llm = Llama(
    model_path="D:\\Local_Models\\mistral.gguf",
    n_ctx=2048
)

# -----------------------------
# Tools
# -----------------------------
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate(expression: str):
    try:
        return str(eval(expression))
    except:
        return "Invalid calculation"

def get_system_info():
    return platform.system()

# -----------------------------
# Simple Agent Logic
# -----------------------------
def agent_response(user_input: str):
    
    # Tool routing (basic)
    if "time" in user_input.lower():
        return get_current_time()
    
    if "calculate" in user_input.lower() or any(x in user_input for x in "+-*/"):
        return calculate(user_input)
    
    if "system" in user_input.lower():
        return get_system_info()

    # Default → LLM
    response = llm(
        user_input,
        max_tokens=200,
        temperature=0.7
    )
    
    return response["choices"][0]["text"]

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_agent(query: Query):
    answer = agent_response(query.question)
    return {"response": answer}