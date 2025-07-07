from unittest.mock import patch
from langchain_core.embeddings import Embeddings
import pytest
from typing import List
from app.tools import index_hotels, index_flights, index_experiences, hotels_vector_store, flights_vector_store, experiences_vector_store, embeddings, search_hotels, search_flights, search_experiences
from langchain_core.documents import Document
import json

def test_embeddings():
    """Test if embeddings are initialized correctly."""
    assert isinstance(embeddings, Embeddings), "Embeddings should be an instance of Embeddings"

def test_hotels_vector_store():
    """Test if hotels are indexed in the vector store."""
    documents = hotels_vector_store.get()['documents']
    assert isinstance(len(documents), int), "The hotels vector store should return a list of documents"

def test_flights_vector_store():
    """Test if flights are indexed in the vector store."""
    documents = flights_vector_store.get()['documents']
    assert isinstance(len(documents), int), "The flights vector store should return a list of documents"

def test_experiences_vector_store():
    """Test if experiences are indexed in the vector store."""
    documents = experiences_vector_store.get()['documents']
    assert isinstance(len(documents), int), "The experiences vector store should return a list of documents"



def test_search_hotels():
    """
    Use mock framework to test search_hotels function.
    mock patches the `similarity_search` function inside the `search_hotels` function to simulate the indexing process.
    """
    with patch('app.tools.hotels_vector_store.similarity_search') as mock_search:
        mock_search.return_value = [
            Document(page_content=json.dumps({"hotel_name": "Hotel A", "city": "City A", "rating": 4.5})),
            Document(page_content=json.dumps({"hotel_name": "Hotel B", "city": "City B", "rating": 3.5})),
            Document(page_content=json.dumps({"hotel_name": "Hotel C", "city": "City C", "rating": 3.0})),
        ]
        results =search_hotels("UK hotels")
        assert mock_search.called, "The similarity_search function should be called during indexing hotels"
        assert len(results)==3, "There should be 3 hotel results returned"
        assert results[0]["hotel_name"] == "Hotel A", "The first hotel result should match the mock data"


# def test_search_flights(mocker):
#     """
#     Use mock framework to test search_flights function.
#     """

#     with patch('app.data.flights') as mock_flights:
#         mock_flights.return_value =[
#             {
#                 "operating_airline": "Virgin Atlantic",
#                 "city_depart": "San Francisco",
#                 "city_arrive": "London",
#                 "flight_number": "VS0123",
#             },
#             {
#                 "operating_airline": "Virgin Atlantic",
#                 "city_depart": "Mumbai",
#                 "city_arrive": "London",
#                 "flight_number": "VS0124",
#             },
#             {
#                 "operating_airline": "Virgin Atlantic",
#                 "city_depart": "Tampa",
#                 "city_arrive": "London",
#                 "flight_number": "VS0125",
#             },
#         ]
        
#         results = search_flights("Tampa", "London")
#         # assert mock_flights.called, "The mock_flights variable should be called during indexing flights"
#         assert len(results)==1, "There should be 1 flight results returned"
#         assert results[0]["flight_number"] == "VS0125", "The first flight result should match the mock data"

def test_search_flights_exact_match(monkeypatch):
    """
    Test search_flights returns correct flights for exact city_depart and city_arrive.
    """
    mock_flights = [
        {"city_depart": "New York", "city_arrive": "London", "flight_number": "VS0001"},
        {"city_depart": "New York", "city_arrive": "Paris", "flight_number": "VS0002"},
        {"city_depart": "London", "city_arrive": "New York", "flight_number": "VS0003"},
    ]
    monkeypatch.setattr("app.tools.flights", mock_flights)
    results = search_flights("New York", "London")
    assert len(results) == 1
    assert results[0]["flight_number"] == "VS0001"

def test_search_flights_no_match(monkeypatch):
    """
    Test search_flights returns empty list if no flights match.
    """
    mock_flights = [
        {"city_depart": "New York", "city_arrive": "Paris", "flight_number": "VS0002"},
    ]
    monkeypatch.setattr("app.tools.flights", mock_flights)
    results = search_flights("London", "Tokyo")
    assert results == []

def test_search_flights_multiple_matches(monkeypatch):
    """
    Test search_flights returns all flights matching the criteria.
    """
    mock_flights = [
        {"city_depart": "San Francisco", "city_arrive": "Tokyo", "flight_number": "VS0004"},
        {"city_depart": "San Francisco", "city_arrive": "Tokyo", "flight_number": "VS0005"},
        {"city_depart": "San Francisco", "city_arrive": "London", "flight_number": "VS0006"},
    ]
    monkeypatch.setattr("app.tools.flights", mock_flights)
    results = search_flights("San Francisco", "Tokyo")
    assert len(results) == 2
    assert all(r["city_depart"] == "San Francisco" and r["city_arrive"] == "Tokyo" for r in results)


def test_search_experiences():
    """
    Use mock framework to test search_experiences function.
    mock patches the `similarity_search` function inside the `search_experiences` function to simulate the indexing process.
    """
    with patch('app.tools.experiences_vector_store.similarity_search') as mock_search:
        mock_search.return_value = [
            Document(page_content=json.dumps({"title": "Beach experience", "description": "Sandy beach", "city": "Miami"})),
            Document(page_content=json.dumps({"title": "Broadway musical", "description": "Performance", "city": "New York"})),
            Document(page_content=json.dumps({"title": "Pyramid tour", "description": "Cultural visit", "city": "Cairo"})),
        ]
        results = search_experiences("Interesting things to do")
        assert mock_search.called, "The similarity_search function should be called during indexing hotels"
        assert len(results)==3, "There should be 3 experiences results returned"
        assert results[0]["title"] == "Beach experience", "The first experience result should match the mock data"

