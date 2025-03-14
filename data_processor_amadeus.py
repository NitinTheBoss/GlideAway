import os
import requests
import pandas as pd

AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")

# Function to get access token
def get_access_token():
    if not AMADEUS_API_KEY or not AMADEUS_API_SECRET:
        raise ValueError("Missing AMADEUS_API_KEY or AMADEUS_API_SECRET. Set them as environment variables.")

    payload = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_API_KEY,
        "client_secret": AMADEUS_API_SECRET
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(TOKEN_URL, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("access_token")

    print("Failed to get access token:", response.text)
    return None


# Amadeus API URLs
TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
FLIGHT_SEARCH_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"


# Function to search flights
def search_flights(access_token, origin, destination, date):
    headers = {"Authorization": f"Bearer {access_token}"}
    search_params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": 1,
        "currencyCode": "INR",
    }

    response = requests.get(FLIGHT_SEARCH_URL, headers=headers, params=search_params)

    if response.status_code == 200:
        flights = response.json().get("data", [])

        filtered_flights = []
        for flight in flights:
            for itinerary in flight["itineraries"]:
                segments = itinerary["segments"]

                if len(segments) == 1 and segments[0]["departure"]["iataCode"] == origin and segments[0]["arrival"][
                    "iataCode"] == destination:
                    filtered_flights.append({
                        "flight_id": flight["id"],
                        "airline": segments[0]["carrierCode"],
                        "departure_airport": segments[0]["departure"]["iataCode"],
                        "arrival_airport": segments[0]["arrival"]["iataCode"],
                        "departure_time": segments[0]["departure"]["at"],
                        "arrival_time": segments[0]["arrival"]["at"],
                        "price": float(flight["price"]["total"]),
                        "duration": itinerary["duration"]
                    })

        return pd.DataFrame(filtered_flights)

    print("Error:", response.status_code, response.text)
    return pd.DataFrame()


def print_flight_details(flights, origin, destination):
    if flights.empty:
        print(f"No direct flights found from {origin} to {destination}.")
        return

    print(f"\nAvailable Flights ({origin} to {destination}):\n" + "-" * 50)

    for _, flight in flights.iterrows():
        print(f"Airline: {flight['airline']}")
        print(f"From: {flight['departure_airport']} -> {flight['arrival_airport']}")
        print(f"Departure: {flight['departure_time']}")
        print(f"Arrival: {flight['arrival_time']}")
        print(f"Price: ₹{flight['price']}")
        print("-" * 50)


def filter_flights_amadeus(source, destination, date):
    """
    Search and filter flights based on user preferences.
    """
    access_token = get_access_token()

    if access_token:
        flights = search_flights(access_token, source, destination, date)
        print_flight_details(flights, source, destination)

        return flights