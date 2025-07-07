from app.agents import hotel_lookup_agent, flight_lookup_agent, experience_lookup_agent
from langgraph.graph.state import CompiledStateGraph

def test_hotel_lookup_agent():
    assert hotel_lookup_agent.name == "hotel_lookup_agent", "Hotel lookup agent should have the correct name"
    assert isinstance(hotel_lookup_agent, CompiledStateGraph), "Should be an agent"


def test_flight_lookup_agent():
    assert flight_lookup_agent.name == "flight_lookup_agent", "Flight lookup agent should have the correct name"
    assert isinstance(flight_lookup_agent, CompiledStateGraph), "Should be an agent"


def test_experience_lookup_agent():
    assert experience_lookup_agent.name == "experience_lookup_agent", "Experience lookup agent should have the correct name"
    assert isinstance(experience_lookup_agent, CompiledStateGraph), "Should be an agent"