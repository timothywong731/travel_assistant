from pydantic import BaseModel, Field
from typing import List, Optional


class TravelQuery(BaseModel):
    """Request body schema for user travel query."""
    query: str = Field(
        description="User's travel query or request for recommendations",
        example="Looking for a romantic beach getaway in Europe during July"
    )


class HotelRecommendation(BaseModel):
    name: str = Field(description="Name of the hotel", example="Seaside Beach Club")
    city: str = Field(description="City where the hotel is located", example="Barcelona")
    price_per_night: float = Field(description="Price per night in USD", example=150.0)
    rating: float = Field(description="Hotel rating out of 5", example=4.5)


class FlightRecommendation(BaseModel):
    airline: str = Field(description="Airline name", example="Virgin Atlantic")
    from_airport: str = Field(description="Departure airport code", example="LAX")
    to_airport: str = Field(description="Arrival airport code", example="LHR")
    price: float = Field(description="Flight price in USD", example=800.0)
    duration: str = Field(description="Flight duration", example="PT10H15M")
    date: str = Field(description="Flight date", example="2023-07-15")


class ExperienceRecommendation(BaseModel):
    name: str = Field(description="Name of the experience", example="Wine Tasting Tour")
    city: str = Field(description="City where the experience takes place", example="Florence")
    price: float = Field(description="Price of the experience in USD", example=120.0)
    duration: str = Field(description="Duration of the experience", example="PT3H")


class TravelAdvice(BaseModel):
    """Structured response returned by the Gen-AI Travel Assistant."""
    destination: str = Field(description="Recommended travel destination", example="Tokyo")
    reason: str = Field(description="Reason for the recommendation", example="Great culture, food, and safe for travelers.")
    budget: str = Field(description="Estimated budget for the trip", example="Moderate to High")
    tips: List[str] = Field(
        description="List of travel tips and recommendations",
        example=[
            "Visit Senso-ji Temple early morning.",
            "Try local street food in Shibuya.",
            "Use JR Pass for transportation."
        ]
    )

    # Optional enrichments
    hotel: Optional[HotelRecommendation] = None
    flight: Optional[FlightRecommendation] = None
    experience: Optional[ExperienceRecommendation] = None
