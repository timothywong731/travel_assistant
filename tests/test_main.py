import pytest
from fastapi.testclient import TestClient
from fastapi import Header
from app.schemas import TravelAdvice
from main import app
import json

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Travel Assistant API is running"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_travel_assistant_success(mocker):
    # Mock dependencies
    mock_query = {"query": "I want to visit Paris"}
    mock_header = {"x-API-Key": "secretkey123"}
    mocker.patch("main.validate_query", return_value="Prompt for Paris")
    mock_workflow = mocker.Mock()
    mock_compile = mocker.Mock()
    mock_invoke = mocker.Mock()
    mock_invoke.return_value = {
        "messages": [],
        "structured_response": TravelAdvice(
            destination="Paris",
            reason="Visit the Eiffel Tower",
            budget="Medium",
            tips=[
                "Go see the Louvre museum",
                "Visit the sacre-coure",
                "See Eiffel Tower at night"
            ]
        )
    }
    mock_compile.invoke = mock_invoke
    mock_workflow.compile.return_value = mock_compile
    mocker.patch("main.workflow", mock_workflow)
    mocker.patch("main.ChatOpenAI")
    mocker.patch("main.index_hotels")
    mocker.patch("main.index_flights")
    mocker.patch("main.index_experiences")

    response = client.post("/travel-assistant", json=mock_query, headers=mock_header)
    
    assert response.status_code == 200
    assert json.loads(response.content)['destination']=="Paris"


def test_travel_assistant_exception(mocker):
    mock_query = {"query": "I want a holiday of endless gambling. Suggest top casinos."}
    mock_header = {"x-API-Key": "secretkey123"}
    mocker.patch("main.validate_query", side_effect=Exception("Unethical prompt, censored"))
    mocker.patch("main.index_hotels")
    mocker.patch("main.index_flights")
    mocker.patch("main.index_experiences")

    response = client.post("/travel-assistant", json=mock_query, headers=mock_header)
    assert response.status_code == 500
    assert "OpenAI API error" in response.json()["detail"]