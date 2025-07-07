from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentStateWithStructuredResponse
from app.prompt import HOTEL_LOOKUP_AGENT_PROMPT, FLIGHT_LOOKUP_AGENT_PROMPT, EXPERIENCE_LOOKUP_AGENT_PROMPT, SUPERVISOR_AGENT_PROMPT
from app.data import search_hotels, search_flights, search_flights_by_month, search_experiences
from app.schemas import TravelAdvice, HotelRecommendation, FlightRecommendation, ExperienceRecommendation

model = ChatOpenAI(model="gpt-4o", output_version="responses/v1")

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