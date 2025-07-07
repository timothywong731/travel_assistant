from app.data import hotels, flights, experiences
from app.data import load_json

def test_hotels():
    """Test the hotels list."""
    assert len(hotels) > 0, "Hotels data should not be empty"

def test_hotels_item():
    """Test the structure of a hotel item."""
    assert isinstance(hotels[0], dict), "Each hotel should be a dictionary"
    assert "hotel_name" in hotels[0], "Hotel should have a 'hotel_name' field"
    assert "city" in hotels[0], "Hotel should have a 'city' field"
    assert "rating" in hotels[0], "Hotel should have a 'rating' field"
    assert isinstance(hotels[0]["rating"], (int, float)), "Hotel rating should be a number"

def test_flights():
    """Test the flights list."""
    assert len(flights) > 0, "Flights data should not be empty"

def test_flights_item():
    """Test the structure of a flight item."""
    assert isinstance(flights[0], dict), "Each flight should be a dictionary"
    assert "flight_number" in flights[0], "Flight should have a 'flight_number' field"
    assert "city_depart" in flights[0], "Flight should have a 'city_depart' field"
    assert "city_arrive" in flights[0], "Flight should have an 'city_arrive' field"
    assert "operating_airline" in flights[0], "Flight should have a 'operating_airline' field"
    assert isinstance(flights[0]["plane_type"], (int, float)), "Flight price should be a number"

def test_load_json():
    """Test the load_json function."""
    data = load_json("../seed_data/hotel_catalogue.json")
    assert isinstance(data, list), "Loaded data should be a list"
    assert len(data) > 0, "Loaded data should not be empty"
    assert isinstance(data[0], dict), "Each item in loaded data should be a dictionary"