from app.schemas import TravelQuery, TravelAdvice, HotelRecommendation, FlightRecommendation, ExperienceRecommendation

def test_travel_query_schema():
    data = {"query": "Looking for adventure travel in South America"}
    obj = TravelQuery(**data)
    assert obj.query == data["query"]

def test_hotel_recommendation_schema():
    data = {
        "name": "Mountain View Resort",
        "city": "Cusco",
        "price_per_night": 200.0,
        "rating": 4.8
    }
    obj = HotelRecommendation(**data)
    assert obj.name == data["name"]
    assert obj.city == data["city"]
    assert obj.price_per_night == data["price_per_night"]
    assert obj.rating == data["rating"]

def test_flight_recommendation_schema():
    data = {
        "airline": "LATAM",
        "from_airport": "JFK",
        "to_airport": "LIM",
        "price": 650.0,
        "duration": "PT8H30M",
        "date": "2024-08-10"
    }
    obj = FlightRecommendation(**data)
    assert obj.airline == data["airline"]
    assert obj.from_airport == data["from_airport"]
    assert obj.to_airport == data["to_airport"]
    assert obj.price == data["price"]
    assert obj.duration == data["duration"]
    assert obj.date == data["date"]

def test_experience_recommendation_schema():
    data = {
        "name": "Amazon Rainforest Trek",
        "city": "Iquitos",
        "price": 300.0,
        "duration": "PT48H"
    }
    obj = ExperienceRecommendation(**data)
    assert obj.name == data["name"]
    assert obj.city == data["city"]
    assert obj.price == data["price"]
    assert obj.duration == data["duration"]

def test_travel_advice_schema_minimal():
    data = {
        "destination": "Kyoto",
        "reason": "Rich history and beautiful temples.",
        "budget": "Moderate",
        "tips": ["Visit Fushimi Inari Shrine", "Try matcha sweets"]
    }
    obj = TravelAdvice(**data)
    assert obj.destination == data["destination"]
    assert obj.reason == data["reason"]
    assert obj.budget == data["budget"]
    assert obj.tips == data["tips"]
    assert obj.hotel is None
    assert obj.flight is None
    assert obj.experience is None

def test_travel_advice_schema_with_enrichments():
    data = {
        "destination": "Paris",
        "reason": "Romantic city with great food.",
        "budget": "High",
        "tips": ["Book Eiffel Tower tickets in advance"],
        "hotel": {
            "name": "Le Meurice",
            "city": "Paris",
            "price_per_night": 500.0,
            "rating": 4.9
        },
        "flight": {
            "airline": "Air France",
            "from_airport": "JFK",
            "to_airport": "CDG",
            "price": 1200.0,
            "duration": "PT7H",
            "date": "2024-09-01"
        },
        "experience": {
            "name": "Seine River Cruise",
            "city": "Paris",
            "price": 80.0,
            "duration": "PT2H"
        }
    }
    obj = TravelAdvice(**data)
    assert obj.destination == data["destination"]
    assert obj.hotel is not None
    assert obj.hotel.name == data["hotel"]["name"]
    assert obj.flight is not None
    assert obj.flight.airline == data["flight"]["airline"]
    assert obj.experience is not None
    assert obj.experience.name == data["experience"]["name"]