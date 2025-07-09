from typing import List
from fastapi import FastAPI, HTTPException
from app.schemas import TravelQuery, TravelAdvice
from app.prompt import validate_query
from app.tools import index_hotels, index_flights, index_experiences
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from app.agents import workflow
from fastapi import Header

# Load environment variables from .env file
load_dotenv()

index_hotels()
index_flights()
index_experiences()

app = FastAPI()

# Initialize OpenAI client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def getAllowedApiKey() -> List[str]:
    return [
        "secretkey123",
        "secretkey456",
        "secretkey789",
    ]


@app.post("/travel-assistant", response_model=TravelAdvice)
def travel_assistant(
    query: TravelQuery,
    x_api_key: str = Header(None, alias="x-API-Key")
):
    # Check API key
    expected_api_key = getAllowedApiKey()
    
    if not expected_api_key or x_api_key not in expected_api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    try:
        print(f"🔍 Received query: {query.query}")
        
        model = ChatOpenAI(model="gpt-4o", output_version="responses/v1")

        # In production, use key vault to store server-side secrets.
        api_key = os.getenv("OPENAI_API_KEY")
        print(f"🔑 Using API key: {api_key[:10]}..." if api_key else "❌ No API key")

        # Checks for prompt injection and sanitises the query
        prompt = validate_query(query.query)

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
