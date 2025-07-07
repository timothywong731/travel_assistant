import json
import os
from typing_extensions import Literal
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from uuid import uuid4
from langchain_core.documents import Document


SEED_DATA_DIR = os.path.join(os.path.dirname(__file__), "seed_data")

def load_json(filename):
    with open(os.path.join(SEED_DATA_DIR, filename), "r") as f:
        return json.load(f)

hotels = load_json("hotel_catalogue.json")
flights = load_json("flight_catalogue.json")
experiences = load_json("experiences_catalogue.json")


embeddings = OpenAIEmbeddings(model="text-embedding-3-large")


hotels_vector_store = Chroma(
    collection_name="hotels",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db/hotels",
)

flights_vector_store = Chroma(
    collection_name="flights",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db/flights",
)

experiences_vector_store = Chroma(
    collection_name="experiences",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db/experiences",
)


def index_hotels():
    """
    Index hotels into the vector store.
    """
    
    if len(hotels_vector_store.get()['documents']) == 0:
        print("Indexing hotels into vector store...")

        # Create a vector store for hotels
        # Generate unique UUIDs for each hotel
        uuids = [str(uuid4()) for _ in range(len(hotels))]

        # Convert each hotel to a Document
        docs = [Document(page_content=json.dumps(x)) for x in hotels]

        # Add documents to the vector store with their corresponding UUIDs
        hotels_vector_store.add_documents(documents=docs, ids=uuids)
    else:
        print("Hotels already indexed in vector store, skipping indexing.")

def index_flights():
    """
    Index flights into the vector store.
    """
    if len(flights_vector_store.get()['documents']) == 0:
        print("Indexing flights into vector store...")
        # Create a vector store for flights
        # Generate unique UUIDs for each flight
        uuids = [str(uuid4()) for _ in range(len(flights))]

        # Convert each flight to a Document
        docs = [Document(page_content=json.dumps(x)) for x in flights]

        # Add documents to the vector store with their corresponding UUIDs
        flights_vector_store.add_documents(documents=docs, ids=uuids)
    else:
        print("Flights already indexed in vector store, skipping indexing.")


def index_experiences():
    if len(experiences_vector_store.get()['documents']) == 0:
        print("Indexing experiences into vector store...")
        # Create a vector store for experiences
        # Generate unique UUIDs for each experience
        uuids = [str(uuid4()) for _ in range(len(hotels))]

        # Convert each experience to a Document
        docs = [Document(page_content=json.dumps(x)) for x in experiences]

        # Add documents to the vector store with their corresponding UUIDs
        experiences_vector_store.add_documents(documents=docs, ids=uuids)
    else:
        print("Experiences already indexed in vector store, skipping indexing.")





def search_hotels(query: str):
    """
    Search hotels based on a query string.
    """
    
    print(f"🏨 Searching for hotels with query: {query}")
    search_results = hotels_vector_store.similarity_search(query, k=3)
    data = [json.loads(x.page_content) for x in search_results]
    return data



# def search_flights(query:str):
#     """
#     Returns all available flights.
#     """
#     search_results = flights_vector_store.similarity_search(query, k=3)
#     data = [json.loads(x.page_content) for x in search_results]
#     return data


def search_flights(
    city_depart:str,
    city_arrive:str
):
    """
    Returns all available flights for a given departure city and arrival city.
    """

    print(f"✈️ Searching for flights from {city_depart} to {city_arrive}...")
    return [f for f in flights if f["city_depart"] == city_depart and f["city_arrive"] == city_arrive]

def search_flights_by_month(
    city_depart:str, 
    city_arrive:str, 
    month=Literal['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
):
    """
    Returns all available flights for a given departure city, arrival city, and month.
    """

    print(f"✈️ Searching for flights from {city_depart} to {city_arrive} in {month}...")
    return [f for f in flights if f["city_depart"] == city_depart and f["city_arrive"] == city_arrive and 
            (f["depart_month"] == month or f["arrive_month"] == month)]


def search_experiences(query:str):
    """
    Returns all available experiences.
    """

    print(f"🌍 Searching for experiences with query: {query}")
    search_results = experiences_vector_store.similarity_search(query, k=3)
    data = [json.loads(x.page_content) for x in search_results]
    return data