# from fastapi import FastAPI
# from pydantic import BaseModel
# from stable_diffusion_cpp import StableDiffusion
# from PIL import Image
# import base64
# from io import BytesIO

# app = FastAPI()

# # Load model once (IMPORTANT)
# MODEL_PATH = r"D:\Local_Models\stable-diffusion-xl-1.0-turbo-Q8_0.gguf"

# sd = StableDiffusion(
#     model_path=MODEL_PATH,
#     n_threads=6,        # adjust based on CPU
#     wtype="q8_0",       # matches your model
# )

# class PromptRequest(BaseModel):
#     prompt: str


# def image_to_base64(img: Image.Image):
#     buffer = BytesIO()
#     img.save(buffer, format="PNG")
#     return base64.b64encode(buffer.getvalue()).decode()


# @app.post("/generate")
# def generate_image(req: PromptRequest):
#     try:
#         result = sd.txt_to_img(
#             prompt=req.prompt,
#             width=512,
#             height=512,
#             steps=4,              # turbo → low steps
#             cfg_scale=1.0
#         )

#         image = result[0]  # first image
#         img_base64 = image_to_base64(image)

#         return {
#             "status": "success",
#             "image_base64": img_base64
#         }

#     except Exception as e:
#         return {"error": str(e)}

from llama_cpp import Llama
import re
import requests
import random, string

llm = Llama(
    model_path=r"D:/Local_Models/meta-llama-3-8b-instruct.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=6
)

# Tools 

def get_current_time():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate(expr):
    return str(eval(expr))

def get_system_info():
    import platform
    return platform.system()

def get_temperature(city="Mumbai"):
    API_KEY = "ba6bbe916a33ccc76ed836931ff3842a"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        print(data,'irufieirrii3iri32fjejf9eif')

        if response.status_code != 200:
            return f"Error: {data.get('message')}"

        temp = data["main"]["temp"]
        return f"Temperature in {city} is {temp}°C"

    except:
        return "Unable to fetch temperature"

def generate_password():
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(10))


def handle_tools(prompt: str):
    prompt_lower = prompt.lower()

    if "time" in prompt_lower:
        return get_current_time()

    elif "calculate" in prompt_lower:
        expr = prompt_lower.replace("calculate", "").strip()
        # return calculate(expr)
     
     # remove unwanted words
        expr = re.sub(r"[^0-9+\-*/().% ]", "", expr)

        if not expr:
            return "Please provide a valid expression"

        return calculate(expr)

    elif "system" in prompt_lower:
        return get_system_info()

    elif "temperature" in prompt_lower or "weather" in prompt_lower:
    # Extract city after 'in'
        match = re.search(r"in ([a-zA-Z ]+)", prompt_lower)

        if match:
            city = match.group(1).strip()
        else:
            city = "Mumbai"  # default

        return get_temperature(city)
    
    
    elif "password" in prompt_lower:
        return generate_password()

    return None


from fastapi import FastAPI

app = FastAPI()

@app.get("/chat")
def chat(query: str):

    # Step 1: Try tools
    tool_result = handle_tools(query)
    if tool_result:
        return {"response": tool_result}

    # Step 2: Otherwise use LLM
    output = llm(
        f"User: {query}\nAssistant:",
        max_tokens=200
    )

    return {"response": output["choices"][0]["text"]}