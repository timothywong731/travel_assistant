from fastapi import FastAPI, HTTPException
from app.schemas import TravelQuery, TravelAdvice
from app.prompt import generate_prompt
from app.tools import index_hotels, index_flights, index_experiences
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from app.agents import workflow

# Load environment variables from .env file
load_dotenv()

index_hotels()
index_flights()
index_experiences()

app = FastAPI()

# Initialize OpenAI client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/travel-assistant", response_model=TravelAdvice)
def travel_assistant(query: TravelQuery):
    try:
        print(f"🔍 Received query: {query.query}")
        
        model = ChatOpenAI(model="gpt-4o", output_version="responses/v1")
        api_key = os.getenv("OPENAI_API_KEY")
        print(f"🔑 Using API key: {api_key[:10]}..." if api_key else "❌ No API key")


        prompt = generate_prompt(query.query)

        app = workflow.compile()

        result = app.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })

        travel_advice = result['structured_response']

        return travel_advice
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Travel Assistant API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
