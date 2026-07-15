from google.adk.agents.llm_agent import Agent
from datetime import datetime
import requests
import platform


# Tool function
def get_current_time():
    """Returns current system time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")



def get_temperature(city: str = "Mumbai"):
    """Get current temperature of a given city (default Mumbai)"""
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return f"❌ Error fetching weather for {city}"

        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]

        return f"Temperature in {city}: {temp}°C, Condition: {weather}"
    
    except Exception as e:
        return f"❌ Error: {str(e)}"
    
def calculate(expression: str):
    """Evaluate math expression"""
    try:
        return str(eval(expression))
    except:
        return "Invalid calculation"
    
def get_system_info():
    """Get system details"""
    return platform.system()


root_agent = Agent(
    model='D:\Local_Models\stable-diffusion-xl-1.0-turbo-Q8_0.gguf',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction="""
    You are a smart assistant.
    Use tools when needed:
    - time → get_current_time
    - math → calculate
    - website → fetch_website
    - system → get_system_info
    """,
    tools=[get_current_time, get_temperature, calculate, get_system_info]   # ✅ important
)
