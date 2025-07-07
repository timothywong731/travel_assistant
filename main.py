from fastapi import FastAPI, HTTPException
from app.schemas import TravelQuery, TravelAdvice, HotelRecommendation, FlightRecommendation, ExperienceRecommendation
from app.prompt import generate_prompt, HOTEL_LOOKUP_AGENT_PROMPT, FLIGHT_LOOKUP_AGENT_PROMPT, EXPERIENCE_LOOKUP_AGENT_PROMPT, SUPERVISOR_AGENT_PROMPT
from app.data import search_hotels, search_flights, search_flights_by_month, search_experiences, index_hotels, index_flights, index_experiences
from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentStateWithStructuredResponse
import os
from dotenv import load_dotenv


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
        
        hotel_lookup_agent = create_react_agent(
            model=model,
            name="hotel_lookup_agent",
            tools=[search_hotels],
            prompt=HOTEL_LOOKUP_AGENT_PROMPT,
            state_schema=AgentStateWithStructuredResponse,
            response_format=HotelRecommendation
        )

        flight_lookup_agent = create_react_agent(
            model=model,
            name="flight_lookup_agent",
            tools=[search_flights, search_flights_by_month],
            prompt=FLIGHT_LOOKUP_AGENT_PROMPT,
            state_schema=AgentStateWithStructuredResponse,
            response_format=FlightRecommendation
        )

        experience_lookup_agent = create_react_agent(
            model=model,
            name="experience_lookup_agent",
            tools=[search_experiences],
            prompt=EXPERIENCE_LOOKUP_AGENT_PROMPT,
            state_schema=AgentStateWithStructuredResponse,
            response_format=ExperienceRecommendation
        )

        # Create supervisor workflow
        workflow = create_supervisor(
            [hotel_lookup_agent, flight_lookup_agent, experience_lookup_agent],
            model=model,
            prompt=SUPERVISOR_AGENT_PROMPT,
            state_schema=AgentStateWithStructuredResponse,
            response_format=TravelAdvice
        )
        
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
